import os

import requests
import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, \
    UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash


from forms import LoginForm, PostForm

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
dbpath = 'ad.db'
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(
    basedir, 'database.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = SECRET_KEY


db = SQLAlchemy(app)
login_manager = LoginManager(app)


class Posts(db.Model):
    __tablename__ = 'Ad'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(1000), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Ad %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    UniqueConstraint("login", "phone", name="uix_1")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/entertainments')
def entertainments():
    return render_template('entertainments.html')


@app.route('/base_contact')
def base_contact():
    return render_template('base_contact.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        phone = request.form['phone']
        post = Posts(title=title, phone=phone, text=text, name='admin')
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('posts')

        except Exception as e:
            return e

    else:
        posts_new = Posts.query.order_by(Posts.date.desc()).all()
        return render_template('posts.html', posts_new=posts_new)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    post = Posts.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except Exception as e:
        return e


@app.context_processor
def year():
    datetime_now = datetime.datetime.now()
    return {
        'year': datetime_now.year,
    }


@app.context_processor
def weather():
    town = 'Сёла'

    url = ('https://api.openweathermap.org/data/2.5/weather?q=' + town +
          '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347')

    weather_data = requests.get(url).json()

    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])

    return {
        'temperature': temperature,
        'feels_like': temperature_feels,
    }


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login = request.form.get('login')
#     password = request.form.get('password')
#     phone = request.form.get('phone')
#     if login and password and phone:
#         user = User.query.filter_by(phone=phone).first()
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             next_page = request.args.get('next')
#             redirect(next_page)
#         else:
#             flash('Некорректный логин или пароль')
#     else:
#         flash('Заполните логин или пароль')
#         return render_template('login.html')
#
#
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     first_name = request.form.get('first_name')
#     login = request.form.get('login')
#     password = request.form.get('password')
#     password2 = request.form.get('password2')
#     phone = request.form.get('phone')
#     if request.method == 'POST':
#         if not (first_name or login or password or password2 or phone):
#             flash('Заполните все поля для регистрации.')
#         elif password != password2:
#             flash('Пароли не совпадают.')
#         else:
#             hash = generate_password_hash(password)
#             new_user = User(
#                 first_name=first_name,
#                 login=login,
#                 password=hash,
#                 phone=phone
#             )
#             try:
#                 db.session.add(new_user)
#                 db.session.commit()
#                 return redirect(url_for('login.html'))
#
#             except Exception as e:
#                 return e
#
#             return render_template('login.html')
#     return render_template('signup.html')
#
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login.html'))
#
#
# @app.after_request
# def redirect_to_signin(response):
#     if response.status_code == 401:
#         return redirect(url_for('login.html') + '?next=' + request.url)
#     else:
#         return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_SERVER_PORT', 5050))

