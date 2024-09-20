from . import files
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import request, render_template
from flask_login import current_user
import os
from werkzeug.utils import secure_filename

basedir = os.path.dirname(__file__).removesuffix('\\files')

STORAGE = 'local'
STORAGE_PATH = basedir + '/static/assets/'

@files.route('/files/upload', methods=['GET', 'POST'])
def upload_file():
    upload_result = None
    thumbnail_url1 = None
    thumbnail_url2 = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        extension = os.path.splitext(file_to_upload.filename)[1]
        if file_to_upload:
            if STORAGE == 'cloud':
                upload_result = upload(file_to_upload)
                thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
                                                     height=100)
                thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
                                                     height=100, radius=20, effect="sepia")
            elif STORAGE == 'local':
                if not os.path.exists(STORAGE_PATH + f'users/{current_user.id}'):
                    os.makedirs(os.path.join(STORAGE_PATH, f'users/{current_user.id}'))
                filename = secure_filename(f'profile-pic' + extension)
                file_to_upload.save(os.path.join(STORAGE_PATH + f'users/{current_user.id}', filename))
                
    return render_template('files/file_upload.html', upload_result=upload_result, thumbnail_url1=thumbnail_url1,
                           thumbnail_url2=thumbnail_url2)