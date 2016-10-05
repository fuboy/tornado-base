from tornado.web import UIModule


class Form(UIModule):
    def render(self, form, action_url):
        return self.render_string('uimodules/form.html', form=form, action_url=action_url)


class FormExtended(UIModule):
    def render(self, form, action_url, extended_forms):
        return self.render_string('uimodules/form_extended.html', form=form, action_url=action_url, extended_forms=extended_forms)


class FieldError(UIModule):
    def render(self, field):
        return self.render_string('uimodules/field_error.html', field=field)


class Field(UIModule):
    def render(self, field):
        return self.render_string("uimodules/field.html", field=field)

        # def embedded_css(self):
        #     return ".entry { margin-bottom: 1em; }"
        #
        # def embedded_javascript(self):
        #     return ".entry { margin-bottom: 1em; }"
        #
        # def javascript_files(self):
        #     return ".entry { margin-bottom: 1em; }"
        #
        # def css_files(self):
        #     return ".entry { margin-bottom: 1em; }"


class Menu(UIModule):
    def render(self, user, page):
        return self.render_string("uimodules/menu.html", user=user, page=page)

        # def embedded_css(self):
        #     return ".entry { margin-bottom: 1em; }"
        #
        # def embedded_javascript(self):
        #     return ".entry { margin-bottom: 1em; }"
        #
        # def javascript_files(self):
        #     return ".entry { margin-bottom: 1em; }"
        #
        # def css_files(self):
        #     return ".entry { margin-bottom: 1em; }"



