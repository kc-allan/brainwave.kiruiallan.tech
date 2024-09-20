from flask_login import login_required, current_user
from flask import make_response, request, redirect, flash, url_for, render_template
import requests, os
from werkzeug.utils import secure_filename

from . import groups
from app.models import storage
from app.models.group import Group, UserGroupAssociation
from .forms import CreateGroupForm, GroupUpdateForm

url = 'http://localhost:4000/api/v1'

DP_PATH = os.path.abspath(
    os.path.dirname(
        os.path.dirname(__file__)
    )
) + f'/static/icons/group.png'
UPDATEABLE_FIELDS = ['name', 'description', 'displayPic', 'coverPic']

@groups.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
        }
        profile_pic = request.files.get('profilePic')
        print(f"Type of profile_pic: {type(profile_pic)}")
        group = Group(**data)
        if profile_pic:
            group.profilePic = profile_pic
        group.add_member(current_user, role='admin')
        group.save()
        if storage.get('Group', group.id):
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = f'/groups/{group.id}'
            flash('Group created successfully', category='message')
            return make_response(redirect(next_page))
        flash("Error creating group", category='error')
    return make_response(render_template('groups/create_group.html', form=form))

@groups.route('/groups')
def my_groups():
    return render_template('groups/groups_page.html')

@groups.route('/join/<group_id>')
@login_required
def join_group(group_id):
    group = storage.get('Group', group_id)
    if group is None:
        return make_response("Group not found"), 500
    user = current_user
    if user not in group.members:
        group.members.append(user)
        group.save()
        flash("You're now a member", category='message')
    else:
        flash("Already a member", category='error')
    next = request.args.get('next')
    if next is None or not next.startswith('/'):
        next = url_for('accounts.current_user_profile')
    return redirect(next)

@groups.route('/leave/<group_id>')
@login_required
def leave_group(group_id):
    group = storage.get('Group', group_id)
    if group is None:
        return make_response("Error while exiting group")
    group.members.remove(current_user)
    group.save()
    flash(f"You're no longer a member - {group.name}")
    next = request.args.get('next')
    if next is None or not next.startswith('/'):
        next = '/home'
    return make_response(redirect(next))

@groups.route('/<group_id>', methods=['GET'])
@login_required
def group_profile(group_id):
    group = storage.get('Group', group_id)
    # from app.models.chat import Chat
    # chat = Chat(is_groupchat=True)
    # chat.group.append(group)
    # chat.save()
    if group is not None:
        if current_user in group.members + group.admins:
            files = group.files
            members = group.admins + group.members
            profilePic = group.profilePic
            if group.chat:
                return make_response(redirect(f'/chats/{group.chat.id}'))
            return make_response(render_template('groups/group_profile.html',
                                                 group=group,
                                                 files=files,
                                                 members=members,
                                                 profilePic=profilePic
                                                 ))
        flash("You're not a member. Join group to view.", category='warn')
    next = request.args.get('next')
    if next is None or not next.startswith('/'):
        next = '/home'
    return make_response(redirect(next))

@groups.route('/delete/<group_id>')
@login_required
def delete_group(group_id):
    groups = storage.all('Group')
    for group in groups:
        group.delete()
        storage.save()
    flash("Group deleted successfully", category='error')
    next = request.args.get('next')
    if next is None or not next.startswith('/'):
        next = '/accounts/profile'
    return make_response(redirect(next))

@groups.route('<group_id>/settings', methods=['GET', 'PUT'])
@login_required
def group_settings(group_id):
    form = GroupUpdateForm()
    if request.method == 'PUT':
        group = storage.get('Group', group_id)
        if group:
            for key, val in request.form.to_dict():
                if key in UPDATEABLE_FIELDS:
                    setattr(group, key, val)
    return render_template('groups/settings.html')