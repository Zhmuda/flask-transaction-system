from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL

class UserForm(FlaskForm):
    balance = FloatField('Balance', validators=[DataRequired()])
    commission_rate = FloatField('Commission Rate', validators=[DataRequired()])
    webhook_url = StringField('Webhook URL', validators=[URL()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Save')
