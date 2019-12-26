from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_login import current_user

#from application.modelsTimesheet import Project, TshtSetting, Assignment
from application.modelsTimesheet import TshtSetting


class ProjectForm(FlaskForm):
    id = IntegerField('ID')
    number = TextField('Project Number',validators=[DataRequired()])
    name = TextField('Project Name',validators=[DataRequired()])
    tsht = SelectField('Time Sheet Format',coerce=int)


class AssignmentForm(FlaskForm):
    id = IntegerField('ID')
    #tsht = SelectField('Time Sheet Format',coerce=int)

    project_id = SelectField('Project ID',validators=[DataRequired()], coerce=int)
    user_id = SelectField('User ID',validators=[DataRequired()], coerce=int)
    rate = DecimalField('Contracted Rate',validators=[DataRequired()])
    currency = TextField('Currency',validators=[DataRequired()])
    rate_basis = TextField('Rate Basis',validators=[DataRequired()])



class TshtSettingsForm(FlaskForm):
    id = IntegerField('ID')
    identifier = TextField('Format Identifier',validators=[DataRequired()])
    description = TextAreaField('Format Description',validators=[DataRequired()])

    act_code_enable = BooleanField('Enable Activity Codes')
    act_title = TextField('Activity Code Column Title')

    wla_hrs_enable = BooleanField('Enable Work Location-A')
    wla_code_enable = BooleanField('Enable Work Location-A Codes')
    wla_title = TextField('Work Location-A  Column Title')

    wlb_hrs_enable = BooleanField('Enable Work Location-B')
    wlb_code_enable = BooleanField('Enable Work Location-B Codes')
    wlb_title = TextField('Work Location-B  Column Title')

    lv_hrs_enable = BooleanField('Enable Leave Column')
    lv_code_enable = BooleanField('Enable Leave Codes')
    lv_title = TextField('Leave Column Title')

    tra_hrs_enable = BooleanField('Enable Travel-A')
    tra_code_enable = BooleanField('Enable Travel-A Codes')
    tra_title = TextField('Travel-A  Column Title')

    trb_hrs_enable = BooleanField('Enable Travel-B')
    trb_code_enable = BooleanField('Enable Travel-B Codes')
    trb_title = TextField('Travel-B  Column Title')

    ot_hrs_enable = BooleanField('Enable Overtime')
    ot_code_enable = BooleanField('Enable Overtime Codes')
    ot_title = TextField('Overtime  Column Title')

    remarks_enable = BooleanField('Enable Remarks')
    remarks_title = TextField('Remarks Column Title')
