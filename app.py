import os
import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
dbpath = 'ad.db'
app = Flask(__name__)
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(
    basedir, 'database.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/')
@app.route('/home')
def index():
    data = datetime.datetime.now().year
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
        "year": datetime_now.year,
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_SERVER_PORT', 5000))
