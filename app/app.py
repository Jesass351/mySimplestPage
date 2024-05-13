from flask import Flask, render_template
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from math import ceil

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from models import *

from auth import bp as auth_bp, init_login_manager
from speechkit import bp as speechkit_bp

from translate import bp as translate_bp
from vision import bp as vision_bp


app.register_blueprint(auth_bp)
app.register_blueprint(translate_bp)
app.register_blueprint(vision_bp)
app.register_blueprint(speechkit_bp)





init_login_manager(app)


# from models import Book, Cover

@app.route('/')
def index():

        return render_template(
            'index.html',
        )
