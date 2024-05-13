import os

SECRET_KEY = 'kdnndkkw'

#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:cloud@mysql_db:3306/cloud'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2033_cloud:123456789@std-mysql.ist.mospolytech.ru/std_2033_cloud'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

USER_ROLE = 3
MODERATOR_ROLE = 2
ADMINISTRATOR_ROLE = 1

BOOKS_ON_INDEX_PAGE = 3


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
