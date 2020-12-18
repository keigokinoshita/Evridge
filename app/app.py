from flask import Flask,render_template,request,flash,redirect,abort,url_for
from flask_wtf import FlaskForm
from model.models import User,Event
from model.database import db_session
from app import key
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from wtforms import TextField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import EmailField,DateField
from wtforms.validators import InputRequired,DataRequired,Email,Optional
from flask_wtf.csrf import CSRFProtect
from hashlib import sha256
import os
from werkzeug.utils import secure_filename

#Flaskオブジェクトの生成
app = Flask(__name__)

app.secret_key = b'\xabc3\x9f\xa8\xbc\xb6\xb5\xcauy\xc9\x8e\xc7\x9e!\xefo\x99}\x1c\x80\x0f\x1f'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

csrf = CSRFProtect(app)

ALLOWED_EXTENSIONS = set(['pdf','png', 'jpg', 'jpeg','gif','HEIC'])
UPLOAD_FOLDER = 'app/static/image/'
app.config.UPLOAD_FOLDER = UPLOAD_FOLDER
app.config.MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4MB max-limit.

@login_manager.user_loader 
def load_user(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    return user

@app.route("/")
@app.route("/index")
def index():
    #以下を変更
    all_event = Event.query.all()
    status = request.args.get("status")
    return render_template("index.html",all_event=all_event,status=status)

class LoginForm(FlaskForm):
    user_id = TextField('user_id', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class UserRegisterForm(FlaskForm):
    user_id = TextField('user_id', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    address = EmailField('address', [DataRequired(), Email()])
    tel = TextField('tel', validators=[DataRequired()])

class EventRegisterForm(FlaskForm):
    img = FileField('img', validators=[Optional(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg','gif','HEIC'])])
    host = TextField('host', validators=[DataRequired()])
    title = TextField('title', validators=[DataRequired()])
    date = DateField('date',format='%Y/%m/%d',validators=[DataRequired()])
    place = TextField('place',validators=[DataRequired()])
    address = EmailField('address', validators=[DataRequired(), Email()])
    tel = TextField('tel', validators=[DataRequired()])
    body = TextField('body', validators=[Optional()])
    url = TextField('url', validators=[Optional()])

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    status = request.args.get("status")
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        password = sha256((form.user_id.data + form.password.data + key.SALT).encode("utf-8")).hexdigest()
        if user:
            if password == user.hashed_password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login',status="wrong_input"))
        else:
            return redirect(url_for('login',status="user_notfound"))
    return render_template("login.html",status=status)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index',status="logout"))

@app.route('/user_register', methods=['GET','POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if user:
            return redirect(url_for("user_register",status="exist_user"))
        else:
            hashed_password = sha256((form.user_id.data + form.password.data + key.SALT).encode("utf-8")).hexdigest()
            user = User(form.user_id.data,form.address.data,form.tel.data, hashed_password)
            db_session.add(user)
            db_session.commit()
            login_user(user)
            return redirect(url_for("index"))
    return render_template("user_register.html")

@app.route('/event_register',methods=['GET','POST'])
@login_required
def event_register():
    form = EventRegisterForm()
    if form.validate_on_submit():
        if form.img.data:
            img = form.img.data
            filename = secure_filename(img.filename)
            img_url = os.path.join(app.config.UPLOAD_FOLDER, filename)
            img.save(img_url)

            img_path = "../static/image/"+filename
            event = Event(current_user.user_id,img_path,form.host.data,form.address.data,form.tel.data,\
                                form.title.data,form.date.data,form.place.data,form.body.data,form.url.data,0)
        else:
            img_path = None
            event = Event(current_user.user_id,img_path,form.host.data,form.address.data,form.tel.data,\
                                form.title.data,form.date.data,form.place.data,form.body.data,form.url.data,0)

        db_session.add(event)
        db_session.commit()
        
        return render_template("event_register.html",status="success",form=form,filename=img_path)
    return render_template("event_register.html",status="fail",form=form)

if __name__ == "__main__":
    app.run(debug=True)