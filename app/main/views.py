from flask import render_template, redirect, url_for, request
from flask_login import current_user, logout_user, login_required
from uuid import uuid4
from app.models import storage
import time

from . import main
from .forms import ContactForm

cache_id = str(uuid4())

@main.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    return render_template('index.html', current_user=current_user)

@main.route('/home')
@login_required
def home():
    return render_template('home.html',
                           user=current_user,
                           cache_id=cache_id,
                           )

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@main.route('/help', methods=['GET', 'POST'])
def help():
    form = ContactForm(request.form)
    return render_template('contact_us.html', form=form)