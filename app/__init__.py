from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
from flask_socketio import SocketIO

bootstrap = Bootstrap()
login_manager = LoginManager()
cors = CORS()
socketio = SocketIO(cors_allowed_origins='*') 

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .accounts import accounts as accounts_blueprint
    app.register_blueprint(accounts_blueprint)
    
    from .groups import groups as groups_blueprint
    app.register_blueprint(groups_blueprint)
    
    from .files import files as files_blueprint
    app.register_blueprint(files_blueprint)

    return app