class Environment:
    def __init__(self, outer=None):
        self.bindings = {}
        self.outer = outer

    def define(self, name, value):
        self.bindings[name] = value

    def set(self, name, value):
        if name in self.bindings:
            self.bindings[name] = value
        elif self.outer is not None:
            self.outer.set(name, value)
        else:
            raise NameError(f"Undefined variable: {name}")

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if self.outer is not None:
            return self.outer.get(name)
        raise NameError(f"Undefined variable: {name}")

    def has(self, name):
        if name in self.bindings:
            return True
        if self.outer is not None:
            return self.outer.has(name)
        return False

    def __repr__(self):
        return f"Environment({list(self.bindings.keys())})"
