import os
import json
from flask import Flask, redirect, render_template, send_from_directory, abort, request # type: ignore
from crawler import crawl, hashes
from environment_variables import localhost
from file_metadata import extract_info
from get_poster_path import get_poster_path
from download_metadata import download_meta
from werkzeug.middleware.proxy_fix import ProxyFix # type: ignore

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

with open("tree.json", "r") as tree:
    content = json.load(tree)


no_hash = "No such hash found. Please load a different file."

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
    meta = {}
    for hash, file_path in hashes.items():

        # Extract metadata
        metadata = extract_info(file_path)

        meta.update({hash: metadata})

    return render_template(
        "index.html", 
        content=meta,
    )

@app.route("/library/search", methods=["GET"])
def search():
    found_hashes = {}
    searchword = request.args.get('search', '').casefold()
    for hash, abs_path in hashes.items():
        if searchword in abs_path.casefold():
            found_hashes.update({hash: abs_path})

    return render_template(
        "search.html", 
        found_titles=found_hashes,
    )

@app.route("/library/<hash>", methods=["GET"])
def play(hash):
    # Lookup the hash in the hashes dictionary
    file_path = hashes.get(hash, no_hash)
    if file_path is not no_hash:
        file_size = os.path.getsize(file_path)
        file_size = file_size / 1e+9  # Convert from bytes to gigabytes
        file_size = round(file_size, 2)
    else:
        file_path = no_hash
        file_size = 0

    # Extract metadata
    metadata = extract_info(file_path)

    # Download poster
    synopsis, _ = download_meta(file_path, metadata["title"])

    parent_dir = os.path.dirname(file_path)
    synopsis_path = f'{parent_dir}/synopsis.txt'

    if os.path.exists(synopsis_path):
        with open(synopsis_path, 'r') as f:
            syn = f.read()
    
    # Get poster
    poster_path = get_poster_path(file_path, "/static/images/fallback.jpg")
    poster_url = f"{localhost}{poster_path}"

    # Render the play.html template with the file path
    return render_template(
        "play.html", 
        file_path=f"{localhost}{file_path}" 
        if file_path != no_hash 
        else file_path, 
        file_size=file_size,
        no_hash=no_hash,
        metadata=metadata,
        poster=poster_url,
        synopsis=syn if os.path.exists("./synopsis.txt") else synopsis,
    )


app.config['MEDIA_FOLDER'] = '/'

@app.route('/<path:filename>')
def serve_media(filename):
    safe_path = os.path.join(app.config['MEDIA_FOLDER'], filename)
    if not os.path.exists(safe_path):
        abort(404)
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=80, debug=True)
