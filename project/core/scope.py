class Scope(object):
    def __init__(self):
        self._current_scope = None

    def set(self, scope):
        self._current_scope = scope

    def get(self):
        return self._current_scope

scope = Scope()