from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    return "<h3>This is an even newer response V3!</h3>"
