import os, sys, dotenv, click
dotenv.load_dotenv()
from flask import Flask
from app import create_app, socketio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
from app.models.user import User
from app.models.group import Group
from app.models.file import File
from app.models import storage
from app import login_manager

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

COV = None

if os.environ.get('COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()
    

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('COVERAGE'):
        os.environ['COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print("HTML version: file://%s/index.html" % covdir)
        COV.erase()
        
@login_manager.user_loader
def load_user(user_id):
    return storage.get('User', user_id)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.shell_context_processor
def make_shell_context():
    return dict(User=User, Group=Group, File=File)
    

from flask_socketio import rooms, emit, join_room, leave_room, send
@socketio.on('message')    
def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    room = data.get('chat_id')
    if room in rooms():
        emit("message", {"username": username, "message": message}, to=room)
        
@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    join_room(room, sid=username)
    send(username + 'joined')

@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room, sid=username)
    send(username + 'left')

if __name__ == '__main__':
    socketio.run(app,
        host='0.0.0.0',
        port=4000,
        use_reloader=True,
        debug=True
    )