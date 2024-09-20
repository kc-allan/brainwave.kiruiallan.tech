from app.models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
import app.models
from app.models.file import File
import os

# user_group_association = Table(
#     'user_group_association',
#     Base.metadata,
#     Column('user_id', String(60), ForeignKey('users.id'), primary_key=True, nullable=False),
#     Column('group_id', String(60), ForeignKey('user_groups.id'), primary_key=True, nullable=False),
#     Column('role', String(60), nullable=False, default='member'),
# )

class UserGroupAssociation(Base):
    __tablename__ = 'user_group_association'
    user_id = Column(String(60), ForeignKey('users.id'), primary_key=True)
    group_id = Column(String(60), ForeignKey('user_groups.id'), primary_key=True)
    role = Column(String(8), default='member')
    user = relationship("User", back_populates="group_associations", overlaps="admin_at,groups")
    group = relationship("Group", back_populates="user_associations", overlaps="admin_at, groups")

class Group(BaseModel, Base):
    __tablename__ = 'user_groups'
    _profilePic = Column(String(255), default='static/assets/groups/default-profile-pic.jpg', nullable=False)
    _coverPic = Column(String(255), default='static/assets/groups/default-cover-pic.jpg', nullable=False)
    name = Column(String(25), nullable=False)
    description = Column(String(128), nullable=False)
    
    chat_id = Column(String(60), ForeignKey('chats.id'))
    chat = relationship('Chat', back_populates='group')
    files = relationship('File', back_populates='group')
    
    user_associations = relationship('UserGroupAssociation', back_populates='group', cascade='all, delete-orphan', overlaps="admin_at,groups")
    members = relationship('User', secondary='user_group_association', back_populates='groups', 
                           primaryjoin="and_(UserGroupAssociation.group_id==Group.id, UserGroupAssociation.role=='member')", overlaps="admin_at, user, group, user_associations, group_associations")
    admins = relationship('User', secondary='user_group_association', back_populates='admin_at',
                          primaryjoin="and_(UserGroupAssociation.group_id==Group.id, UserGroupAssociation.role=='admin')",
                          overlaps="groups, members, user, group, user_associations, group_associations")
    
    def add_member(self, user, role='member'):
        if user not in self.members or user not in self.admins:
            association = UserGroupAssociation(user=user, group=self, role=role)
            self.user_associations.append(association)
            
    def promote_user(self, user):
        session = app.models.storage.get_session()
        association = session.query(UserGroupAssociation).filter_by(
            user_id = user.id, group_id = self.id).first()
        association.role = 'admin'
        session.commit()
        
    def demote_user(self, user):
        session = app.models.storage.get_session()
        association = session.query(UserGroupAssociation).filter_by(
            user_id = user.id, group_id = self.id).first()
        association.role = 'member'
        session.commit()
     
    @property
    def profilePic(self):
        return self._profilePic
    
    @profilePic.setter
    def profilePic(self, pic):
        if hasattr(pic, 'filename'):
            extension = os.path.splitext(pic.filename)[1]
            filename = 'profile-pic' + extension
        else:
            raise ValueError("Cannot parse given file")
        saved = self.uploadFile(pic, filename)
        if not isinstance(saved, File):
            raise ValueError("Error uploading profile picture")
        self._profilePic = os.path.join(saved.filepath, saved.filename)
        
    @property
    def coverPic(self):
        return self._coverPic
    
    @coverPic.setter
    def coverPic(self, pic):
        if hasattr(pic, 'filename'):
            extension = os.path.splitext(pic.filename)[1]
            filename = 'cover-pic' + extension
        else:
            raise ValueError("Cannot parse given file")
        saved = self.uploadFile(pic, filename)
        if not isinstance(saved, File):
            raise ValueError("Error uploading cover picture")
        self._coverPic = os.path.join(saved.filepath, saved.filename)
    
    def uploadFile(self, file, filename):
        print(filename)
        filedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.abspath(os.path.dirname(filedir))
        relative_path = f'static/assets/groups/{self.id}/shared'
        full_path = os.path.join(basedir, relative_path)
        if os.path.splitext(filename)[0] == 'profile-pic' or os.path.splitext(filename)[0] == 'cover-pic':
            relative_path = f'static/assets/groups/{self.id}/'
            full_path = os.path.join(basedir, relative_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        file.save(os.path.join(full_path, filename))
        saved_file = File(
            **{
                'filepath': relative_path,
                'filename': filename,
                'group': self,
            }
        )
        return saved_file
        
    def dp_path(self):
        file = app.models.storage.get('File', field='owner_id', value=self.id)
        