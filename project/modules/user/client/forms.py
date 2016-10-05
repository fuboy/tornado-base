from project.core.wtforms.form import TorForm, SelectField
from project.core.wtforms.validators import DataRequired


from .models import Client


class CreateClientForm(TorForm):
    class Meta:
        model = Client
        only = ['email', 'first_name', 'last_name', 'phone', 'password',]


class UpdateClientForm(TorForm):
    class Meta:
        model = Client
        only = ['first_name', 'last_name', 'phone', 'password',]