from sqlalchemy import Column, String, Boolean, or_, Unicode, ForeignKey
from sqlalchemy_utils import IPAddressType, PasswordType, PhoneNumberType, EmailType

from sqlalchemy.dialects.postgres import ENUM

from .constants import Constants
from project.core.db import TorModel, relationship, Integer, UUIDType
from project.core.wtforms.validators import EqualTo, ValidatePhoneNumber


class User(TorModel):
    __tablename__ = 'users'

    email = Column(EmailType(120), unique=True, nullable=False)

    first_name = Column(Unicode(25), nullable=False)
    last_name = Column(Unicode(25), nullable=False)

    phone = Column(String(15))  # PhoneNumberType

    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']
    ), info={'validators': []}, nullable=False)

    last_ip = Column(IPAddressType())

    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @classmethod
    def get_by_username(cls, username):
        if not username:
            return None

        return cls.query.filter(cls.username == username).first()

    @classmethod
    def get_by_email(cls, email):
        if not email:
            return None

        return cls.query.filter(cls.email == email).first()

    @classmethod
    def get_by_phone(cls, phone):
        if not phone:
            return None

        return cls.query.filter(cls.phone == phone).first()
