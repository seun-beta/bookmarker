from flask import Flask, jsonify


app = Flask(__name__)


@app.get("/")
def index():
    return "Hello World"

@app.get("/hello")
def hello_json():
    return {"information": 1223, "just": "do it"}
