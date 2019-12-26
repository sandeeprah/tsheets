from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from application import app, db
from application.formsTimesheet import ProjectForm, TshtSettingsForm, AssignmentForm
from application.modelsTimesheet import Project, TshtSetting, Assignment
from application.models import User

@app.route('/master-project/')
def masterProject():
    q = Project.query.all()
    return render_template('timesheet/master-project.html', items=q)

@app.route('/detail-project/<int:id>/', methods=['GET', 'POST'])
def detailProject(id):
    error=None
    try:
        q = Project.query.filter_by(id=id).first_or_404()
        form = ProjectForm(obj=q)
        choices = TshtSetting.query.with_entities(TshtSetting.id, TshtSetting.identifier).all()
        form.tsht.choices = choices
        if request.method == 'POST':
            form.tsht.data = int(form.tsht.data)

    except Exception as e:
        error = e
    return render_template('timesheet/detail-project.html', form=form, error=error, mode='view')


def getFormatChoices(current_user):
    if current_user.is_authenticated:
        print('congratulations the user is uthenticated')
    else:
        print('you do not deserve any choices')

    choices = TshtSetting.query.with_entities(TshtSetting.id, TshtSetting.identifier).all()
    return choices

@app.route('/add-project/', methods=['GET', 'POST'])
def addProject():
    error = None
    form = ProjectForm()
    form.tsht.choices = getFormatChoices(current_user)

    if form.validate_on_submit():
        try:
            i = Project()
            form.populate_obj(i)
            print(i.id, i.name, i.tsht)
            db.session.add(i)
            db.session.commit()
            flash('Project added successfully')
            return redirect(url_for('masterProject'))
        except Exception as e:
            db.session.rollback()
            error = e
    return render_template('timesheet/detail-project.html', form=form, error=error, mode='add')

@app.route('/edit-project/<int:id>/', methods=['GET', 'POST'])
def editProject(id):
    error = None
    q = Project.query.filter_by(id=id).first_or_404()
    form = ProjectForm(obj=q)
    choices = TshtSetting.query.with_entities(TshtSetting.id, TshtSetting.identifier).all()
    form.tsht.choices = choices
    if request.method == 'POST':
        form.tsht.data = int(form.tsht.data)

    if form.validate_on_submit():
        try:
            form.populate_obj(q)
            db.session.commit()
            flash('Project updated successfully')
        except Exception as e:
            error = e
    return render_template('timesheet/detail-project.html', form=form, error=error, mode='edit')

@app.route('/delete-project/<int:id>/', methods=['GET', 'POST'])
def deleteProject(id):
    error = None
    q = Project.query.filter_by(id=id).first()
    if q:
        try:
            db.session.delete(q)
            db.session.commit()
            flash("Project deleted successfully")
            return redirect(url_for('masterProject'))
        except Exception as e:
            error = e
    return render_template('timesheet/master-project.html', error=error)



@app.route('/master-tshtsetting/')
def masterTshtSettings():
    q = TshtSetting.query.all()
    return render_template('timesheet/master-tshtsetting.html', items=q)

@app.route('/detail-tshtsetting/<int:id>/', methods=['GET', 'POST'])
def detailTshtSettings(id):
    error=None
    try:
        q = TshtSetting.query.filter_by(id=id).first_or_404()
        form = TshtSettingsForm(obj=q)
    except Exception as e:
        error = e
    return render_template('timesheet/detail-tshtsetting.html', form=form, error=error, mode='view')

@app.route('/add-tshtsetting/', methods=['GET', 'POST'])
def addTshtSettings():
    error = None
    form = TshtSettingsForm()
    if form.validate_on_submit():
        try:
            i = TshtSetting()
            form.populate_obj(i)
            db.session.add(i)
            db.session.commit()
            flash('Time Sheet Format Settings added successfully')
            return redirect(url_for('masterTshtSettings'))
        except Exception as e:
            error = e
    return render_template('timesheet/detail-tshtsetting.html', form=form, error=error, mode='add')

@app.route('/edit-tshtsetting/<int:id>/', methods=['GET', 'POST'])
def editTshtSettings(id):
    error = None
    q = TshtSetting.query.filter_by(id=id).first_or_404()
    form = TshtSettingsForm(obj=q)
    if form.validate_on_submit():
        try:
            form.populate_obj(q)
            db.session.commit()
            flash('Timesheet Format Settings updated successfully')
        except Exception as e:
            error = e
    return render_template('timesheet/detail-tshtsetting.html', form=form, error=error, mode='edit')

@app.route('/delete-tshtsetting/<int:id>/', methods=['GET', 'POST'])
def deleteTshtSettings(id):
    error = None
    q = TshtSetting.query.filter_by(id=id).first()
    if q:
        try:
            db.session.delete(q)
            db.session.commit()
            flash("Timesheet Format Settings deleted successfully")
            return redirect(url_for('masterTshtSettings'))
        except Exception as e:
            error = e
    return render_template('timesheet/master-tshtsetting.html', error=error)


@app.route('/master-assignment/')
def masterAssignment():
    q = Assignment.query.join(Project).order_by(Project.number)
    return render_template('timesheet/master-assignment.html', items=q)


def getProjectChoices():
    choices = Project.query.with_entities(Project.id, Project.name).all()
    return choices

def getUserChoices():
    choices = User.query.with_entities(User.id, User.employee_no).all()
    return choices


@app.route('/detail-assignment/<int:id>/', methods=['GET', 'POST'])
def detailAssignment(id):
    error=None
    try:
        q = Assignment.query.filter_by(id=id).first_or_404()
        form = AssignmentForm(obj=q)
        form.project_id.choices = getProjectChoices()
        form.user_id.choices = getUserChoices()
    except Exception as e:
        error = e
    return render_template('timesheet/detail-assignment.html', form=form, error=error, mode='view')

@app.route('/add-assignment/', methods=['GET', 'POST'])
def addAssignment():
    error = None
    form = AssignmentForm()
    form.project_id.choices = getProjectChoices()
    form.user_id.choices = getUserChoices()
    if form.validate_on_submit():
        try:
            i = Assignment()
            form.populate_obj(i)
            db.session.add(i)
            db.session.commit()
            flash('Assignment added successfully')
            return redirect(url_for('masterAssignment'))
        except Exception as e:
            error = e
    return render_template('timesheet/detail-assignment.html', form=form, error=error, mode='add')

@app.route('/edit-assignment/<int:id>/', methods=['GET', 'POST'])
def editAssignment(id):
    error = None
    q = Assignment.query.filter_by(id=id).first_or_404()
    form = AssignmentForm(obj=q)
    form.project_id.choices = getProjectChoices()
    form.user_id.choices = getUserChoices()
    if form.validate_on_submit():
        try:
            form.populate_obj(q)
            db.session.commit()
            flash('Assignment updated successfully')
        except Exception as e:
            error = e
    return render_template('timesheet/detail-assignment.html', form=form, error=error, mode='edit')

@app.route('/delete-assignment/<int:id>/', methods=['GET', 'POST'])
def deleteAssignment(id):
    error = None
    q = Assignment.query.filter_by(id=id).first()
    if q:
        try:
            db.session.delete(q)
            db.session.commit()
            flash("Assignment deleted successfully")
            return redirect(url_for('masterAssignment'))
        except Exception as e:
            error = e
    return render_template('timesheet/master-assignment.html', error=error)



@app.route('/prjselect-timesheet/', methods=['GET', 'POST'])
def prjSelectTimesheet():
    error = None
    q = Assignment.query.filter_by(id=id).first_or_404()
    form = ProjectSelectForm(obj=q)
    form.project_id.choices = getProjectChoices()
    if form.validate_on_submit():
        try:
            form.populate_obj(q)
            db.session.commit()
            flash('Assignment updated successfully')
        except Exception as e:
            error = e
    return render_template('timesheet/detail-assignment.html', form=form, error=error, mode='edit')
