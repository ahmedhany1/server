from flask import Flask, render_template, redirect, request, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "None"
