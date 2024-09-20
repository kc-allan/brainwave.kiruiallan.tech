from flask import render_template, request
from flask_login import current_user, login_required
from uuid import uuid4

from . import accounts
from app.models import storage

cache_id = uuid4()

@accounts.route('/accounts/profile')
@login_required
def current_user_profile():
    groups = current_user.groups
    files=current_user.owned_files
    nav = request.args.get('nav')
    content = 'groups' if nav == 'groups' or nav is None else 'files'
    suggestions = storage.all('Group').values()
    new_suggestions = []
    user_groups = [str(grp.id) for grp in current_user.groups]
    for group in suggestions:
        if group.id not in user_groups:
            new_suggestions.append(group)
    return render_template('accounts/current_user_profile.html',
                           user=current_user,
                           content=content,
                           cache_id=cache_id,
                           my_groups=groups,
                           my_files=files,
                           suggestions=new_suggestions)
    
@accounts.route('/settings')
def settings():
    return render_template('accounts/settings.html')