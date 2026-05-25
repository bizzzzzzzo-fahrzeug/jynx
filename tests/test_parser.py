import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import unittest
from jynx.lexer import Lexer
from jynx.parser import Parser, ParseError
from jynx.ast import Number, String, Boolean, Nil, Symbol, List, Quote


def _parse(source):
    lexer = Lexer(source)
    parser = Parser(lexer.tokens)
    return parser.parse()


class TestParser(unittest.TestCase):
    def test_parse_number(self):
        ast = _parse("42")
        self.assertIsInstance(ast[0], Number)
        self.assertEqual(ast[0].value, 42)

    def test_parse_string(self):
        ast = _parse('"hello"')
        self.assertIsInstance(ast[0], String)
        self.assertEqual(ast[0].value, "hello")

    def test_parse_boolean(self):
        ast = _parse("true")
        self.assertIsInstance(ast[0], Boolean)
        self.assertIs(ast[0].value, True)

    def test_parse_nil(self):
        ast = _parse("nil")
        self.assertIsInstance(ast[0], Nil)

    def test_parse_symbol(self):
        ast = _parse("foo")
        self.assertIsInstance(ast[0], Symbol)
        self.assertEqual(ast[0].name, "foo")

    def test_parse_list(self):
        ast = _parse("(+ 1 2)")
        self.assertIsInstance(ast[0], List)
        self.assertEqual(len(ast[0].elements), 3)

    def test_parse_nested(self):
        ast = _parse("(+ (* 2 3) 1)")
        self.assertIsInstance(ast[0], List)
        inner = ast[0].elements[1]
        self.assertIsInstance(inner, List)
        self.assertEqual(inner.elements[0].name, "*")

    def test_parse_quote(self):
        ast = _parse("'(1 2 3)")
        self.assertIsInstance(ast[0], Quote)
        self.assertIsInstance(ast[0].expr, List)

    def test_parse_empty_list(self):
        ast = _parse("()")
        self.assertIsInstance(ast[0], List)
        self.assertEqual(len(ast[0].elements), 0)

    def test_parse_multiple(self):
        ast = _parse("1 2 3")
        self.assertEqual(len(ast), 3)

    def test_parse_unclosed(self):
        with self.assertRaises(ParseError):
            _parse("(1 2")

    def test_parse_comment(self):
        ast = _parse("; comment\n42")
        self.assertEqual(len(ast), 1)
        self.assertEqual(ast[0].value, 42)


if __name__ == "__main__":
    unittest.main()
