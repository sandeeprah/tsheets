from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from collections import OrderedDict
#from wtforms_alchemy import ModelForm
from application.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

'''
class BaseForm(FlaskForm):
    def __iter__(self):
        field_order = getattr(self, 'field_order', None)
        if field_order:
            temp_fields = []
            for name in field_order:
                if name == '*':
                    temp_fields.extend([f for f in self._unbound_fields if f[0] not in field_order])
                else:
                    temp_fields.append([f for f in self._unbound_fields if f[0] == name][0])
            self._unbound_fields = temp_fields
            self._fields = OrderedDict((k[0], self._fields[k[0]]) for k in self._unbound_fields)
        return super(BaseForm, self).__iter__()
'''

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'already exists, must be unique'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if 'id' in form:
            id = form.id.data
        else:
            id = None

        if check and (id is None or id != check.id):
            raise ValidationError(self.message)

class UserAddForm(FlaskForm):
    id = IntegerField('ID')
    username = TextField('User Name',validators=[DataRequired(), Unique(User, User.username)])
    name = TextField('Full Name',validators=[DataRequired()])
    employee_no = TextField('Employee No.',validators=[DataRequired(), Unique(User, User.employee_no)])
    email = TextField('Email',validators=[DataRequired(), Unique(User, User.email)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


class UserEditForm(FlaskForm):
    id = IntegerField('ID')
    username = TextField('User Name',validators=[DataRequired(), Unique(User, User.username)])
    name = TextField('Full Name',validators=[DataRequired()])
    employee_no = TextField('Employee No.',validators=[DataRequired(), Unique(User, User.employee_no)])
    email = TextField('Email',validators=[DataRequired(), Unique(User, User.email)])

class AdminPasswdChgForm(FlaskForm):
    user_id = SelectField('Employee No',coerce=int)
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


class QueryForm(FlaskForm):
    name = TextField('Item name', validators=[DataRequired()])

class Component(Form):
    id = IntegerField('ID',validators=[DataRequired()])
    name = TextField('Name',validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    price = DecimalField('Price',validators=[DataRequired()], places=2)

class ItemForm(FlaskForm):
    id = IntegerField('ID')
    name = TextField('Name',validators=[DataRequired()])
    description = TextAreaField('Description')
    date = DateField('Date',render_kw={"type":"date"})
    int = IntegerField('An Integer', render_kw={"type":"number","step":1})
    decimal = DecimalField('A Decimal', render_kw={"type":"number","step":0.01 }, places=1)
    file = FileField('A File')
    choices=[('op1', 'Option-1'), ('op2', 'Option-2'), ('op3', 'Option-3')]
    useme = BooleanField('Use Me')
    radio = RadioField('Options', choices=choices, default='op1')
    selection = SelectField('Selection', choices=choices, default='op1')
    components = FieldList(FormField(Component,label='My Component'))
    submit = SubmitField('Edit')
