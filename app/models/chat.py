from app.models.base_model import BaseModel, Base
from app.models.user import user_chat_association
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


"""
A chat is created for USER to USER conversations by the creator which is defined by creator_id
On creation the the recipient gets an additional chats in their invited_chats column
A chat therefore has several messages
A group cannot instanciate a chat
"""
class Chat(BaseModel, Base):
    __tablename__ = 'chats'
    is_groupchat = Column(Boolean, default=False, nullable=False)
    messages = relationship('Message', back_populates='chat')
    participants = relationship('User', secondary=user_chat_association, back_populates='chats', foreign_keys=[])
    
    # group_id = Column(String(60), ForeignKey('groups.id'), nullable=True)
    group = relationship('Group', back_populates='chat')