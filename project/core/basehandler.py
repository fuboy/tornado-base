import functools
import urlparse
import json
import jwt
from urllib import urlencode
from tornado.util import unicode_type

from tornado.web import RequestHandler, HTTPError

from pycket.session import SessionManager

from project.modules.user.models import User
from project.ext.utility import from_gregorian_to_jalali
from project.core.rest import make_rest, get_data_as_json, get_pagination_as_json

from .torurl import TorUrl
from .scope import scope
from .db import db


class BaseHandler(RequestHandler):
    # _session = None
    _username = None

    # TODO => change sid on pycket lib
    # @property
    # def session(self):
    #     if not self._session:
    #         self._session = SessionManager(self)
    #
    #     return self._session

    def get_current_user(self):
        username = self.session.get('username')
        if not username:
            return None

        self.current_user, error = User.get_by_username(username)

        return self.current_user

    @property
    def user_type(self):
        return self.current_user.type if self.current_user else 'none'

    @property
    def query_params(self):
        q_ps = self.request.query_arguments
        if 'include' in q_ps:
            del q_ps['include']

        if 'exclude' in q_ps:
            del q_ps['exclude']

        if 'order' in q_ps:
            del q_ps['order']

        if 'pagination' in q_ps:
            del q_ps['pagination']

        return q_ps

    def return_rest(self, data=None, errors=None, status_code=200):
        self._status_code = status_code
        return self.finish(make_rest(data, errors))

    @property
    def pagination(self):
        pagin = self.get_argument('pagination', None)

        if not pagin:
            return None

        pagin = pagin.split(',')

        if len(pagin) < 2:
            return None

        return [pagin[0], pagin[1]]

    @property
    def order(self):
        ord = self.get_argument('order', None)
        new_ord = ord
        if ord:
            ord = ord.split(',')
            new_ord = []
            for key in ord:
                new_ord.append(key)

        return new_ord

    @property
    def include(self):
        inc = self.get_argument('include', None)
        new_inc = inc
        if inc:
            inc = inc.split(',')
            new_inc = []
            for key in inc:
                new_inc.append(key)

        return new_inc

    @property
    def exclude(self):
        exc = self.get_argument('exclude', None)
        new_exc = exc
        if exc:
            exc = exc.split(',')
            new_exc = []
            for key in exc:
                new_exc.append(key)

        return new_exc

    def redirect(self, url, permanent=False, status=None, **kwargs):
        if len(kwargs.items()) > 0:
            if '?' not in url:
                url += '?' + '&'.join(['{k} = {v}'.format(k=k, v=kwargs[k]) for k in kwargs])
            else:
                url += '&' + '&'.join(['{k} = {v}'.format(k=k, v=kwargs[k]) for k in kwargs])

        super(BaseHandler, self).redirect(url, permanent, status)

    def prepare(self):
        scope.set(self)

        # TODO - product - comment out
        # # get jwt token
        # _jwt_encoded = self.request.headers.get('jwt', None)
        # if _jwt_encoded:
        #     _jwt_decoded = jwt.decode(_jwt_encoded, self.settings['jwt_secret'], algorithms=[self.settings['jwt_algorithm']])
        #     self._username = _jwt_decoded['username']
        #
        #     self.set_header('jwt', _jwt_encoded)  # add to header!!! TODO - update time expiration

        '''Incorporate request JSON into arguments dictionary.'''
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)

                for k, v in json_data.items():
                    # Tornado expects values in the argument dict to be lists.
                    # in tornado.web.RequestHandler._get_argument the last argument is returned.
                    json_data[k] = [v]

                # self.request.arguments.pop(self.request.body)
                self.request.arguments.update(json_data)

            except ValueError, e:
                message = 'Unable to parse JSON.'
                self.send_error(400, reason=message)  # Bad Request

    def _get_arguments(self, name, source, strip=True):
        values = []
        for v in source.get(name, []):
            if not isinstance(v, int) and not isinstance(v, list):
                v = self.decode_argument(v, name=name)

            if isinstance(v, unicode_type):
                # Get rid of any weird control chars (unless decoding gave
                # us bytes, in which case leave it alone)
                v = RequestHandler._remove_control_chars_regex.sub(" ", v)
            if strip and not isinstance(v, int) and not isinstance(v, list):
                v = v.strip()

            values.append(v)
        return values

    def on_finish(self):
        scope.set(self)
        db.session.remove()
        scope.set(None)

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        May be overridden by subclasses to add or modify values.

        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        # Add some function to used in template
        namespace = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
            from_gregorian_to_jalali=from_gregorian_to_jalali,
        )
        namespace.update(self.ui)

        return namespace

    def write_error(self, status_code, **kwargs):
        # template_name = self.settings['template_xxx']
        # if status_code in [403, 404, 500]:
        #     template_name = self.settings['template_' + str(status_code)]

        # return self.render(template_name, message=None)
        return {'data': {}, 'errors': {'error_name': str(status_code)}}

    # @property
    # def mail_connection(self):
    #     return self.application.mail_connection
    #
    # def email_callback(self, result):
    #     # TODO => log result email per mail => overwrite send function to pass email to callback
    #     print '*=>'*20, result

    # def send_mail(self, subject='', message='', sender_mail=None, rec_mails=[]):
    #     if not sender_mail:
    #         sender_mail = self.settings['mail_smtp']['username']
    #
    #     if not isinstance(rec_mails, list):
    #         rec_mails = [rec_mails]
    #
    #     message = EmailMessage(subject, message,
    #                            sender_mail, rec_mails,
    #                            connection=self.mail_connection)
    #
    #     message.send(fail_silently=self.settings['mail_smtp']['fail_silently'],
    #                  callback=self.email_callback)

    # Wtform Integration
    def __iter__(self):
        return iter(self.request.arguments)

    def __len__(self):
        return len(self.request.arguments)

    def __contains__(self, name):
        return (name in self.request.arguments)

    def getlist(self, name):
        return self.get_arguments(name)


t_url = TorUrl


def login_required(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def is_type(type):
    def is_type_decorator(method):
        """Decorate methods with this to require that the user be logged in.

        If the user is not logged in, they will be redirected to the configured
        `login url <RequestHandler.get_login_url>`.

        If you configure a login url with a query parameter, Tornado will
        assume you know what you're doing and use it as-is.  If not, it
        will add a `next` parameter so the login page knows where to send
        you once you're logged in.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                raise HTTPError(403)

            if isinstance(type, list):
                flag = False
                for t in type:
                    if self.current_user.type == t:
                        flag = True
                        break

                if not flag:
                    raise HTTPError(403)
                    return
            else:
                if self.current_user.type != type:
                    raise HTTPError(403)
                    return

            return method(self, *args, **kwargs)
        return wrapper
    return is_type_decorator