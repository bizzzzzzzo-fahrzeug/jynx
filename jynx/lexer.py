import re


class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.kind}, {self.value!r})"


TOKEN_SPEC = [
    ("COMMENT", r";[^\n]*"),
    ("NUMBER", r"-?\d+(\.\d+)?"),
    ("STRING", r'"(?:[^"\\]|\\.)*"'),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("QUOTE", r"'"),
    ("BOOL", r"true|false"),
    ("NIL", r"nil(?=[\s\(\)'\"\];]|$)"),
    ("SYMBOL", r"[^\s\(\)'`;\"]+"),
    ("WHITESPACE", r"\s+"),
]


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        self._tokenize()

    def _tokenize(self):
        while self.pos < len(self.source):
            matched = False
            for kind, pattern in TOKEN_SPEC:
                regex = re.compile(pattern)
                m = regex.match(self.source, self.pos)
                if m:
                    value = m.group(0)
                    if kind == "COMMENT":
                        pass
                    elif kind == "WHITESPACE":
                        if "\n" in value:
                            self.line += value.count("\n")
                            last_newline = value.rfind("\n")
                            after_newline = len(value) - last_newline - 1
                            self.column = 1 + after_newline
                        else:
                            self.column += len(value)
                    elif kind == "BOOL":
                        self.tokens.append(Token("BOOL", value == "true", self.line, self.column))
                        self.column += len(value)
                    elif kind == "NIL":
                        self.tokens.append(Token("NIL", None, self.line, self.column))
                        self.column += len(value)
                    elif kind == "NUMBER":
                        if "." in value:
                            self.tokens.append(Token("NUMBER", float(value), self.line, self.column))
                        else:
                            self.tokens.append(Token("NUMBER", int(value), self.line, self.column))
                        self.column += len(value)
                    elif kind == "STRING":
                        parsed = value[1:-1]
                        parsed = parsed.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"').replace("\\\\", "\\")
                        self.tokens.append(Token("STRING", parsed, self.line, self.column))
                        self.column += len(value)
                    elif kind == "QUOTE":
                        self.tokens.append(Token("QUOTE", value, self.line, self.column))
                        self.column += len(value)
                    elif kind in ("LPAREN", "RPAREN"):
                        self.tokens.append(Token(kind, value, self.line, self.column))
                        self.column += len(value)
                    elif kind == "SYMBOL":
                        self.tokens.append(Token("SYMBOL", value, self.line, self.column))
                        self.column += len(value)
                    self.pos = m.end()
                    matched = True
                    break
            if not matched:
                char = self.source[self.pos]
                raise LexerError(f"Unexpected character {char!r} at line {self.line}, column {self.column}")

    def __iter__(self):
        return iter(self.tokens)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, idx):
        return self.tokens[idx]
