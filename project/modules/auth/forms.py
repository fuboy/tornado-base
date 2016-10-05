from project.core.wtforms.form import TorForm, StringField, PasswordField
from project.core.wtforms.validators import DataRequired, Length

from project.modules.user.models import User


class LoginForm(TorForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])