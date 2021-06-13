from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ ='users'

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255))
    email=db.Column(db.String(255), unique=True, index = True)
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String())
    password_hash=db.Column(db.String(255))
    pass_secure = db.Column(db.String(255), unique=True, index=True)
    pitch = db.relationship('Pitch',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__='pitches'

    id=db.Column(db.Integer, primary_key=True)
    pitch_title=db.Column(db.String)
    pitch_id=db.Column(db.Integer)
    pitch_idea=db.Column(db.String(1000))
    category=db.Column(db.String(255))
    posted=db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))

class Pitch:
    def __init__(self, pitch_title, pitch_idea, category ):
        self.pitch_title = pitch_title
        self.pitch_idea = pitch_idea
        self.category = category


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod 
    def get_pitches(cls,id):
        pitches=Pitch.query.filter_by(pitch_id=id).all()
        return pitches
