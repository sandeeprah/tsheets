from flask import request, render_template, jsonify, abort, make_response, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from application import app, db
from application.forms import LoginForm, RegistrationForm, EditProfileForm
from application.models import User


@app.route('/')
@app.route('/index/')
@login_required
def index():
    user = {'username': 'Sandeep'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", user=user, posts=posts)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

'''

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/admin/')
def admin():
    return render_template("admin.html")

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/google5ca5209499debead.html')
def google_verify():
    return render_template("google5ca5209499debead.html")

@app.route('/sitemap.xml')
def google_sitemap():
    template = render_template('sitemap.xml')
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def google_robots():
    template = render_template('robots.txt')
    response = make_response(template)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/forgot/', methods=['GET'])
def forgot_password():
    return render_template("forgot_password.html")

@app.route('/register/', methods=['GET'])
def register_user():
    return render_template("register.html")

@app.route('/profile/', methods=['GET'])
def profile_user():
    return render_template("profile.html")

@app.route('/indexlogin/', methods=['GET'])
def index_user():
    return render_template("indexlogin.html")
'''