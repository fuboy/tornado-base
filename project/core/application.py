from tornado.web import Application, _RequestDispatcher, \
                        RedirectHandler, _unquote_or_none, \
                        ErrorHandler
# from tornadomail.backends.smtp import EmailBackend


class Tor_RequestDispatcher(_RequestDispatcher):
    def _find_handler(self):
        # Identify the handler to use as soon as we have the request.
        # Save url path arguments for later.
        app = self.application
        handlers = app._get_host_handlers(self.request)
        if not handlers:
            self.handler_class = RedirectHandler
            self.handler_kwargs = dict(url="%s://%s/"
                                       % (self.request.protocol,
                                          app.default_host))
            return
        for spec in handlers:
            match = spec.regex.match(self.request.path)
            if match:
                self.handler_class = spec.handler_class
                self.handler_kwargs = spec.kwargs
                if spec.regex.groups:
                    # Pass matched groups to the handler.  Since
                    # match.groups() includes both named and
                    # unnamed groups, we want to use either groups
                    # or groupdict but not both.
                    if spec.regex.groupindex:
                        self.path_kwargs = dict(
                            (str(k), _unquote_or_none(v))
                            for (k, v) in match.groupdict().items())
                    else:
                        self.path_args = [_unquote_or_none(s)
                                          for s in match.groups()]

                # Change parameters with url_map if hasattr and set args corrects
                # TODO
                # print '*'*20, spec
                return
        if app.settings.get('default_handler_class'):
            self.handler_class = app.settings['default_handler_class']
            self.handler_kwargs = app.settings.get(
                'default_handler_args', {})
        else:
            self.handler_class = ErrorHandler
            self.handler_kwargs = dict(status_code=404)


class Application(Application):
    # @property
    # def mail_connection(self):
    #     # TODO => why one instance usage?!
    #     return EmailBackend(**self.settings['mail_smtp'])

    def start_request(self, server_conn, request_conn):
        # Modern HTTPServer interface
        return Tor_RequestDispatcher(self, request_conn)

    def __call__(self, request):
        # Legacy HTTPServer interface
        dispatcher = Tor_RequestDispatcher(self, None)
        dispatcher.set_request(request)
        return dispatcher.execute()