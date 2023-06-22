import datetime

from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
