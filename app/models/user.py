from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import Base, BaseModel
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os
from app.models.file import File

user_chat_association = Table(
    'user_chat_association',
    Base.metadata,
    Column('user_id', String(60), ForeignKey('users.id')),
    Column('chat_id', String(60), ForeignKey('chats.id')),
)

class User(BaseModel, UserMixin, Base):
    __tablename__ = 'users'
    _profilePic = Column(String(255), default='static/assets/users/default-profile-pic.png', nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    _password = Column("password", String(128), nullable=False)
    
    chats = relationship('Chat', secondary=user_chat_association, back_populates='participants')
    files = relationship('File', back_populates='owner')
    messages = relationship('Message', back_populates='sender')

    group_associations = relationship('UserGroupAssociation', back_populates='user', cascade='all, delete-orphan', overlaps="groups, admin_at")
    groups = relationship('Group', secondary='user_group_association', back_populates='members', overlaps="group_associations, admin_at")
    admin_at = relationship('Group', secondary='user_group_association', back_populates='admins', overlaps="group_associations")
    
    @property
    def password(self):
        raise AttributeError("password attribute cannot be accessed")
    
    @password.setter
    def password(self, pwd):
        self._password = md5(pwd.encode()).hexdigest()
    
    def verify_password(self, pwd):
        return md5(pwd.encode()).hexdigest() == self._password
    
    @property
    def profilePic(self):
        return self._profilePic
    
    @profilePic.setter
    def profilepic(self, pic):
        if hasattr(pic, 'filename'):
            extension = os.path.splitext(pic.filename)[1]
            filename = 'profile-pic' + extension
        else:
            raise ValueError("Cannot parse given file")
        saved = self.uploadFile(pic, filename)
        if not isinstance(saved, File):
            raise ValueError("Error uploading profile picture")
        self._profilePic = os.path.join(saved.filepath, saved.filename)
    
    def uploadFile(self, file, filename):
        filedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.abspath(os.path.dirname(filedir))
        relative_path = f'static/assets/users/{self.username}/shared'
        full_path = os.path.join(basedir, relative_path)
        if os.path.splitext(filename)[0] == 'profile-pic' or os.path.splitext(filename)[0] == 'cover-pic':
            relative_path = f'static/assets/users/{self.username}/'
            full_path = os.path.join(basedir, relative_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        file.save(os.path.join(full_path, filename))
        saved_file = File(
            **{
                'filepath': relative_path,
                'filename': filename,
                'owner': self,
            }
        )
        return saved_file