import uuid
import datetime
from sqlalchemy.orm.collections import InstrumentedList

from ipaddr import IPv4Address

from project.core.db import TorModel


def get_json_from_obj(obj, user_type, level=1, include=None, exclude=None):
    if not include:
        include = []

    if not exclude:
        exclude = []

    view = obj.dft_view() if hasattr(obj, 'dft_view') else {}

    if user_type == 'none':
        get_access_fields = []
    else:
        get_access_fields = obj.user_acl()[user_type] if hasattr(obj, 'user_acl') else []

    view.update({inc: inc for inc in include})

    data = {}
    for key in view.keys():
        if key in exclude or key not in get_access_fields:
            continue

        key_dot = key.split('.')
        if len(key_dot) > 1:
            attr = getattr(obj, key_dot[0])
            for k in key_dot[1:]:
                attr = getattr(attr, k)

        elif len(key_dot) == 1:
            attr = getattr(obj, key)
        else:
            continue

        if isinstance(attr, TorModel):
            if level < 3:
                data[view[key]] = get_json_from_obj(attr, user_type, level=level+1)  # , include=include, exclude=exclude)
            else:
                data[view[key]] = {}
        elif isinstance(attr, InstrumentedList):
            data[view[key]] = []
            for attr_el in attr:
                if level < 3:
                    data[view[key]].append(get_json_from_obj(attr_el, user_type, level=level+1)) # , include=include, exclude=exclude)
                else:
                    data[view[key]].append({})
        else:
            data[view[key]] = str(attr) if isinstance(attr, uuid.UUID) or isinstance(attr, IPv4Address) or isinstance(attr, datetime.date) or isinstance(attr, datetime.datetime) else attr

    return data


def get_data_as_json(objs, user_type, include=None, exclude=None):
    if not objs:
        return None

    if not include:
        include = []

    if not exclude:
        exclude = []

    if not isinstance(objs, list):
        objs = [objs]

    ret = []

    for obj in objs:
        data = get_json_from_obj(obj, user_type, level=1, include=include, exclude=exclude)
        ret.append(data)

    return ret


def get_pagination_as_json(pagination):
    return {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }


def make_rest(data, errors):
    return {'data': data, 'errors': errors}