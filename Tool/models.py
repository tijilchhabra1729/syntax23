from Tool import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    manager = db.Column(db.Integer, nullable=True)
    password_hash = db.Column(db.String(128))
    key = db.Column(db.String(128))
    lockers = db.relationship('Locker' , backref = 'users' , lazy = 'dynamic')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, password, name, email, key):
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.email = email
        self.key = key


class Locker(db.Model):
    __tablename__ = 'lockers'
    locker_id = db.Column(db.Integer, primary_key=True)
    locker_status = db.Column(db.Integer)
    locker_key=db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, status, key):
        self.locker_status = status
        self.locker_key = key