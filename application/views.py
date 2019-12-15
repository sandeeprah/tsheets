from flask import request, render_template, jsonify, abort, make_response, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField

from application import app, db
from application.forms import LoginForm, RegistrationForm, EditProfileForm, ItemForm, QueryForm, UserForm
from application.models import User, Item

import application.viewsTimesheet

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

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

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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
    return render_template('edit_profile.html', title='Edit Profile',form=form)


@app.route('/master-user/', methods=['GET', 'POST'])
def masterUser():
    q = User.query.all()
    return render_template('master-user.html', items=q)

@app.route('/detail-user/<int:id>/', methods=['GET', 'POST'])
def detailUser(id):
    error=None
    try:
        q = User.query.filter_by(id=id).first_or_404()
        form = UserForm(obj=q)
    except Exception as e:
        error = e
    return render_template('detail-user.html', form=form, error=error, mode='view')

@app.route('/add-user/', methods=['GET', 'POST'])
def addUser():
    error = None
    form = UserForm()
    if form.validate_on_submit():
        try:
            i = User()
            form.populate_obj(i)
            db.session.add(i)
            db.session.commit()
            flash('User added successfully')
            return redirect(url_for('masterUser'))
        except Exception as e:
            error = e
    return render_template('detail-user.html', form=form, error=error, mode='add')

@app.route('/edit-user/<int:id>/', methods=['GET', 'POST'])
def editUser(id):
    error = None
    q = User.query.filter_by(id=id).first_or_404()
    form = UserForm(obj=q)
    if form.validate_on_submit():
        try:
            form.populate_obj(q)
            db.session.commit()
            flash('User updated successfully')
        except Exception as e:
            error = e
    return render_template('detail-user.html', form=form, error=error, mode='edit')


@app.route('/delete-user/<int:id>/', methods=['GET', 'POST'])
def deleteUser(id):
    error = None
    q = User.query.filter_by(id=id).first()
    if q:
        try:
            db.session.delete(q)
            db.session.commit()
            flash("User deleted successfully")
            return redirect(url_for('masterUser'))
        except Exception as e:
            error = e
    return render_template('master-user.html', error=error)


@app.route('/master-item/')
def masterItem():
    q = Item.query.all()
    return render_template('master-item.html', items=q)

@app.route('/detail-item/<int:id>/', methods=['GET', 'POST'])
def detailItem(id):
    error=None
    try:
        q = Item.query.filter_by(id=id).first_or_404()
        form = ItemForm(obj=q)
    except Exception as e:
        error = e
    return render_template('detail-item.html', form=form, error=error, mode='view')

@app.route('/query-item/', methods=['GET', 'POST'])
def query_item():
    error = None
    form = QueryForm()
    if form.validate_on_submit():
        q = Item.query.filter_by(name=form.name.data).all()
        if q:
            return render_template('query-item.html', form=form, items=q)
        else:
            error = "No items"
    return render_template('query-item.html', form=form, error=error)

@app.route('/add-item/', methods=['GET', 'POST'])
def addItem():
    error = None
    form = ItemForm()
    if form.validate_on_submit():
        try:
            i = Item()
            form.populate_obj(i)
            db.session.add(i)
            db.session.commit()
            flash('Item added successfully')
            return redirect(url_for('masterItem'))
        except Exception as e:
            error = e
    return render_template('detail-item.html', form=form, error=error, mode='add')

@app.route('/edit-item/<int:id>/', methods=['GET', 'POST'])
def editItem(id):
    error = None
    q = Item.query.filter_by(id=id).first_or_404()
    form = ItemForm(obj=q)
    if form.validate_on_submit():
        try:
            form.populate_obj(q)
            db.session.commit()
            flash('Item updated successfully')
        except Exception as e:
            error = e
    return render_template('detail-item.html', form=form, error=error, mode='edit')

@app.route('/delete-item/<int:id>/', methods=['GET', 'POST'])
def deleteItem(id):
    error = None
    q = Item.query.filter_by(id=id).first()
    if q:
        try:
            db.session.delete(q)
            db.session.commit()
            flash("Item deleted successfully")
            return redirect(url_for('masterItem'))
        except Exception as e:
            error = e
    return render_template('master-item.html', error=error)


@app.route('/project/', methods=['GET', 'POST'])
def project():
    form = ProjectForm(request.form, meta={'id':'form1'})
    form.submit = SubmitField('submit')
    if request.method == "POST" and form.validate():
        flash('Your Project has been saved.')
        return redirect(url_for('index'))
    return render_template('project.html', title='Project',
                           form=form)


@app.route('/timesheet/')
def timesheet():
    user = {'username': 'sandeep'}
    project = 'Enoc'
    settings = {
    "wla" : True,
    "wla_title" : "Work Location A",
    "wla_codes" : True,

    "wlb" : True,
    "wlb_title" : "Work Location A",
    "wlb_codes" : True,

    "lv" : True,
    "lv_title" : "Work Location A",
    "lv_codes" : True,

    "tra" : True,
    "tra_title" : "Work Location A",
    "tra_codes" : True,

    "trb" : False,
    "trb_title" : "Work Location A",
    "trb_codes" : True,

    "ot" : True,
    "ot_title" : "Work Location A",
    "ot_codes" : True,
    }
    days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    return render_template("timesheet.html", user=user, project=project, days = days, settings = settings)
