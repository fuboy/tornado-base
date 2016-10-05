from sqlalchemy import Column, Integer, ForeignKey

from project.core.db import relationship

from project.modules.models import User


# super admin user, can add issuer
class Admin(User):

    def delete_related_obj(self):
        pass

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }