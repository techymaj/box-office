import os
import json
from flask import Flask, redirect, render_template # type: ignore
from crawler import crawl, hashes
from data import movies, series as series_library


app = Flask(__name__)

with open("tree.json", "r") as tree:
    content = json.load(tree)

@app.route("/")
@app.route("/home")
def index():
    if not os.path.exists("./tree.json"):
        crawl()
    return redirect("/library")

@app.route("/library")
def library():
    return render_template("index.html", content=hashes)

@app.route("/library/<hash>", methods=["GET"])
def play(hash):
    # Lookup the hash in the hashes dictionary
    file_path = hashes.get(hash, "No such hash found")
    if file_path is not "No such hash found":
        file_size = os.path.getsize(file_path)
    else:
        file_size = 0

    # Render the play.html template with the file path
    return render_template("play.html", file_path=file_path, file_size=file_size)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)