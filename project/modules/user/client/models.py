from project.core.db import relationship, Column, Integer, ForeignKey

from project.core.db import UUIDType
from project.modules.models import User


### auto_generate_support ###
class Client(User):
    ### others ###
    ### email: acl[*] # default
    ### first_name: acl[*] # default
    ### last_name: acl[*] # default
    ### phone: acl[*] # default
    ### type: acl[*] # default
    ### full_name: acl[*] # default
    ### END_OTHERS ###

    __mapper_args__ = {
        'polymorphic_identity': 'client',
    }

    def delete_related_obj(self):
        pass

    # auto generate
    @classmethod
    def acl(cls):
        return {
            'first_name': ['admin', 'client'],
            'last_name': ['admin', 'client'],
            'created_at': ['admin', 'client'],
            'updated_at': ['admin', 'client'],
            'id': ['admin', 'client'],
            'phone': ['admin', 'client'],
            'full_name': ['admin', 'client'],
            'type': ['admin', 'client'],
            'email': ['admin', 'client'],
        }

    @classmethod
    def user_acl(cls):
        return {
            'admin': ['email', 'first_name', 'last_name', 'phone', 'type', 'full_name', 'id', 'created_at', 'updated_at'],
            'client': ['email', 'first_name', 'last_name', 'phone', 'type', 'full_name', 'id', 'created_at', 'updated_at'],
        }

    @classmethod
    def dft_view(cls):
        return {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'created_at': 'created_at',
            'updated_at': 'updated_at',
            'id': 'id',
            'phone': 'phone',
            'full_name': 'full_name',
            'type': 'type',
            'email': 'email',
        }
    # end auto generate
