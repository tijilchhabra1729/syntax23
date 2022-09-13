from lzma import FILTER_LZMA1
from Tool import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(64))
    name2 = db.Column(db.String(64))
    name3 = db.Column(db.String(64))
    name4 = db.Column(db.String(64))
    name5 = db.Column(db.String(64))
    name6 = db.Column(db.String(64))

    school1 = db.Column(db.String(64))
    school2 = db.Column(db.String(64))
    school3 = db.Column(db.String(64))
    school4 = db.Column(db.String(64))
    school5 = db.Column(db.String(64))
    school6 = db.Column(db.String(64))

    email1 = db.Column(db.String(64))
    emailb = db.Column(db.String(64))

    phone1 = db.Column(db.Integer)
    phoneb = db.Column(db.Integer)

    file1 = db.Column(db.String(64))
    file2 = db.Column(db.String(64))
    file3 = db.Column(db.String(64))
    file4 = db.Column(db.String(64))

    interest = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, password, name1, name2, name3, name4, name5, name6, school1, school2, school3, school4, school5, school6, email1, emailb, phone1, phoneb, interest, file1, file2, file3,  file4):
        self.password_hash = generate_password_hash(password)
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name4 = name4
        self.name5 = name5
        self.name6 = name6

        self.school1 = school1
        self.school2 = school2
        self.school3 = school3
        self.school4 = school4
        self.school5 = school5
        self.school6 = school6

        self.email1 = email1
        self.emailb = emailb

        self.phone1 = phone1
        self.phoneb = phoneb

        self.interest = interest

        self.file1 = file1
        self.file2 = file2
        self.file3 = file3
        self.file4 = file4
