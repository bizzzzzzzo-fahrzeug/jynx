class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class String(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String({self.value!r})"

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Boolean({self.value})"

class Nil(ASTNode):
    def __repr__(self):
        return "Nil"

class Symbol(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Symbol({self.name})"

class List(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"List({self.elements})"

class Quote(ASTNode):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Quote({self.expr})"
