from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from app import db as db
from functools import wraps
import base64
import requests


bp = Blueprint('vision', __name__, url_prefix='/vision')

def encode_file(file):
  file_content = file.read()
  return base64.b64encode(file_content) 

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('vision/index.html')
    if request.method == 'POST':
        image = encode_file(request.files['file'])
        content_str = str(image)[2:-1]
        body = {
            "mimeType": "JPEG",
            "languageCodes": ["*"],
            "model": "page",
            "content": content_str
        }
        API_TOKEN = "AQVN1SPhgUYvc1ZCbR45oRcVR80_OROhbhkAwDAC"
        catalog = "b1gbugbuqoa1o1qr6a6h"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key {0}".format(API_TOKEN),
            "x-folder-id" : catalog,
        }
        response = requests.post('https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText',
            headers = headers,
            json = body
        )
        print(response.json())
        text = response.json()['result']['textAnnotation']['fullText']
        return render_template('vision/index.html', text=text)



