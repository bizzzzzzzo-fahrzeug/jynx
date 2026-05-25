import sys
import os
import io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import unittest
from jynx.lexer import Lexer
from jynx.parser import Parser
from jynx.interpreter import Interpreter


def _eval(source):
    lexer = Lexer(source)
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    interp = Interpreter()
    return interp.interpret(ast)


class TestInterpreter(unittest.TestCase):
    def test_number(self):
        self.assertEqual(_eval("42"), 42)

    def test_float(self):
        self.assertEqual(_eval("3.14"), 3.14)

    def test_string(self):
        self.assertEqual(_eval('"hello"'), "hello")

    def test_boolean_true(self):
        self.assertIs(_eval("true"), True)

    def test_boolean_false(self):
        self.assertIs(_eval("false"), False)

    def test_nil(self):
        self.assertIsNone(_eval("nil"))

    def test_empty_list(self):
        self.assertIsNone(_eval("()"))

    def test_addition(self):
        self.assertEqual(_eval("(+ 1 2)"), 3)

    def test_subtraction(self):
        self.assertEqual(_eval("(- 10 3)"), 7)

    def test_multiplication(self):
        self.assertEqual(_eval("(* 2 3 4)"), 24)

    def test_division(self):
        self.assertEqual(_eval("(/ 10 2)"), 5.0)

    def test_nested_arith(self):
        self.assertEqual(_eval("(+ (* 2 3) (- 10 4))"), 12)

    def test_define_and_use(self):
        interp = Interpreter()
        for src in ["(define x 42)", "x"]:
            lexer = Lexer(src)
            parser = Parser(lexer.tokens)
            result = interp.interpret(parser.parse())
        self.assertEqual(result, 42)

    def test_set(self):
        interp = Interpreter()
        for src in ["(define x 1)", "(set! x 99)", "x"]:
            lexer = Lexer(src)
            parser = Parser(lexer.tokens)
            result = interp.interpret(parser.parse())
        self.assertEqual(result, 99)

    def test_if_true(self):
        self.assertEqual(_eval("(if true 1 2)"), 1)

    def test_if_false(self):
        self.assertEqual(_eval("(if false 1 2)"), 2)

    def test_if_no_else(self):
        self.assertIsNone(_eval("(if false 1)"))

    def test_cond(self):
        self.assertEqual(_eval("(cond ((= 1 2) 1) ((= 3 3) 2))"), 2)

    def test_cond_else(self):
        self.assertEqual(_eval("(cond ((= 1 2) 1) (else 2))"), 2)

    def test_lambda(self):
        self.assertEqual(_eval("((lambda (x) (* x x)) 5)"), 25)

    def test_recursion(self):
        interp = Interpreter()
        src = "(define (fact n) (if (<= n 1) 1 (* n (fact (- n 1)))))"
        interp.interpret(Parser(Lexer(src).tokens).parse())
        result = interp.interpret(Parser(Lexer("(fact 5)").tokens).parse())
        self.assertEqual(result, 120)

    def test_closure(self):
        interp = Interpreter()
        interp.interpret(Parser(Lexer("(define (make-adder x) (lambda (y) (+ x y)))").tokens).parse())
        result = interp.interpret(Parser(Lexer("((make-adder 10) 5)").tokens).parse())
        self.assertEqual(result, 15)

    def test_cons(self):
        self.assertEqual(_eval("(cons 1 (list 2 3))"), [1, 2, 3])

    def test_car(self):
        self.assertEqual(_eval("(car (list 1 2 3))"), 1)

    def test_cdr(self):
        self.assertEqual(_eval("(cdr (list 1 2 3))"), [2, 3])

    def test_cdr_single(self):
        self.assertIsNone(_eval("(cdr (list 1))"))

    def test_list_length(self):
        self.assertEqual(_eval("(length (list 1 2 3))"), 3)

    def test_map(self):
        interp = Interpreter()
        interp.interpret(Parser(Lexer("(define (square n) (* n n))").tokens).parse())
        interp.interpret(Parser(Lexer("(define (map fn lst) (if (nil? lst) nil (cons (fn (car lst)) (map fn (cdr lst)))))").tokens).parse())
        result = interp.interpret(Parser(Lexer("(map square (list 1 2 3))").tokens).parse())
        self.assertEqual(result, [1, 4, 9])

    def test_type_of_number(self):
        self.assertEqual(_eval("(type-of 42)"), "number")

    def test_type_of_string(self):
        self.assertEqual(_eval('(type-of "hi")'), "string")

    def test_type_of_nil(self):
        self.assertEqual(_eval("(type-of nil)"), "nil")

    def test_type_of_list(self):
        self.assertEqual(_eval("(type-of (list 1))"), "list")

    def test_type_of_procedure(self):
        self.assertEqual(_eval("(type-of +)"), "procedure")

    def test_quote_symbol(self):
        self.assertEqual(_eval("'x"), "x")

    def test_quote_list(self):
        self.assertEqual(_eval("'(1 2 3)"), [1, 2, 3])

    def test_begin(self):
        self.assertEqual(_eval("(begin 1 2 3)"), 3)

    def test_print(self):
        interp = Interpreter()
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            interp.interpret(Parser(Lexer('(print "hello")').tokens).parse())
        finally:
            sys.stdout = old_stdout
        self.assertEqual(captured.getvalue(), "hello\n")

    def test_undefined_variable(self):
        with self.assertRaises(NameError):
            _eval("undefined")

    def test_complex_expr(self):
        self.assertEqual(_eval("(+ (* 3 4) (/ 10 2) (- 8 3))"), 12 + 5.0 + 5)


if __name__ == "__main__":
    unittest.main()
