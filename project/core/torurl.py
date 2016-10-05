from tornado.web import URLSpec


class TorUrl(URLSpec):
    def __init__(self, pattern, handler, kwargs=None, name=None, url_map=None):
        super(TorUrl, self).__init__(pattern, handler, kwargs, name)
        self.url_map = url_map

    def __repr__(self):
        return '%s(%r, %s, kwargs=%r, name=%r, url_map=%s)' % \
            (self.__class__.__name__, self.regex.pattern,
             self.handler_class, self.kwargs, self.name, self.url_map)