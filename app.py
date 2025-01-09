import os
import json
from flask import Flask, redirect, render_template, send_from_directory, abort, request # type: ignore
from werkzeug.middleware.proxy_fix import ProxyFix # type: ignore
from crawler import crawl, hashes
from convert_to_hls import generate_hls

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

with open("tree.json", "r") as tree:
    content = json.load(tree)


@app.route("/crawl")
def re_crawl():
    crawl()
    return redirect("/library")

@app.route("/")
@app.route("/home")
def index():
    if not os.path.exists("./tree.json"):
        crawl()
    return redirect("/library")

@app.route("/library")
def library():
    return render_template("index.html", content=hashes)

@app.route("/library/search", methods=["GET"])
def search():
    found_hashes = {}
    searchword = request.args.get('search', '').casefold()
    for hash, abs_path in hashes.items():
        if searchword in abs_path.casefold():
            found_hashes.update({hash: abs_path})
    return render_template("search.html", found_titles=found_hashes)


# Update with your local server's IP and port
localhost = "http://192.168.1.86:8080"

# Base directory for HLS files
hls_base_directory = "/media/kali/2TB/hls"

@app.route("/library/<hash>", methods=["GET"])
def play(hash):
    no_hash = "No such hash found. Please load a different file."
    
    # Construct the HLS directory path
    hls_directory = os.path.join(hls_base_directory, hash)

    # Check if the HLS directory exists
    if os.path.exists(hls_directory) and os.path.isdir(hls_directory):
        # Path to the playlist.m3u8 file
        playlist_path = os.path.join(hls_directory, "playlist.m3u8")
        if os.path.exists(playlist_path):
            # Construct the URL to serve the playlist
            file_path = f"{localhost}/hls/{hash}/playlist.m3u8"
            file_size = sum(
                os.path.getsize(os.path.join(hls_directory, f)) for f in os.listdir(hls_directory) if os.path.isfile(os.path.join(hls_directory, f))
            ) / 1e+9  # Calculate total directory size in gigabytes
            file_size = round(file_size, 2)
        else:
            file_path = no_hash
            file_size = 0
    else:
        file_path = no_hash
        file_size = 0

    # Render the play.html template with the file path and file size
    return render_template(
        "play.html", 
        file_path=file_path, 
        file_size=file_size,
        no_hash=no_hash if file_path == no_hash else None,
    )


app.config['MEDIA_FOLDER'] = '/'

@app.route('/<path:filename>')
def serve_media(filename):
    safe_path = os.path.join(app.config['MEDIA_FOLDER'], filename)
    if not os.path.exists(safe_path):
        abort(404)
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)
