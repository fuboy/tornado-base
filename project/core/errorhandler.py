from tornado.web import ErrorHandler

from .basehandler import BaseHandler


class ErrorHandler(ErrorHandler, BaseHandler):
    def write_error(self, status_code, **kwargs):
        # template_name = self.settings['template_xxx']
        # if status_code in [403, 404, 500]:
        #     template_name = self.settings['template_' + str(status_code)]

        # return self.render(template_name, message=None)
        return {'data': {}, 'errors': {'error_name': str(status_code)}}

