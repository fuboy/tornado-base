from wtforms.validators import Email, EqualTo, IPAddress, MacAddress, Length, \
    NumberRange, Optional, Required, InputRequired, DataRequired, Regexp, URL, AnyOf, NoneOf, ValidationError


from project.ext.utility import correct_phone


class ValidatePhoneNumber(object):
    def __init__(self, message=None):
        if not message:
            message = u'Phone number is wrong, must be like 9337825098 or 09337825098'
        self.message = message

    def __call__(self, form, field):
        data = correct_phone(field.data)

        field.data = data

        # raise ValidationError(self.message)
