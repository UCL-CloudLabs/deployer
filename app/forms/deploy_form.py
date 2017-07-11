from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeployForm(FlaskForm):
    name = StringField('Host name', validators=[DataRequired()])
    dnsname = StringField('Domain prefix', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    passwd = StringField('Password', validators=[])
    public_key = StringField('Public key', validators=[])
    private_key_path = StringField('Path to private key', validators=[])
