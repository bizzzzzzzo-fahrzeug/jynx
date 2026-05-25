import sys
import math
import os
import subprocess


class BuiltinProcedure:
    def __init__(self, name, fn, arity=None):
        self.name = name
        self.fn = fn
        self.arity = arity

    def call(self, args):
        if self.arity is not None and len(args) != self.arity:
            raise TypeError(f"{self.name} expects {self.arity} arguments, got {len(args)}")
        return self.fn(args)

    def __repr__(self):
        return f"<builtin: {self.name}>"


def _number(args):
    for a in args:
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            return False
    return True


def _string(args):
    for a in args:
        if not isinstance(a, str):
            return False
    return True


def _listp(args):
    for a in args:
        if not isinstance(a, list):
            return False
    return True


def _procedure(args):
    for a in args:
        if not isinstance(a, (BuiltinProcedure, list)):
            return False
    return True


def _type_of(args):
    val = args[0]
    if isinstance(val, bool):
        return "boolean"
    elif isinstance(val, (int, float)):
        return "number"
    elif isinstance(val, str):
        return "string"
    elif val is None:
        return "nil"
    elif isinstance(val, list):
        return "list"
    elif isinstance(val, BuiltinProcedure):
        return "procedure"
    else:
        return "unknown"


BUILTINS = {
    "+": BuiltinProcedure("+", lambda a: sum(a)),
    "-": BuiltinProcedure("-", lambda a: a[0] - sum(a[1:]) if len(a) > 1 else -a[0]),
    "*": BuiltinProcedure("*", lambda a: __import__("functools").reduce(lambda x, y: x * y, a, 1)),
    "/": BuiltinProcedure("/", lambda a: __import__("functools").reduce(lambda x, y: x / y, a)),
    "%": BuiltinProcedure("%", lambda a: a[0] % a[1] if len(a) == 2 else TypeError("mod expects 2 args")),
    "=": BuiltinProcedure("=", lambda a: a[0] == a[1] if len(a) == 2 else TypeError("= expects 2 args")),
    "<": BuiltinProcedure("<", lambda a: a[0] < a[1] if len(a) == 2 else TypeError("< expects 2 args")),
    ">": BuiltinProcedure(">", lambda a: a[0] > a[1] if len(a) == 2 else TypeError("> expects 2 args")),
    "<=": BuiltinProcedure("<=", lambda a: a[0] <= a[1] if len(a) == 2 else TypeError("<= expects 2 args")),
    ">=": BuiltinProcedure(">=", lambda a: a[0] >= a[1] if len(a) == 2 else TypeError(">= expects 2 args")),
    "and": BuiltinProcedure("and", lambda a: all(a)),
    "or": BuiltinProcedure("or", lambda a: any(a)),
    "not": BuiltinProcedure("not", lambda a: not a[0] if len(a) == 1 else TypeError("not expects 1 arg")),
    "cons": BuiltinProcedure("cons", lambda a: [a[0]] + (a[1] if isinstance(a[1], list) else [])),
    "car": BuiltinProcedure("car", lambda a: a[0][0] if a[0] else nil_error("car of empty list")),
    "cdr": BuiltinProcedure("cdr", lambda a: _cdr(a[0])),
    "list": BuiltinProcedure("list", lambda a: a),
    "length": BuiltinProcedure("length", lambda a: len(a[0])),
    "append": BuiltinProcedure("append", lambda a: a[0] + (a[1] if isinstance(a[1], list) else [a[1]])),
    "print": BuiltinProcedure("print", lambda a: sys.stdout.write(" ".join(str(x) for x in a) + "\n") or None),
    "display": BuiltinProcedure("display", lambda a: sys.stdout.write(str(a[0])) or None),
    "read-line": BuiltinProcedure("read-line", lambda a: sys.stdin.readline().rstrip("\n")),
    "string-append": BuiltinProcedure("string-append", lambda a: "".join(str(x) for x in a)),
    "string-length": BuiltinProcedure("string-length", lambda a: len(str(a[0]))),
    "string-slice": BuiltinProcedure("string-slice", lambda a: str(a[0])[a[1]:a[2]]),
    "number->string": BuiltinProcedure("number->string", lambda a: str(a[0])),
    "string->number": BuiltinProcedure("string->number", lambda a: float(a[0]) if "." in str(a[0]) else int(a[0])),
    "type-of": BuiltinProcedure("type-of", _type_of),
    "number?": BuiltinProcedure("number?", lambda a: _number(a)),
    "string?": BuiltinProcedure("string?", lambda a: _string(a)),
    "list?": BuiltinProcedure("list?", lambda a: _listp(a)),
    "boolean?": BuiltinProcedure("boolean?", lambda a: isinstance(a[0], bool)),
    "nil?": BuiltinProcedure("nil?", lambda a: a[0] is None),
    "procedure?": BuiltinProcedure("procedure?", lambda a: _procedure(a)),
    "exit": BuiltinProcedure("exit", lambda a: sys.exit(a[0] if a else 0)),
    "error": BuiltinProcedure("error", lambda a: _raise_error(a[0])),
    "typeof": BuiltinProcedure("typeof", _type_of),
}


def _cdr(lst):
    if not lst:
        return None
    tail = lst[1:]
    return tail if tail else None


def nil_error(msg):
    raise RuntimeError(msg)


def _raise_error(msg):
    raise RuntimeError(msg)
