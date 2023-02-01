import flask

from flask import Flask, request, abort, send_file
from flask_cors import CORS
from pathlib import Path

import requests

app = Flask(__name__)

CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/api/recognize', methods=['POST'])
def recognize_api():
    file = request.files["document"]
