from api.v1.views import api_views
from app.models import storage
from flask import request, make_response, jsonify

@api_views.route('/groups', methods=['GET'])
def groups_all():
    if request.method == 'GET':
        groups = storage.all('Group').values()
        groups = [group.to_dict() for group in groups]
        return make_response(jsonify(groups), 200)
    
@api_views.route('/groups/<group_id>', methods=['GET'])
def groups_one(group_id):
    if request.method == 'GET':
        group = storage.get('Group', group_id)
        parsed = group.to_dict()
        parsed['admins'] = [admin.to_dict() for admin in group.admins]
        parsed['members'] = [member.to_dict() for member in group.members + group.admins]
        parsed['files'] = [file.to_dict() for file in group.files]
        return make_response(jsonify(parsed), 200)
    