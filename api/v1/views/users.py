from api.v1.views import api_views
from app.models.user import User
from app.models import storage
from flask import request, make_response, jsonify, abort

@api_views.route('/users', methods=['GET', 'POST'])
def users_all():
    if request.method == 'GET':
        users = storage.all('User').values()
        users = [user.to_dict() for user in users]
        return make_response(jsonify(users), 200)
    
    if request.method == 'POST':
        data = request.get_json()
        profile_pic = request.files['profile_pic']
        if data is None:
            abort(400, "Not a JSON")
        if data.get('username') is None:
            abort(400, "Missing username")
        if data.get('password') is None:
            abort(400, 'Missing password')
        user = User(**data)
        if profile_pic:
            user.profilePic = profile_pic
            user.save()
        if storage.get('User', user.id) is None:
            abort(404, "Could not complete user creation")
        return make_response(jsonify(user.to_dict()), 201)
    
@api_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_one(user_id):
    if request.method == 'GET':
        user = storage.get('User', user_id)
        if user is None:
            abort(404, "User not found")
        parsed_user = user.to_dict()
        parsed_user['groups'] = [group.to_dict() for group in user.groups]
        parsed_user['files'] = [file.to_dict() for file in user.files]
        parsed_user['chats'] = [chat.to_dict() for chat in user.chats]
        return make_response(jsonify(parsed_user), 200)
    
    user = storage.get('User', user_id)
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if not user:
            abort(404, "User not found")
        user.update(data)
        
    if request.method == 'DELETE':
        user.delete()
        del user
        return make_response(jsonify({}), 204)