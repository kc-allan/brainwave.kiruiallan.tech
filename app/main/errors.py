from flask import render_template, redirect, url_for
from . import main

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@main.app_errorhandler(401)
def unauthorized(error):
    return redirect(url_for('auth.login'))