import os, sys, dotenv, click
dotenv.load_dotenv()
from flask import Flask
from app import create_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
from app.models.user import User
from app.models.group import Group
from app.models.file import File
from app.models import storage
from app import login_manager

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

@login_manager.user_loader
def load_user(user_id):
    return storage.get('User', user_id)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.shell_context_processor
def make_shell_context():
    return dict(User=User, Group=Group, File=File)

@app.cli.command('test')
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=4000,
        use_reloader=True,
        debug=True
    )

# COV = None
# if os.environ.get('FLASK_COVERAGE'):
#     import coverage
#     COV = coverage.coverage(branch=True, include='app/*')
#     COV.start()