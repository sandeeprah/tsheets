from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from application import app, db
from application.formsTimesheet import ProjectForm, TshtSettingsForm, AssignmentForm
from application.modelsTimesheet import Project, TshtSetting, Assignment


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
    except Exception as e:
        error = e
    return render_template('timesheet/detail-project.html', form=form, error=error, mode='view')

@app.route('/add-project/', methods=['GET', 'POST'])
def addProject():
    error = None
    form = ProjectForm()
    if form.validate_on_submit():
        try:
            i = Project()
            form.populate_obj(i)
            db.session.add(i)
            db.session.commit()
            flash('Project added successfully')
            return redirect(url_for('masterProject'))
        except Exception as e:
            error = e
    return render_template('timesheet/detail-project.html', form=form, error=error, mode='add')

@app.route('/edit-project/<int:id>/', methods=['GET', 'POST'])
def editProject(id):
    error = None
    q = Project.query.filter_by(id=id).first_or_404()
    form = ProjectForm(obj=q)
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
    q = Assignment.query.all()
    return render_template('timesheet/master-assignment.html', items=q)

@app.route('/detail-assignment/<int:id>/', methods=['GET', 'POST'])
def detailAssignment(id):
    error=None
    try:
        q = Assignment.query.filter_by(id=id).first_or_404()
        form = AssignmentForm(obj=q)
    except Exception as e:
        error = e
    return render_template('timesheet/detail-assignment.html', form=form, error=error, mode='view')

@app.route('/add-assignment/', methods=['GET', 'POST'])
def addAssignment():
    error = None
    form = AssignmentForm()
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
