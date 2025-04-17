import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://root:1234@localhost/diesel_delivery'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sarvarsingh:(sarvar777)@db4free.net/diesel_delivery'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
    INVOICE_FOLDER = os.path.join(basedir, 'static', 'invoices')
