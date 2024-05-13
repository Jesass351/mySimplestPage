from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from app import db as db
from functools import wraps
import requests

bp = Blueprint('translate', __name__, url_prefix='/translate')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('translate/index.html')
    if request.method == 'POST':
        API_TOKEN = 'AQVN1SPhgUYvc1ZCbR45oRcVR80_OROhbhkAwDAC'
        texts = request.form.get('text')
        lang = request.form.get('lang')
        body = {    
            "targetLanguageCode": lang,
            "texts": texts,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key {0}".format(API_TOKEN)
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
            json = body,
            headers = headers
        )

        print(response.text)

        text = response.json()['translations'][0]['text']
        return render_template('translate/index.html', text=text, textarea_value = texts)



