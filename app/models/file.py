from app.models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

"""
For Users
"""
class File(BaseModel, Base):
    __tablename__ = 'files'
    filename = Column(String(60), nullable=False)
    filepath = Column(String(255), nullable=False)
    
    owner_id = Column(String(60), ForeignKey('users.id'))
    owner = relationship('User', back_populates='files')
    
    group_id = Column(String(60), ForeignKey('user_groups.id'))
    group = relationship('Group', back_populates='files')
    
    message_id = Column(String(60), ForeignKey('messages.id'))
    message = relationship('Message', back_populates='attachments')
        

"""
For Groups
"""
# class GroupFile(File):
#     recipient_user = relationship('User', back_populates='saved_files', viewonly=False, foreign_keys='SharedFile.user_id')
#     user_id = Column(String(60), ForeignKey('users.id'))
#     recipient_group = relationship('Group', back_populates='group_files', foreign_keys='SharedFile.group_id')
#     group_id = Column(String(60), ForeignKey('groups.id'))