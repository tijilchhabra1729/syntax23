from Tool import app,db
from Tool.forms import RegistrationForm, LoginForm, VisitorForm_1
from Tool.models import User
from flask import render_template, request, url_for, redirect, flash, abort, jsonify, make_response
from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, request
import qrcode
import random
import string
import cv2
import webbrowser


cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

with app.app_context():
    db.create_all()

def create_key():
    n = 10
    my_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
    return my_str

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(9)
        user = User(name=form.name.data,
                    email=form.email.data,
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

        user = User.query.filter_by(email=form.email.data).first()

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

@app.route('/locker', methods=['GET', 'POST'])
@login_required
def locker():
    if current_user.manager == None:
        form1 = VisitorForm_1()
        if form1.validate_on_submit():

            data = create_key()
            img = qrcode.make(data)
            current_user.key = data
            db.session.commit()
            user_id = current_user.id
            img.save(str(user_id)+".png")    

        return render_template('visitor.htm', form1=form1)
    
    else:
        while True:
            _,img = cap.read()
            data, bbox, _ = detector.detectAndDecode(img)
            if data: 
                a = data
                break
            cv2.imshow('scan', img)
            if cv2.waitKey(1) == ord('q'):
                break
        try:
            cap.release()
        except:
            print("Scanned")
        cv2.destroyAllWindows()

        user = User.query.filter_by(key=a).first()
        name = user.name
        f = "thank you " + name
        return(f)

@app.route('/temp')
def shit():
    user = User(name="manager",
                    email='admin@gmail.com',
                    password='password',
                    manager=1)
    print('hey')
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
