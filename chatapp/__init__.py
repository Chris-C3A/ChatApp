from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from chatapp.src.config import Config

app = Flask(__name__)
socketio = SocketIO(app)
# socketio.init_app(app, cors_allowed_origins="*:*")

app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from chatapp import routes

