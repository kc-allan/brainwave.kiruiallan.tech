from app.models.base_model import Base, BaseModel
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

"""
A message can be:
from USER to GROUP 	- the message is instanciated directly by the group
					- parameters passed: text, sender_id, attachments
	or
 from USER to USER 	- the message is instanciated by the User from a Chat object to represent a conversation between two users
					- parameters passed: text, attachments, chat_id
"""
class Message(BaseModel, Base):
    __tablename__ = 'messages'
    text = Column(String(255), nullable=False)
    attachments = relationship('File', back_populates='message')
    sender_id = Column(String(60), ForeignKey('users.id'), nullable=False) # in a group
    sender = relationship('User', foreign_keys=[sender_id], back_populates='messages')

    chat_id = Column(String(60), ForeignKey('chats.id'))
    chat = relationship('Chat', foreign_keys=[chat_id], back_populates='messages')