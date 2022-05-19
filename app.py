from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "None"
