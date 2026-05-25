import sys
import os
from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .interpreter import Interpreter, InterpreterError


class REPL:
    def __init__(self):
        self.interpreter = Interpreter()

    def run_file(self, path):
        with open(path) as f:
            source = f.read()
        try:
            lexer = Lexer(source)
            parser = Parser(lexer.tokens)
            ast = parser.parse()
            self.interpreter.interpret(ast)
        except (LexerError, ParseError, InterpreterError, TypeError, NameError, RuntimeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        return 0

    def run_repl(self):
        print(f"Jynx v0.1.0 — Type 'exit' to quit")
        history = []
        while True:
            try:
                line = input("jynx> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line.strip():
                continue
            if line.strip() == "exit":
                break
            history.append(line)
            try:
                lexer = Lexer(line)
                parser = Parser(lexer.tokens)
                ast = parser.parse()
                for node in ast:
                    result = self.interpreter.eval_expr(node)
                    if result is not None:
                        print(self._repr(result))
            except (LexerError, ParseError, InterpreterError, TypeError, NameError, RuntimeError) as e:
                print(f"Error: {e}")

    def eval_source(self, source):
        lexer = Lexer(source)
        parser = Parser(lexer.tokens)
        ast = parser.parse()
        return self.interpreter.interpret(ast)

    def _repr(self, val):
        if val is None:
            return "nil"
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, list):
            return "(" + " ".join(self._repr(v) for v in val) + ")"
        elif isinstance(val, float):
            if val == int(val):
                return str(int(val))
            return str(val)
        return str(val)
