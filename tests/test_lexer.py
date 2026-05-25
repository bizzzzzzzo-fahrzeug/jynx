import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import unittest
from jynx.lexer import Lexer, LexerError


class TestLexer(unittest.TestCase):
    def test_number_integer(self):
        tokens = Lexer("42").tokens
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, "NUMBER")
        self.assertEqual(tokens[0].value, 42)

    def test_number_float(self):
        tokens = Lexer("3.14").tokens
        self.assertEqual(tokens[0].kind, "NUMBER")
        self.assertEqual(tokens[0].value, 3.14)

    def test_number_negative(self):
        tokens = Lexer("-5").tokens
        self.assertEqual(tokens[0].value, -5)

    def test_string(self):
        tokens = Lexer('"hello"').tokens
        self.assertEqual(tokens[0].kind, "STRING")
        self.assertEqual(tokens[0].value, "hello")

    def test_string_escape(self):
        tokens = Lexer('"hello\\nworld"').tokens
        self.assertEqual(tokens[0].value, "hello\nworld")

    def test_boolean_true(self):
        tokens = Lexer("true").tokens
        self.assertEqual(tokens[0].kind, "BOOL")
        self.assertIs(tokens[0].value, True)

    def test_boolean_false(self):
        tokens = Lexer("false").tokens
        self.assertEqual(tokens[0].kind, "BOOL")
        self.assertIs(tokens[0].value, False)

    def test_nil(self):
        tokens = Lexer("nil").tokens
        self.assertEqual(tokens[0].kind, "NIL")
        self.assertIsNone(tokens[0].value)

    def test_nil_with_paren(self):
        tokens = Lexer("(nil)").tokens
        self.assertEqual(tokens[1].kind, "NIL")

    def test_nil_question(self):
        tokens = Lexer("nil?").tokens
        self.assertEqual(tokens[0].kind, "SYMBOL")
        self.assertEqual(tokens[0].value, "nil?")

    def test_symbol(self):
        tokens = Lexer("foo-bar").tokens
        self.assertEqual(tokens[0].kind, "SYMBOL")
        self.assertEqual(tokens[0].value, "foo-bar")

    def test_lparen(self):
        tokens = Lexer("(").tokens
        self.assertEqual(tokens[0].kind, "LPAREN")

    def test_rparen(self):
        tokens = Lexer(")").tokens
        self.assertEqual(tokens[0].kind, "RPAREN")

    def test_quote(self):
        tokens = Lexer("'x").tokens
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].kind, "QUOTE")
        self.assertEqual(tokens[1].kind, "SYMBOL")

    def test_comment(self):
        tokens = Lexer("; this is a comment\n42").tokens
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].value, 42)

    def test_expression(self):
        tokens = Lexer("(+ 1 2)").tokens
        self.assertEqual(len(tokens), 5)
        self.assertEqual([t.kind for t in tokens], ["LPAREN", "SYMBOL", "NUMBER", "NUMBER", "RPAREN"])

    def test_unexpected_char(self):
        with self.assertRaises(LexerError):
            Lexer("`")

    def test_line_column(self):
        tokens = Lexer("\n 42").tokens
        self.assertEqual(tokens[0].line, 2)
        self.assertEqual(tokens[0].column, 2)


if __name__ == "__main__":
    unittest.main()
