import datetime
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, url_for, g
from flask import session, app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import (LoginManager, UserMixin, fresh_login_required,
                         login_user, logout_user, current_user)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from forms import LoginForm, PostForm, ProfileForm

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get("SECRET_KEY")
UPLOAD_FOLDER = 'static/photo/post/'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(
    basedir, 'database.db'))
app.config['SECRET_KEY'] = SECRET_KEY
app.config['COOKIE_SECURE'] = 'Secure'
app.config['COOKIE_DURATION'] = timedelta(minutes=30)
app.debug = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 5000
db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Administration Panel', template_mode='bootstrap3')

login_manager = LoginManager(app)





class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    UniqueConstraint("login", "phone", name="uix_1")
    db.relationship('Post', backref='post')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(1000), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author = db.Column(db.Integer(), db.ForeignKey(User.id))
    image = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return '<Ad %r>' % self.id



class ProtectedModelView(ModelView):
    """Проверка авторизации в админке."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin.add_view(ProtectedModelView(User, db.session))
admin.add_view(ProtectedModelView(Post, db.session))


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


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


@app.route('/posts', methods=['GET'])
def get_posts():
    form = PostForm()
    posts_new = Post.query.order_by(Post.date.desc()).all()
    return render_template('posts.html', posts_new=posts_new, form=form)


@app.route('/posts', methods=['POST'])
@fresh_login_required
def add_posts():
    if request.method == 'POST':
        if request.files['file1']:
            file1 = request.files['file1']
            path = os.path.join(app.config['UPLOAD_FOLDER'],
                                secure_filename(file1.filename))
            file1.save(path)
        else:
            path = ''
        title = request.form['title']
        text = request.form['text']
        phone = request.form['phone']
        author_id = current_user.id
        image = path

        post = Post(title=title, phone=phone, text=text, author=author_id,
                    image=image)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')

        except Exception.OperationalError:
            raise 'Ошибка записи в БД.'
    else:
        return 'Ошибка валидации.'


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    post = Post.query.get_or_404(id)
    file = post.image
    try:
        if file != '':
            os.remove(file)
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except Exception:
        raise 'Ошибка записи в БД.'
        return redirect('/posts')


@app.context_processor
def year():
    datetime_now = datetime.datetime.now()
    return {
        'year': datetime_now.year,
    }


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    phone = request.form.get('phone')
    password = request.form.get('password')

    if password and phone:
        user = User.query.filter_by(phone=phone).first()
        if (user and user.password and phone and check_password_hash(
                user.password,
                password)):
            login_user(user)
            flash('Logged in successfully.')
            return redirect('/posts')
        else:
            flash('Некорректный логин или пароль')
    else:
        flash('Заполните логин или пароль')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    first_name = request.form.get('first_name')
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    phone = request.form.get('phone')
    if request.method == 'POST':
        if not (first_name or login or password or password2 or phone):
            flash('Заполните все поля для регистрации.')
        elif password != password2:
            flash('Пароли не совпадают.')
        else:
            hash = generate_password_hash(password)
            new_user = User(
                first_name=first_name,
                login=login,
                password=hash,
                phone=phone
            )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        except Exception as e:
            flash('Пользователь с указанным номером уже зарегистрирован. '
                  'Пожалуйста используйте другой номер.')
            return render_template('signup.html')
        return render_template('login.html')

    else:
        flash('Заполните форму.')
    return render_template('signup.html')


@app.route('/profile', methods=['GET', 'POST'])
@fresh_login_required
def profile():
    g.user = current_user
    user = g.user.id
    user = User.query.get_or_404(user)
    form = ProfileForm(obj=user)
    if request.method == 'POST' and form.validate():
        g.user.phone = request.form.get('phone')
        g.user.login = request.form.get('login')
        g.user.first_name = request.form.get('first_name')
        try:
            db.session.add(g.user)
            db.session.commit()
            return redirect(url_for('profile'))

        except Exception as e:
            flash('Данные не обновлены.')
            return render_template('login.html')
        return render_template('profile.html', form=form)

    flash('Заполните форму.')
    return render_template('profile.html', form=form, user=user)


@app.route('/change_auth', methods=['GET', 'POST'])
@fresh_login_required
def change_auth():
    g.user = current_user
    user = g.user.id
    user = User.query.get_or_404(user)
    form = ProfileForm(obj=user)
    if request.method == 'POST' and form.validate():
        new_password = request.form.get('new_password')
        new_password2 = request.form.get('new_password2')
        old_password = request.form.get('old_password')
        if not (new_password or new_password2 or old_password):
            flash('Заполните все поля.')
        elif new_password != new_password2:
            flash('Пароли не совпадают.')
        elif not check_password_hash(user.password, old_password):
            flash('Введен неправильный пароль.')
        else:
            g.user.password = generate_password_hash(new_password)
            try:
                db.session.add(g.user)
                db.session.commit()
                flash('Пароль успешно изменен.')
                return redirect(url_for('profile'))

            except Exception as e:
                flash('Данные не обновлены.')
                return render_template('login.html')
            return render_template('change_auth.html', form=form)

    flash('Заполните форму.')
    return render_template('change_auth.html', form=form, user=user)



@app.route("/logout")
@fresh_login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    else:
        return response


# @app.context_processor
# def weather():
#     town = 'Сёла'
#
#     url = ('https://api.openweathermap.org/data/2.5/weather?q=' + town +
#            '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347')
#
#     weather_data = requests.get(url).json()
#
#     temperature = round(weather_data['main']['temp'])
#     temperature_feels = round(weather_data['main']['feels_like'])
#
#     return {
#         'temperature': temperature,
#         'feels_like': temperature_feels,
#     }
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=os.environ.get('FLASK_SERVER_PORT', 5050),
 #       static_folder='static'
    )
