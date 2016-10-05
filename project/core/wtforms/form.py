from wtforms import Form, StringField, FloatField, DateField, DateTimeField, IntegerField, \
    HiddenField, PasswordField, RadioField, DecimalField, \
    SubmitField, BooleanField, TextAreaField, SelectField, FormField, FieldList

from wtforms_alchemy import model_form_factory, ModelFormField, ModelFieldList


# used wtforms-sqlalchemy lib  - link: https://wtforms-alchemy.readthedocs.io
ModelForm = model_form_factory(Form)
"""
.. _WTForms: http://wtforms.simplecodes.com/
A simple wrapper for WTForms_.
Basically we only need to map the request handler's `arguments` to the
`wtforms.form.Form` input. Quick example::
    from wtforms import TextField, validators
    from tornadotools.forms import Form
    class SampleForm(Form):
        username = TextField('Username', [
            validators.Length(min=4, message="Too short")
            ])
        email = TextField('Email', [
            validators.Length(min=4, message="Not a valid mail address"),
            validators.Email()
            ])
Then, in the `RequestHandler`::
    def get(self):
        form = SampleForm(self)
        if form.validate():
            # do something with form.username or form.email
            pass
        self.render('template.html', form=form)



"""

"""
class User(Base):
    __tablename__ = 'user'

    name = sa.Column(sa.Unicode(100), primary_key=True, nullable=False)
    color = sa.Column(
        sa.String(7),
        info={'form_field_class': ColorField},
        nullable=False
    )

class UserForm(ModelForm):
    class Meta:
        model = User
"""


class TorForm(ModelForm):
    class Meta:
        pass

    submit = SubmitField('submit')

    @classmethod
    def get_session(cls):
        from project.core.db import db
        # this method should return sqlalchemy session
        return db.session
    """
    `WTForms` wrapper for Tornado.
    """

    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        """
        Wrap the `formdata` with the `TornadoInputWrapper` and call the base
        constuctor.
        """
        self._handler = formdata
        super(TorForm, self).__init__(formdata=TornadoInputWrapper(formdata), obj=obj,
                                       prefix=prefix, data=data, meta=meta, **kwargs)

    # def _get_translations(self):
    #     return TornadoLocaleWrapper(self._handler.get_user_locale())


class TornadoInputWrapper(object):
    def __init__(self, handler):
        self._handler = handler

    def __iter__(self):
        return iter(self._handler.request.arguments)

    def __len__(self):
        return len(self._handler.request.arguments)

    def __contains__(self, name):
        return (name in self._handler.request.arguments)

    def getlist(self, name):
        return self._handler.get_arguments(name)


class TornadoLocaleWrapper(object):
    def __init__(self, locale):
        self.locale = locale

    def gettext(self, message):
        return self.locale.translate(message)

    def ngettext(self, message, plural_message, count):
        return self.locale.translate(message, plural_message, count)