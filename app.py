from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def hello():
    return redirect("/library")

@app.route("/library")
def library():
    return "Library"
