import json
from tornado import gen, web, httpclient, escape
from tornado.auth import GoogleOAuth2Mixin

from project.core.basehandler import BaseHandler, t_url

from project.modules.models import User

from .forms import LoginForm

__all__ = ['routes']


class AuthLoginHandler(BaseHandler):
    def get(self):
        import jwt
        _jwt_encoded = jwt.encode({'username': self._username}, self.settings['jwt_secret'], algorithm=self.settings['jwt_algorithm'])
        self.add_header('jwt', _jwt_encoded)
        return self.finish('Okey, '*100)
        # form = LoginForm(self)
        # self.render('auth/login.html', form=form)

    def post(self):
        if self.current_user:
            if self.current_user.type == 'admin':
                return self.redirect(self.reverse_url('user.admin', self.current_user.username))
            elif self.current_user.type == 'client':
                return self.redirect(self.reverse_url('user.client', self.current_user.username, ''))

        form = LoginForm(self)
        if form.validate():
            user = User.get_by_username(form.username.data.lower())
            if not user:
                form['username'].errors.append('Requested User not exist')
                return self.render('auth/login.html', form=form)

            if user.password == '':
                form['password'].errors.append('The Password can not be empty')
                return self.render('auth/login.html', form=form)

            if user.password != form.password.data:
                form['password'].errors.append('The Password is wrong for the user')
                return self.render('auth/login.html', form=form)

            self.session.set('username', user.username.lower())

            if user.type == 'admin':
                return self.redirect(self.reverse_url('user.admin', user.username))
            elif user.type == 'client':
                return self.redirect(self.reverse_url('user.client', user.username, ''))

        return self.render('auth/login.html', form=form)


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.session.delete('username')
        self.redirect("/")


class GoogleOAuth2LoginHandler(BaseHandler, GoogleOAuth2Mixin):
    @gen.coroutine
    def get(self):
        # TODO
        # if self.current_user:
        #     self.redirect('index')
        #     return

        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                redirect_uri=self.settings['google_oauth']['redirect_url'],
                code=self.get_argument('code'))

            if not access:
                pass  # TODO => clear sessin

            access_token = str(access['access_token'])
            http_client = self.get_auth_http_client()
            http_client.fetch('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+access_token, self._save_user_profile)

            # Save the user and access token with
            # e.g. set_secure_cookie.
        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['google_oauth']['redirect_url'],
                client_id=self.settings['google_oauth']['key'],
                scope=self.settings['google_oauth']['scope'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

    def _save_user_profile(self, response):
        if not response:
            raise web.HTTPError(500, "Google authentication failed.")

        user = json.loads(response.body)
        # TODO complete it - if not user create user or redirect to register user page else login it
        print '*'*20, user
        # self.set_secure_cookie('trakr', user['email'])
        # self.redirect('/products')


routes = [t_url(r'/auth/login/', AuthLoginHandler, name='auth.login'),
          t_url(r'/auth/logout/', AuthLogoutHandler, name='auth.logout'),
          t_url(r'/', AuthLoginHandler, name='index')]
          # n_url(r'/auth/google/', GoogleOAuth2LoginHandler, name='auth.google'),]