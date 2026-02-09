#!/usr/bin/env python3
"""
app.py - minimal Flask API

Production:
    gunicorn -w 4 -b 0.0.0.0:8000 app:app
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/data", methods=["GET"])
def api_data():
    return jsonify(
        status="success",
        message="Service is running",
        data=[1, 2, 3, 4],
    )


if __name__ == "__main__":
    # Local testing only
    app.run(host="127.0.0.1", port=5000)

