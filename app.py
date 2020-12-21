from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import googlemaps
import math
import requests
from boto.s3.connection import S3Connection
import json
import time
from uszipcode import SearchEngine
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from twilio.rest import Client
import os
from send_mail import send_mail
from datetime import timedelta
from flask_mail import Mail, Message
import smtplib
import ssl
aefdsv = []
delta = timedelta(
    weeks=1
)


app = Flask(__name__)

hi786 = uuid.uuid1()
app.secret_key = 'djgoihdojdhnit0erhgn3erdi0bm540e9rjg0934ermb94e05erwgb9rtehn0394erpdbfnthrerdsg.,bfgdfgmnbkkfgd.xfxbkhzxpingeoirty3h4w80thw80*H*$T)*HE)*Gfhrdt'
app.config['REMEMBER_COOKIE_DURATION'] = delta
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


env = 'dev'

if env == 'dev':
    app.debug = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bvipgytqmvgyiq:7b6c0f324808e528c01d5e2351c52834e94cdb8fc92cdd3e268a0977a8ca2d84@ec2-54-235-192-146.compute-1.amazonaws.com:5432/dfmrk83fdrmlua'

else:
    app.debug = False
    database_key = os.environ.get('DATABASE_URL')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_key

    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)


db = SQLAlchemy(app)

# Define the User data-model


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String)
    checkin = db.Column(db.Boolean)
    phone_number = db.Column(db.String, nullable=True)
    callstatus = db.Column(db.Boolean)
    verification = db.Column(db.Boolean)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles')
    secret_code = db.Column(db.String)

# Define the Role data-model


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))

# Define the UserRoles association table


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


'''
db.create_all()
db.session.commit()
'''


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')


@app.route('/.well-known/acme-challenge/JDMqizXXpBvEaMoC87xpHy-XphwxO8sz72KNzartHes')
def ssl():
    return render_template('ssl.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/f')
def f():
    return render_template('aboutus.html')


@app.route('/aboutus')
def aboutus():
    return render_template('updated_aboutus.html')


@app.route('/webinar')
def webinar():
    return render_template('webinar.html')


@app.route('/help')
def help():
    return render_template('help_page.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/login')
def login():
    return render_template("index2.html")


@app.route('/final')
@login_required
def final():
    return render_template('final.html', name=current_user.first_name)


@app.route('/doctr')
def doctr():
    return 'gihgihsgheruighefdgheroigehrgiohoiergieoroghierghoerighoiergh'


@app.route('/hi')
def hi():
    return render_template('yeet.html')


@app.route("/dctrsignup")
def dctrsignup():
    return render_template("dctrsignup.html")


@app.route("/checkin")
def checkin():
    return render_template("checkin.html")


@app.route('/doctorstatus')
def status():
    return render_template("checkin2.html")


@app.route('/test')
@login_required
def test():
    weeee = User.query.filter_by(checkin=True).all()
    return render_template('test.html', test=weeee)


@app.route('/no')
def ni():
    return('ifg')


@app.route('/checkin2/<hi>', methods=["POST", "GET"])
def checkin2(hi):
    if request.method == "POST":
        u = User.query.filter_by(secret_code=hi).first()
        u.checkin = False
        u.secret_code = None
        db.session.commit()
        flash("Checked Out")
        return redirect('/logout')
    else:
        y = User.query.filter_by(secret_code=hi).first()
        return render_template('checko.html', hi=y.first_name, bye=hi)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if 'check2' in request.form:
            return redirect('/doctorstatus')
        if 'home' in request.form:
            return redirect('/')
        if 'kii' in request.form:
            return redirect('/login')
        if 'submit' in request.form:
            uoo = request.form['content']
            uii = request.form['content2']
            user = User.query.filter_by(username=uoo).first()
            if user:
                if check_password_hash(user.password, uii):
                    login_user(user, remember=True)
                    return redirect('/final')
                else:
                    flash("Invalid username or password")
                    return redirect('/login')
            else:
                flash("Invalid username or password")
                return redirect('/login')
        if 'choosedoc' in request.form:
            return redirect('/test')
        if 'signup' in request.form:
            return redirect('/signup')
        if 'logout' in request.form:
            return redirect('/logout')
        if 'logout2' in request.form:
            return redirect('/')
        if 'signup4' in request.form:
            return redirect('/dctrsignup')
        if 'signup6' in request.form:
            return redirect('/dctrlogin')
        if 'check' in request.form:
            return redirect('/checkin')
        elif 'submit2' in request.form:
            uee = request.form['content3']
            uaa = request.form['content4']
            uuu = request.form['content5']
            haa = request.form['first_name']
            huu = request.form['middle_name']
            hee = request.form['last_name']

            aser = User.query.filter_by(username=uee).first()
            if aser:
                flash("Username Taken")
                return redirect('/signup')
            else:
                if uaa == uuu:
                    hashword = generate_password_hash(uaa, method='sha256')
                    admin_role = Role(name='Patient')
                    new_user = User(username=uee, password=hashword, first_name=haa,
                                    middle_name=huu, last_name=hee, checkin=False)
                    new_user.roles.append(admin_role)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('You were succesfully signed up')
                    return redirect('/login')
                else:
                    flash("Passwords don't match")
                    return redirect('/signup')
        elif 'checkin1' in request.form:
            eoo = request.form['checklog3']
            eii = request.form['checklog4']
            wer = User.query.filter_by(username=eoo).first()
            if wer:
                if check_password_hash(wer.password, eii):
                    der = Role.query.filter_by(id=wer.id).first()
                    if der.name == "Doctor":
                        wer.doctorstatus = True
                        db.session.commit()
                        flash("Status Updated")
                        return redirect('/doctorstatus')
                    else:
                        flash("Account not a doctor")
                        return redirect('/doctorstatus')
                else:
                    flash("Invalid Password")
                    return redirect('/doctorstatus')
            else:
                flash("Invalid username")
                return redirect('/doctorstatus')
        elif 'checkout1' in request.form:
            loo = request.form['checklog3']
            lii = request.form['checklog4']
            fer = User.query.filter_by(username=loo).first()
            if fer:
                if check_password_hash(fer.password, lii):
                    rer = Role.query.filter_by(id=fer.id).first()
                    if rer.name == "Doctor":
                        fer.doctorstatus = False
                        db.session.commit()
                        flash("Status Updated")
                        return redirect('/doctorstatus')
                    else:
                        flash("Account not a doctor")
                        return redirect('/doctorstatus')
                else:
                    flash("Invalid Password")
                    return redirect('/doctorstatus')
            else:
                flash("Invalid username")
                return redirect('/doctorstatus')
        elif 'checkin' in request.form:
            too = request.form['checklog']
            tii = request.form['checklog2']
            ser = User.query.filter_by(username=too).first()
            if ser:
                if check_password_hash(ser.password, tii):
                    mer = Role.query.filter_by(id=ser.id).first()
                    if mer.name == "Doctor":
                        ser.checkin = True
                        waa = str(uuid.uuid4())
                        ser.secret_code = waa
                        db.session.commit()
                        login_user(ser, remember=True)
                        return redirect('/checkin2/' + str(ser.secret_code))
                    else:
                        flash("Account not a doctor")
                        return redirect('/checkin')
                else:
                    flash("Invalid Password")
                    return redirect('/checkin')
            else:
                flash("Invalid username")
                return redirect('/checkin')
        elif 'logout3' in request.form:
            item2 = User.query.filter_by(checkin=True).all()
            tttt2 = int(len(item2)) - 1
            if tttt2 == -1:
                flash("No Doctors Avaliable, please try again later")
                return redirect("/final")
            else:
                return redirect('/symptomcheck')

        elif 'reset' in request.form:
            email_add = request.form['sss']
            db_user = User.query.filter_by(username=email_add).first()
            if db_user:
                db_user.secret_code = str(uuid.uuid4())
                db.session.commit()
                yeeee = db_user.secret_code
                link = "vidveda.com/pwdreset/" + yeeee
                send_mail(email_add, link)
                return redirect('/forgot')
            else:
                return redirect('/forgot')

        elif 'docsubmit2' in request.form:
            aee = request.form['content9']
            aaa = request.form['content6']
            auu = request.form['content7']
            yuu = request.form['first_name2']
            yaa = request.form['middle_name2']
            yee = request.form['last_name2']
            yoo = request.form['secret_key']
            yii = request.form['phone_number']
            if yoo == "4t7w9z$C&F)J@NcRfUjXn2r5u8x/A%D*G-KaPdSgVkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!z%C*F-J@NcRfUjXn2r5u8x/A?D(G+KbPdSgVkYp3s6v9y$B&E)H@McQfThWmZq4t7w!z%C*F-JaNdRgUkXn2r5u8x/A?D(G+KbPeShVmYq3s6v9y$B&E)H@McQfTjWnZr4u7w!z%C*F-JaNdRgUkXp2s5v8y/A?D(G+KbPeShVmYq3t6w9z$C&E)H@McQfTjWnZr4u7x!A%D*G-JaNdRgUkXp2s5v8y/B?E(H+MbPeShVmYq3t6w9z$C&F)J@NcRfTjWnZr4u7x!A%D*G-KaPdSgVkXp2s5v8y/B?E(H+MbQeThWmZq3t6w9z$C&F)J@NcRfUjXn2r5u8x!A%D*G-KaPdSgVkYp3s6v9y$B?E(H+MbQeThWmZq4t7w!z%C*F)J@NcRfUjXn2r5u8x/A?D(G+KaPdSgVkYp3s6v9y$B&E)H@McQeThWmZ":
                hi = User.query.filter_by(username=aee).first()
                if hi:
                    flash("Username Taken")
                    return redirect('/dctrsignup')
                else:
                    if aaa == auu:
                        hshword = generate_password_hash(aaa, method='sha256')
                        bdmin_role = Role(name='Doctor')
                        wew_user = User(username=aee, password=hshword, checkin=False, first_name=yuu,
                                        middle_name=yaa, last_name=yee, phone_number=yii, callstatus=False)
                        wew_user.roles.append(bdmin_role)
                        db.session.add(wew_user)
                        db.session.commit()
                        flash('You were succesfully signed up')
                        return redirect('/checkin')
                    else:
                        flash("Passwords don't match")
                        return redirect('/dctrsignup')
            else:
                flash("Invalid Secret Key")
                return redirect('/dctrsignup')
    if request.method == "GET":
        return render_template('newindex.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/vidcall/<hi787>')
@login_required
def plz(hi787):
    hi787 = hi787
    return render_template('hope.html', plz=hi787)


@app.route('/requestdoc/<id2>', methods=['POST', 'GET'])
@login_required
def requestdoc(id2):
    if request.method == "POST":
        if 'requestdoc' in request.form:
            return render_template('symptomchecker2.html', he=id2)
        if 'symptom_submit2' in request.form:
            bsdvsdv = request.form['symptom_check2']
            otheritem = User.query.filter_by(id=id2).first()
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                    body='The link is: vidveda.com/vidcall/' + str(hi786) + ", the patients name is " + str(
                        current_user.first_name) + " " + str(current_user.last_name) + ", and the symptoms are " + bsdvsdv,
                    from_='+12084233761',
                    to="+" + str(otheritem.phone_number)
                )
        return redirect('/vidcall/' + str(hi786))


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/pwdreset/<hq>', methods=["POST", "GET"])
def pwd(hq):
    if request.method == "POST":
        tttt = request.form['ssss']
        ttttt = request.form['contentss']
        if tttt == ttttt:
            hq = hq
            yryryr = User.query.filter_by(secret_code=hq).first()
            rerrr = generate_password_hash(tttt, method='sha256')
            yryryr.password = rerrr
            yryryr.secret_code = None
            db.session.commit()
            flash("Password Changed")
            return redirect('/login')
        else:
            flash("Password's don't match")
            return redirect('/pwdreset' + str(hq))
    else:
        return render_template('rrrrr.html', uuu=hq)


@app.route('/symptomcheck', methods=["POST", "GET"])
@login_required
def symptomcheck():
    if request.method == 'POST':
        bsdvsdvd = request.form['symptom_check']
        item = User.query.filter_by(checkin=True).all()
        tttttt = int(len(item)) - 1
        r1 = random.randint(0, tttttt)
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body='The link is: vidveda.com/vidcall/' + str(hi786) + ", the patients name is " + str(
                    current_user.first_name) + " " + str(current_user.last_name) + ", and the symptoms are " + bsdvsdvd,
                from_='+12084233761',
                to="+" + str(item[r1].phone_number)
            )
        return redirect('/vidcall/' + str(hi786))
    else:
        return render_template('symptomchecker.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()
