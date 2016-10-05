from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgres import ENUM

from sqlalchemy_utils import generic_relationship

from .constants import Constants
from project.core.db import TorModel, UUIDType

MESSAGE_TYPE_ENUM = ENUM(Constants.MESSAGE_TYPES, name='message_type_enum')


### auto_generate_support ###
class Log(TorModel):
    __tablename__ = 'logs'

    ### others ###
    ### END_OTHERS ###

    # acl[*] # default
    object_id = Column(UUIDType(binary=False))
    # acl[*] # default
    object_type = Column(String(50))

    # acl[*] # default
    object = generic_relationship(object_type, object_id)

    # acl[*] # default
    message_type = Column(MESSAGE_TYPE_ENUM, default=Constants.MESSAGE_TYPE_INFO, nullable=False)
    # acl[*] # default
    message = Column(String)

    def delete_related_obj(self):
        pass

    # auto generate
    @classmethod
    def acl(cls):
        return {
            'object': ['admin', 'client'],
            'created_at': ['admin', 'client'],
            'object_type': ['admin', 'client'],
            'updated_at': ['admin', 'client'],
            'object_id': ['admin', 'client'],
            'message': ['admin', 'client'],
            'message_type': ['admin', 'client'],
            'id': ['admin', 'client'],
        }

    @classmethod
    def user_acl(cls):
        return {
            'admin': ['object_id', 'object_type', 'object', 'message_type', 'message', 'id', 'created_at', 'updated_at'],
            'client': ['object_id', 'object_type', 'object', 'message_type', 'message', 'id', 'created_at', 'updated_at'],
        }

    @classmethod
    def dft_view(cls):
        return {
            'object': 'object',
            'created_at': 'created_at',
            'object_type': 'object_type',
            'updated_at': 'updated_at',
            'object_id': 'object_id',
            'message': 'message',
            'message_type': 'message_type',
            'id': 'id',
        }
    # end auto generate
