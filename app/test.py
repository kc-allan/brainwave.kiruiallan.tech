from models.user import User
from models.group import Group
from models.chat import Chat
from models.file import File
from models.message import Message

user = User(
    username='smurfke',
    first_name='Allan',
    last_name='Kirui',
    password="qwertyuiop12345"
)

group = Group(
    name='Wakali Wao',
    description='The Last of Us',
)

groupprofilePic = File(
    filename='profile-pic.jpg',
    filepath='static/assets/groups',
    filetype='profilePic',
)