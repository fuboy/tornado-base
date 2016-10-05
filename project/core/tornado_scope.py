import tornado.gen

from .scope import scope

original_runner_init = tornado.gen.Runner.__init__
original_runner_run = tornado.gen.Runner.run
original_runner_handle_exception = tornado.gen.Runner.handle_exception


def new_runner_init(self, *args, **kwargs):
    original_runner_init(self, *args, **kwargs)
    self.scope = scope.get()


def new_runner_run(self, *args, **kwargs):
    scope.restore(self.scope)
    return original_runner_run(self, *args, **kwargs)


tornado.gen.Runner.__init__ = new_runner_init
tornado.gen.Runner.run = new_runner_run