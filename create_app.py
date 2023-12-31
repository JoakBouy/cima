from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()

DB_NAME = "cima.db"


base_dir = os.path.dirname(os.path.realpath(__file__))

uri = 'postgresql://buoy:sudanman@localhost:5432/cima'# or other relevant config var
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)


app = Flask(__name__)
app.config['SECRET_KEY'] = "bb50f9bc34d753c0216f8c802f805a86"
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migration = Migrate(app, db)

from views import views
from auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


from models.base_model import User

with app.app_context():
    db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    with app.app_context():
        db.create_all()

def create_database(app):
     if not os.path.exists(os.path.join(base_dir, DB_NAME)):
         db.create_all(app=app)
         print('Created Database!')
