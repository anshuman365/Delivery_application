import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql12773739:muGBJitR88@sql12.freesqldatabase.com:3306/sql12773739'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
    INVOICE_FOLDER = os.path.join(basedir, 'static', 'invoices')


#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/diesel_delivery'