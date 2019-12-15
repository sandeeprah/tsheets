from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class ProjectForm(FlaskForm):
    id = IntegerField('ID')
    number = TextField('Project Number',validators=[DataRequired()])
    name = TextField('Project Name',validators=[DataRequired()])
    tsht = TextField('Time Sheet Format',validators=[DataRequired()])

class AssignmentForm(FlaskForm):
    id = IntegerField('ID')
    project_id = TextField('Project ID',validators=[DataRequired()])
    user_id = TextField('User ID',validators=[DataRequired()])
    rate = DecimalField('Contracted Rate',validators=[DataRequired()])
    currency = TextField('Currency Rate',validators=[DataRequired()])
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
