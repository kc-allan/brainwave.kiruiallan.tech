#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import api_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from app.models import storage
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = '0.0.0.0'
port = 5000

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "http://127.0.0.1:4000"}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(api_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_400(exception):
    """
    handles 400 errros, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port, use_reloader=True)
