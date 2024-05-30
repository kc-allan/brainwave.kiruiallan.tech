from flask import request, render_template, make_response, redirect, flash, url_for
from flask_login import current_user, login_user
from uuid import uuid4

from . import auth
from .forms import RegistrationForm, LoginForm
from app.models import storage
from app.models.user import User

cache_id=str(uuid4())

@auth.route('/auth/signup', methods=['GET','POST'])
async def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = storage.get_username('User', request.form['username'])
            if user is None:
                user = User(**request.form.to_dict())
                user.save()
                return redirect(url_for('auth.login'))
            else:
                flash('Username is taken')
        for errors in form.errors.values():
            for err in errors:
                flash(err)
    return render_template('auth/signup.html',
                           form=form,
                           title='Create Account',
                           user=current_user,
                           cache_id=cache_id)

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = storage.get_username('User', request.form['username'])   
        if user is not None and user.verify_password(request.form['password']):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = '/home'
            return redirect(next)
        flash("Invalid Credentials")
    return render_template('auth/login.html',
                           form=form,
                           user=current_user,
                           cache_id=cache_id)