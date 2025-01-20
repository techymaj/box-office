import os
import json
from flask import Flask, redirect, render_template, render_template_string, send_from_directory, abort, request # type: ignore
# from crawler import crawl, hashes
import crawler
from environment_variables import localhost
from extract_subtitles import extract_subtitles
from file_metadata import extract_info
from get_poster_path import get_poster_path
from download_metadata import download_meta
from srt_to_vtt import srt_to_vtt
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
    crawler.crawl()
    return redirect("/library")

@app.route("/")
@app.route("/home")
def index():
    if not os.path.exists("./tree.json"):
        crawler.crawl()
    return redirect("/library")

@app.route("/library")
def library():
    meta = {}
    for hash, file_path in crawler.hashes.items():

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
    for hash, abs_path in crawler.hashes.items():
        if searchword in abs_path.casefold():
            # Extract metadata
            metadata = extract_info(abs_path)
            found_hashes.update({hash: metadata})

    return render_template(
        "search.html" if found_hashes else "404.html", 
        found_titles=found_hashes,
    )
    

@app.route("/library/<hash>", methods=["GET"])
def play(hash):
    # Lookup the hash in the hashes dictionary
    file_path = crawler.hashes.get(hash, no_hash)
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

    # Fetch related content
    related_title = metadata["title"]
    related = {}

    title_words = related_title.lower().split()
    if len(title_words) > 1:
        del title_words[1:]
    searchword = " ".join(title_words)

    for id, related_path in crawler.hashes.items():
        if id == hash:
            continue
        if searchword in related_path.casefold():
            found_metadata = extract_info(related_path)
            if len(related) <= 5:
                related.update({id: found_metadata})


    # Extract subtitles
    if file_path.lower().endswith((".mkv", ".mp4")):
        subtitles_dir = f'{parent_dir}/subtitles/{hash}'
        input_file = file_path.split("/")[-1]
        print(f"Processing {input_file} for subtitles")
        message = None
        if not os.path.exists(subtitles_dir):
            message = extract_subtitles(file_path, subtitles_dir)

        # convert .srt to webVTT
        subtitle_files = []
        if os.path.exists(subtitles_dir):
            subtitles = os.listdir(subtitles_dir)
            for i, subtitle in enumerate(subtitles):
                path_to_my_srt_file = f"{parent_dir}/subtitles/{subtitle}"
                path_to_converted_vtt_file = f"{parent_dir}/subtitles/{hash}/{subtitle}_v{i}.vtt"
                srt_to_vtt(path_to_my_srt_file, path_to_converted_vtt_file)
                subtitle_files.append(path_to_converted_vtt_file)

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
        hash=hash,
        related_content=related,
        subtitle_paths=subtitle_files,
        message=message if message else "Subttiles available.",
    )

@app.route("/library/<hash>", methods=["POST"])
def update_metadata(hash):
    updated_title = request.form.get("title", "")
    current_filepath = crawler.hashes.pop(hash, no_hash)
    
    splits = current_filepath.split("/")
    old_title = splits[-1]

    parent_dir = os.path.dirname(current_filepath)
    old_filepath = f"{parent_dir}/{old_title}"
    new_filepath = f"{parent_dir}/{updated_title}"
    os.rename(old_filepath, new_filepath)
    crawler.crawl()

    # Extract metadata
    metadata = extract_info(new_filepath)
    return render_template_string(
        "<p class='title'>Title: {{metadata['title']}}</p>", 
        metadata=metadata,
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
