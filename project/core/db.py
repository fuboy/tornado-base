from datetime import datetime

from sqlalchemy_utils import UUIDType
import uuid

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Integer, String, and_, or_, desc
from sqlalchemy_utils import generic_relationship

from sqlalchemy.dialects.postgres import JSONB

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from project.ext.utility import add_be_af
from project.core.pagination import Pagination


__all__ = ['db', 'TorModel']


class DB(object):
    pass


class BaseModel(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = declarative_base()

        return cls._instance


# MIXIN
class Model(object):
    @classmethod
    def get_new_query(cls, query, q_params, user_type):
        # add_be_af(q_params, '1')
        if q_params:
            for key, value in q_params.iteritems():
                operator = 'equal'
                if key.startswith('__not__'):
                    operator = 'not_equal'
                    key = key.split('__not__')[1]
                elif key.startswith('__g_than__'):
                    operator = 'greater_than'
                    key = key.split('__g_than__')[1]
                elif key.startswith('__s_than__'):
                    operator = 'smaller_than'
                    key = key.split('__s_than__')[1]
                elif key.startswith('__like__'):
                    operator = 'like'
                    key = key.split('__like__')[1]

                if (not hasattr(cls, key)) or \
                        (key not in cls.user_acl()[user_type]):
                    continue

                attr = getattr(cls, key)
                l = len(value)
                if operator == 'equal':
                    if l > 1:
                        query = query.filter(attr.in_(value))
                    elif l > 0:
                        if value[0] == '':
                            query = query.filter(attr == None)
                        else:
                            query = query.filter(attr == value[0])
                    else:
                        query = query.filter(attr == None)
                elif operator == 'not_equal':
                    if l > 1:
                        query = query.filter(~attr.in_(value))
                    elif l > 0:
                        if value[0] == '':
                            query = query.filter(attr != None)
                        else:
                            query = query.filter(attr != value[0])
                    else:
                        query = query.filter(attr != None)
                elif operator == 'greater_than':
                    if l > 1:
                        print 'Error-'*100
                    elif l > 0:
                        if value[0] == '':
                            query = query.filter(attr > None)
                        else:
                            query = query.filter(attr > value[0])
                    else:
                        query = query.filter(attr > None)
                elif operator == 'smaller_than':
                    if l > 1:
                        print 'Error-'*100
                    elif l > 0:
                        if value[0] == '':
                            query = query.filter(attr < None)
                        else:
                            query = query.filter(attr < value[0])
                    else:
                        query = query.filter(attr < None)
                elif operator == 'like':
                    if l > 1:
                        print 'Error-'*100
                    elif l > 0:
                        # if value[0] == '':
                        #     query = query.filter(attr == None)
                        # else:
                        query = query.filter(attr.like("%" + str(value[0]) + "%"))
                    else:
                        pass
                        # query = query.filter(attr == None)

        # add_be_af(query, '2')
        return query

    @classmethod
    def not_deleted(cls, query):
        return query.filter(cls.deleted_at == None)

    @classmethod
    def get_one_or_404(cls, handler, id, query=None, q_params=None, user=None, owner=None):
        result, error = cls.get_one(id, query=query, q_params=q_params, user=user, owner=owner)

        if not result:
            handler.send_error(404, reason='There is not the requested object!')

        return result, error

    @classmethod
    def get_one(cls, id, query=None, q_params=None, user=None):
        if not query:
            query = cls.query

        if q_params:
            query = cls.get_new_query(query, q_params, user.type if user else 'none', owner=owner)

        query = cls.not_deleted(query)

        error = None
        result = []

        try:
            result = query.filter(cls.id == id).all()
        except Exception:
            error = 'Sqlalchemy Error'

        if len(result) > 0:
            return result[0], error
        else:
            return None, error

    @classmethod
    def get_ordered_query(cls, query, order, user_type):
        for o in order:
            o = o.split('-')
            is_desc = False
            if len(o) > 1:
                is_desc = True
                o = o[1]
            else:
                o = o[0]

            if (not hasattr(cls, o)) or (o not in cls.user_acl()[user_type]):
                continue

            attr = getattr(cls, o)
            query = query.order_by(desc(attr)) if is_desc else query.order_by(attr)

        return query

    @classmethod
    def get(cls, query=None, q_params=None, order=None, user=None, pagination=None):
        if not query:
            query = cls.query

        if q_params:
            query = cls.get_new_query(query, q_params, user.type if user else 'none')

        if order:
            query = cls.get_ordered_query(query, order, user.type if user else 'none')

        query = cls.not_deleted(query)

        try:
            if pagination:
                pagin = cls.paginate(query, int(pagination[0]), int(pagination[1]))
                return pagin, None
            else:
                items = query.all()
                pagin = Pagination(items=items)

                return pagin, None
        except Exception:
            return None, 'Sqlalchemy error'

    @classmethod
    def add(cls, obj, user=None):
        # obj.created_at = datetime.now()
        if user:
            obj.created_by_id = user.id

        obj.id = uuid.uuid4()

        try:
            cls.session.add(obj)
            cls.session.commit()
        except Exception:
            return 'Sqlalchemy Error'

    @classmethod
    def adds(cls, objs, user=None):
        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            # obj.created_at = datetime.now()
            if user:
                obj.created_by_id = user.id

            obj.id = uuid.uuid4()
            try:
                cls.session.add(obj)
            except Exception:
                return 'Sqlalchemy Error'

        try:
            cls.session.commit()
        except Exception:
            return 'Sqlalchemy Error'

    @classmethod
    def update(cls, obj, user=None):
        # TODO => JSONB Check it - fix by sqlalchemy_utils
        obj.updated_at = datetime.now()
        if user:
            obj.updated_by_id = user.id

        # cls.session.query.update({name: getattr(obj, name) for name in dir(obj) if not name.startswith('__')})
        try:
            cls.session.add(obj)
            cls.session.commit()
        except Exception:
            return 'Sqlalchemy Error'

    @classmethod
    def updates(cls, objs, user=None):
        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            obj.updated_at = datetime.now()
            if user:
                obj.updated_by_id = user.id

            # TODO => JSONB Check it - fix by sqlalchemy_utils
            # cls.query.update({name: getattr(obj, name) for name in dir(obj) if not name.startswith('__')})
            try:
                cls.session.add(obj)
            except Exception:
                return 'Sqlalchemy Error'

        try:
            cls.session.commit()
        except Exception:
            return 'Sqlalchemy Error'

    @classmethod
    def remove(cls, obj, user=None):
        # soft delete
        obj.deleted_at = datetime.now()
        if user:
            obj.deleted_by_id = user.id

        obj.delete_related_obj()
        # cls.session.delete(obj) # => hard delete
        # cls.session.commit() # used in hard delete
        return cls.update(obj)

    @classmethod
    def removes(cls, objs, user=None):
        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            # soft delete
            obj.deleted_at = datetime.now()
            if user:
                obj.deleted_by_id = user.id

            obj.delete_related_obj()

            # cls.session.delete(obj) # => hard delete

        # cls.session.commit() # used in hard delete
        return cls.updates(objs)

    @classmethod
    def paginate(cls, query, page, per_page):
        """Returns ``per_page`` items from page ``page``.
        If no items are found and ``page`` is greater than 1, or if page is less than 1, it aborts with 404.
        This behavior can be disabled by passing ``error_out=False``.
        If ``page`` or ``per_page`` are ``None``, they will be retrieved from the request query.
        If the values are not ints and ``error_out`` is ``True``, it aborts with 404.
        If there is no request or they aren't in the query, they default to 1 and 20 respectively.
        Returns a :class:`Pagination` object.
        """

        items = query.limit(per_page).offset((page - 1) * per_page).all()

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = query.order_by(None).count()

        return Pagination(query, page, per_page, total, items)


db = DB()
db.BaseModel = BaseModel()


class TorModel(db.BaseModel, Model):
    __abstract__ = True

    id = Column(UUIDType(binary=False), primary_key=True)

    created_at = Column(DateTime, default=datetime.now)
    created_by_id = Column(UUIDType(binary=False))  # , ForeignKey('users.id'))
    # created_by_type = Column(String(50))
    # created_by = generic_relationship(created_by_type, created_by_id)

    @property
    def created_by(self):
        from project.modules.user.models import User
        return User.get_one(self.created_by_id)[0]

    updated_at = Column(DateTime, default=datetime.now)
    updated_by_id = Column(UUIDType(binary=False))  # , ForeignKey('users.id'))
    # updated_by_type = Column(String(50))
    # updated_by = generic_relationship(updated_by_type, updated_by_id)

    @property
    def updated_by(self):
        from project.modules.user.models import User
        return User.get_one(self.updated_by_id)[0]

    # soft delete
    deleted_at = Column(DateTime)
    deleted_by_id = Column(UUIDType(binary=False),)  # , ForeignKey('users.id'))
    # deleted_by_type = Column(String(50))
    # deleted_by = generic_relationship(deleted_by_type, deleted_by_id)

    @property
    def deleted_by(self):
        from project.modules.user.models import User
        return User.get_one(self.deleted_by_id)[0]

    # additional used
    data = Column(JSONB())