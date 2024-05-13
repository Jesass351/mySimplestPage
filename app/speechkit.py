from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User
from app import db as db
from functools import wraps

import urllib.request
import json


bp = Blueprint('speechkit', __name__, url_prefix='/speechkit')


@bp.route('/', methods=['GET', 'POST'])
def index():
    # try:

        if request.method == 'GET':
            return render_template('speechkit/index.html')
    # except:
    #     flash('Ошибка при загрузке', 'danger')
    #     return redirect(url_for('index'))

@bp.route('/recognition', methods=['GET', 'POST'])
def recognition():
    if request.method == "GET":
        return render_template('speechkit/recognition.html')
    if request.method == "POST":
        FOLDER_ID = "b1gbugbuqoa1o1qr6a6h"
        IEM_TOKEN = "t1.9euelZrPjJWanMzPk8iek8-NlI6Rze3rnpWajpSJz5qJx57MlJGel4-LmZ7l9PckIXdN-e93aGrC3fT3ZE90Tfnvd2hqws3n9euelZqTlY_IyIuRzcnNzZGUysqTm-_8xeuelZqTlY_IyIuRzcnNzZGUysqTmw.amMS-OEWO0OUJ8_QkSTdALL0x_F2ln8hdN03r54MrQMwXjzuHxiLX8RzgetKB0gkPIC4Sr33ey9EfZr3Lq9OBA"
        params = "&".join([
            "topic=general",
            "folderId=%s" % FOLDER_ID,
            "lang=ru-RU"
        ])
        data = request.files['audio']
        

        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
        # Аутентификация через IAM-токен.
        url.add_header("Authorization", "Bearer %s" % IEM_TOKEN)

        responseData = urllib.request.urlopen(url).read().decode('UTF-8')
        decodedData = json.loads(responseData)

        if decodedData.get("error_code") is None:
            print(decodedData.get("result"))
        return render_template('speechkit/recognition.html', text=decodedData.get("result"))
        

@bp.route('/register', methods=['POST', 'GET'])
def register():
    # try:
        if request.method == 'POST':
            login_form = request.form.get('login')
            password_form = request.form.get('password')
           
            if login_form and password_form:
                user = db.session.execute(db.select(User).filter_by(login=login_form)).scalar()
                if not user:
                    print('---------------------')
                    user = User(login=login_form, first_name=login_form, last_name=login_form)
                    print(user.login)
                    user.set_password(password_form)
                    db.session.add(user)
                    db.session.commit()

                    login_user(user)
                    flash('Вход выполнен успешно', 'success')
                    next = request.args.get('next')
                    return redirect(url_for('index') or next)
                flash('Логин занят', 'warning')
                return redirect(url_for('auth.login'))
            return redirect(url_for('index'))
        if request.method == 'GET':
            return render_template('auth/register.html')
             

@bp.route('/logout')
@login_required
def logout():
    # try:
        logout_user()
        return redirect(url_for('index'))
    # except:
    #     flash('Ошибка. Попробуйте позже', 'danger')
    #     return redirect(url_for('index'))

def check_rights(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = None
            user_id = kwargs.get("user_id")
            if user_id:
                user = load_user(user_id)
            if not current_user.can(action, user):
                flash("Недостаточно прав", "warning")
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return wrapper
    return decorator
