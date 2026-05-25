from .ast import Number, String, Boolean, Nil, Symbol, List, Quote


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        results = []
        while self.pos < len(self.tokens):
            results.append(self._parse_expr())
        return results

    def _parse_expr(self):
        if self.pos >= len(self.tokens):
            raise ParseError("Unexpected end of input")
        tok = self.tokens[self.pos]
        if tok.kind == "NUMBER":
            self.pos += 1
            return Number(tok.value)
        elif tok.kind == "STRING":
            self.pos += 1
            return String(tok.value)
        elif tok.kind == "BOOL":
            self.pos += 1
            return Boolean(tok.value)
        elif tok.kind == "NIL":
            self.pos += 1
            return Nil()
        elif tok.kind == "SYMBOL":
            self.pos += 1
            return Symbol(tok.value)
        elif tok.kind == "LPAREN":
            self.pos += 1
            elements = []
            while self.pos < len(self.tokens) and self.tokens[self.pos].kind != "RPAREN":
                elements.append(self._parse_expr())
            if self.pos >= len(self.tokens):
                raise ParseError("Unclosed parenthesis")
            self.pos += 1
            return List(elements)
        elif tok.kind == "QUOTE":
            self.pos += 1
            expr = self._parse_expr()
            return Quote(expr)
        else:
            raise ParseError(f"Unexpected token {tok}")
