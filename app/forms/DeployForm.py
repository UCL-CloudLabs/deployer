from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class DeployForm(FlaskForm):
    vm_name = StringField('VM name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
