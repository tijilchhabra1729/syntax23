from Tool import app,db
from Tool.forms import RegistrationForm, LoginForm, VisitorForm_1
from Tool.models import User, Locker
from flask import render_template, request, url_for, redirect, flash, abort, jsonify, make_response
from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, request
import qrcode
import random
import string
import cv2


cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()


def create_locker():
    for i in range(5):
        key = create_key()
        img = qrcode.make(key)
        img.save("locker"+str(i)+".png")
        locker = Locker(status = 0,
                        key = key)
        db.session.add(locker)
        db.session.commit()

def create_key():
    n = 10
    my_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
    return my_str

with app.app_context():
    db.create_all()
    # create_locker()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        key = create_key()
        img = qrcode.make(key)
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                    key=key)
        db.session.add(user)
        db.session.commit()
        img.save(str(user.id)+".png")  
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
        locker = Locker.query.filter_by(locker_key=str(a)).first()
        locker.user_id = current_user.id
        # current_user.lockers.append(locker)
        locker.locker_status = 1
        db.session.commit()
        print(locker.locker_status)
        return render_template('visitor.htm')


@app.route('/locker/<locker_id>')
@login_required
def manager(locker_id):
    locker = Locker.query.get(locker_id)
    if locker.locker_status == 0:
        return "unlocked"
    
    if current_user.manager != None:
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
        user = User.query.get(locker.user_id)
        if user.key == str(a):
            name = user.name
            f = "thank you " + name + " locker unlocked"
            locker.locker_status = 0
            locker.users = None
            db.session.commit()
            return(f)
        else:
            f = 'error'
            return(f)


@app.route('/temp')
def shit():
    user = User(name="manager",
                    email='admin@gmail.com',
                    password='password',
                    manager=1,
                    key=create_key())
    print('hey')
    db.session.add(user)
    db.session.commit()




    
if __name__ == '__main__':
    app.run(debug=True)
