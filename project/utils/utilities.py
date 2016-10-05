import re
import os
import random
from datetime import datetime


def datetime_to_date(dt):
    return datetime.date(dt.year, dt.month, dt.day)


def niceboolean(value):
    if type(value) is bool:
        return value
    falseness = ('','no','off','false','none','0', 'f')
    return str(value).lower().strip() not in falseness

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain


def valid_email(email):
    return bool(email_re.search(email))


def mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                    "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)

from random import choice
from string import letters


def random_string(length):
    return ''.join(choice(letters) for i in xrange(length))


def all_hash_tags(tags, title):
    """return true if all tags in the title were constructed with a '#' instead
    of a '@' sign"""
    for tag in tags:
        if re.findall(r'(^|\s)@%s\b' % re.escape(tag), title):
            return False
    return True


def all_atsign_tags(tags, title):
    """return true if all tags in the title were constructed with a '@' instead
    of a '#' sign"""
    for tag in tags:
        if re.findall(r'(^|\s)#%s\b' % re.escape(tag), title):
            return False
    return True


def generate_random_color():
    def dec2hex(d):
        return "%02X" % d
    return '#%s%s%s' % (
      dec2hex(random.randint(0, 255)),
      dec2hex(random.randint(0, 255)),
      dec2hex(random.randint(0, 255)),
    )