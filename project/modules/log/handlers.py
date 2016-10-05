from project.core.basehandler import BaseHandler, t_url, make_rest, login_required, is_type, get_data_as_json, get_pagination_as_json

from .models import Log


__all__ = ['routes']


class LogHandler(BaseHandler):
    # @login_required
    # @is_type(['sales_man', 'sales_manager'])
    def get(self, id=None):
        if id:
            log, error = Log.get_one(self, id=id,
                                q_params=self.query_params,
                                user=self.current_user
                                )
            if not log:
                return

            data = {
                    'log': get_data_as_json(
                                        log,
                                        user_type=self.user_type,
                                        include=self.include,
                                        exclude=self.exclude)
                    }
        else:
            logs_pagin, error = Log.get(
                            q_params=self.query_params,
                            order=self.order,
                            user=self.current_user,
                            pagination=self.pagination
                            )
            data = {
                    'logs': get_data_as_json(
                                        logs_pagin.items,
                                        user_type=self.user_type,
                                        include=self.include,
                                        exclude=self.exclude),
                    'pagination': get_pagination_as_json(logs_pagin)
                    }

        return self.finish(make_rest(data, None))

    def delete(self, id):
        log, error = Log.get_one(id)

        if not log:
            return self.return_rest(None, {'id': 'There is not the requested id: ' + id}, 404)

        Log.remove(log, self.current_user)

        return self.return_rest({'deleted_log_id': id}, None, 200)

    def options(self, id):
        pass


routes = [t_url(r'/logs/(.*)', LogHandler, name='logs')]