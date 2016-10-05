from project.core.basehandler import BaseHandler, t_url, make_rest, login_required, is_type, get_data_as_json, get_pagination_as_json
from project.libs.utility import confirm_token

from .models import Client
from .forms import CreateClientForm, UpdateClientForm

__all__ = ['routes']


class ClientHandler(BaseHandler):
    # @login_required
    # @is_type(['sales_man', 'sales_manager'])
    def get(self, id=None):
        if id:
            client, error = Client.get_one(self, id=id, q_params=self.query_params, user=self.current_user)
            if not client:
                return

            data = {
                    'client': get_data_as_json(
                                        client,
                                        user_type=self.user_type,
                                        include=self.include,
                                        exclude=self.exclude)
                    }
        else:
            clients_pagin, error = Client.get(q_params=self.query_params,
                                 order=self.order,
                                 user=self.current_user,
                                 pagination=self.pagination)
            data = {
                    'clients': get_data_as_json(
                                        clients_pagin.items,
                                        user_type=self.user_type,
                                        include=self.include,
                                        exclude=self.exclude),
                    'pagination': get_pagination_as_json(clients_pagin)
                    }

        return self.finish(make_rest(data, None))

    def post(self, id=None):
        form = CreateClientForm(self)
        if form.validate():
            client = Client()
            form.populate_obj(client)

            client.password = form.password.data
            Client.add(client, self.current_user)

            data = {
                    'client': get_data_as_json(
                                        client,
                                        user_type=self.user_type,
                                        include=self.include,
                                        exclude=self.exclude)
                    }

            return self.finish(make_rest(data, None))

        return self.return_rest(None, form.errors, 400)

    def put(self, id):
        client, error = Client.get_one(id)

        if not client:
            return self.return_rest(None, {'id': 'There is not the requested id: ' + id}, 404)

        form = UpdateClientForm(self, obj=client)
        if form.validate():
            form.populate_obj(client)

            client.password = form.password.data
            Client.update(client, self.current_user)

            data = {
                    'client': get_data_as_json(
                                        client,
                                        user_type=self.user_type,
                                        include=self.include,
                                        exclude=self.exclude)
                    }

            return self.finish(make_rest(data, None))

        return self.return_rest(None, form.errors, 400)

    def delete(self, id):
        client, error = Client.get_one(id)

        if not client:
            return self.return_rest(None, {'id': 'There is not the requested id: ' + id}, 404)

        Client.remove(client, self.current_user)

        return self.return_rest({'deleted_client_id': id}, None, 200)

    def options(self, id):
        pass


routes = [t_url(r'/clients/(.*)', ClientHandler, name='clients'),]