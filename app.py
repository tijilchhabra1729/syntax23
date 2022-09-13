from Tool import app,db
from Tool.forms import RegistrationForm, LoginForm
from Tool.models import User
from flask import render_template, request, url_for, redirect, flash, abort, jsonify, make_response
from flask_login import current_user, login_required, login_user, logout_user
import secrets
from sqlalchemy import desc, asc
import os
import json
from flask import Flask, render_template, request, abort
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(9)
        user = User(name1=form.name1.data,
                    name2=form.name2.data,
                    name3=form.name3.data,
                    name4=form.name4.data or '',
                    name5=form.name5.data or '',
                    name6=form.name6.data or '',

                    school1=form.school1.data,
                    school2=form.school2.data,
                    school3=form.school3.data,
                    school4=form.school4.data or '',
                    school5=form.school5.data or '',
                    school6=form.school6.data or '',

                    email1=form.email1.data,
                    emailb=form.emailb.data,

                    phone1=form.phone1.data,
                    phoneb=form.phoneb.data,

                    file1=form.file1.data,
                    file2=form.file2.data,
                    file3=form.file3.data,
                    file4=form.file4.data,

                    interest=form.interest.data,
                    password=form.password.data)
        print('hey')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email1=form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'

    return render_template('login.htm', form=form, mess=error)


if __name__ == '__main__':
    app.run(debug=True)
