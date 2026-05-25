from .ast import Number, String, Boolean, Nil, Symbol, List, Quote
from .env import Environment
from .builtins import BUILTINS, BuiltinProcedure


class InterpreterError(Exception):
    pass


class UserProcedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def call(self, args):
        if len(args) != len(self.params):
            raise TypeError(f"Expected {len(self.params)} arguments, got {len(args)}")
        local_env = Environment(outer=self.env)
        for param, arg in zip(self.params, args):
            local_env.define(param.name, arg)
        return self._eval_body(self.body, local_env)

    def _eval_body(self, body, env):
        result = None
        for expr in body:
            result = evaluate(expr, env)
        return result

    def __repr__(self):
        return f"<procedure: ({' '.join(p.name for p in self.params)})>"


class MacroProcedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def call(self, args):
        if len(args) != len(self.params):
            raise TypeError(f"Macro expected {len(self.params)} arguments, got {len(args)}")
        local_env = Environment(outer=self.env)
        for param, arg in zip(self.params, args):
            local_env.define(param.name, arg)
        result = None
        for expr in self.body:
            result = evaluate(expr, local_env)
        return result

    def __repr__(self):
        return f"<macro: ({' '.join(p.name for p in self.params)})>"


def evaluate(expr, env):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, String):
        return expr.value
    elif isinstance(expr, Boolean):
        return expr.value
    elif isinstance(expr, Nil):
        return None
    elif isinstance(expr, Symbol):
        return env.get(expr.name)
    elif isinstance(expr, Quote):
        return _quote_val(expr.expr)
    elif isinstance(expr, List):
        if not expr.elements:
            return None
        head = expr.elements[0]
        if isinstance(head, Symbol):
            name = head.name
            if name == "define":
                return _eval_define(expr.elements[1:], env)
            elif name == "set!":
                return _eval_set(expr.elements[1:], env)
            elif name == "if":
                return _eval_if(expr.elements[1:], env)
            elif name == "cond":
                return _eval_cond(expr.elements[1:], env)
            elif name == "lambda":
                return _eval_lambda(expr.elements[1:], env)
            elif name == "macro":
                return _eval_macro(expr.elements[1:], env)
            elif name == "begin":
                return _eval_begin(expr.elements[1:], env)
            elif name == "quote":
                if len(expr.elements) == 2:
                    return _quote_val(expr.elements[1])
                raise InterpreterError("quote expects 1 argument")
            elif name == "and":
                return _eval_and(expr.elements[1:], env)
            elif name == "or":
                return _eval_or(expr.elements[1:], env)
            elif name == "defmacro":
                return _eval_defmacro(expr.elements[1:], env)
            elif name == "let":
                return _eval_let(expr.elements[1:], env)
        return _eval_call(expr, env)
    else:
        return expr


def _quote_val(expr):
    if isinstance(expr, List):
        return [_quote_val(e) for e in expr.elements]
    elif isinstance(expr, Symbol):
        return expr.name
    elif isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, String):
        return expr.value
    elif isinstance(expr, Boolean):
        return expr.value
    elif isinstance(expr, Nil):
        return None
    elif isinstance(expr, Quote):
        return _quote_val(expr.expr)
    return expr


def _eval_define(args, env):
    if len(args) < 2:
        raise InterpreterError("define expects at least 2 arguments")
    first = args[0]
    if isinstance(first, List):
        name = first.elements[0].name
        params = first.elements[1:]
        body = args[1:]
        proc = UserProcedure(params, body, env)
        env.define(name, proc)
        return None
    elif isinstance(first, Symbol):
        val = evaluate(args[1], env)
        env.define(first.name, val)
        return None
    raise InterpreterError(f"Invalid define syntax: {first}")


def _eval_set(args, env):
    if len(args) != 2:
        raise InterpreterError("set! expects 2 arguments")
    if not isinstance(args[0], Symbol):
        raise InterpreterError("set! first argument must be a symbol")
    val = evaluate(args[1], env)
    env.set(args[0].name, val)
    return None


def _eval_if(args, env):
    if len(args) < 2 or len(args) > 3:
        raise InterpreterError("if expects 2 or 3 arguments")
    cond = evaluate(args[0], env)
    if cond is not None and cond is not False:
        return evaluate(args[1], env)
    elif len(args) == 3:
        return evaluate(args[2], env)
    return None


def _eval_cond(args, env):
    for clause in args:
        if not isinstance(clause, List) or len(clause.elements) < 2:
            raise InterpreterError("cond clause must be a list of (test expr...)")
        test_expr = clause.elements[0]
        if isinstance(test_expr, Symbol) and test_expr.name == "else":
            test = True
        else:
            test = evaluate(test_expr, env)
        if test is not None and test is not False:
            result = None
            for expr in clause.elements[1:]:
                result = evaluate(expr, env)
            return result
    return None


def _eval_lambda(args, env):
    if not args:
        raise InterpreterError("lambda expects parameter list and body")
    params = args[0]
    body = args[1:]
    if not isinstance(params, List):
        raise InterpreterError("lambda parameter list must be a list")
    param_symbols = []
    for p in params.elements:
        if not isinstance(p, Symbol):
            raise InterpreterError("lambda parameters must be symbols")
        param_symbols.append(p)
    return UserProcedure(param_symbols, body, env)


def _eval_macro(args, env):
    if not args:
        raise InterpreterError("macro expects parameter list and body")
    params = args[0]
    body = args[1:]
    if not isinstance(params, List):
        raise InterpreterError("macro parameter list must be a list")
    param_symbols = []
    for p in params.elements:
        if not isinstance(p, Symbol):
            raise InterpreterError("macro parameters must be symbols")
        param_symbols.append(p)
    return MacroProcedure(param_symbols, body, env)


def _eval_let(args, env):
    if len(args) < 2:
        raise InterpreterError("let expects bindings and body")
    bindings = args[0]
    body = args[1:]
    if not isinstance(bindings, List):
        raise InterpreterError("let bindings must be a list")
    local_env = Environment(outer=env)
    for binding in bindings.elements:
        if not isinstance(binding, List) or len(binding.elements) != 2:
            raise InterpreterError("let binding must be (name value)")
        name = binding.elements[0]
        val = evaluate(binding.elements[1], env)
        if not isinstance(name, Symbol):
            raise InterpreterError("let binding name must be a symbol")
        local_env.define(name.name, val)
    result = None
    for expr in body:
        result = evaluate(expr, local_env)
    return result


def _eval_defmacro(args, env):
    if len(args) < 2:
        raise InterpreterError("defmacro expects at least 2 arguments")
    first = args[0]
    if isinstance(first, List):
        name = first.elements[0].name
        params = first.elements[1:]
        body = args[1:]
        proc = MacroProcedure(params, body, env)
        env.define(name, proc)
        return None
    elif isinstance(first, Symbol):
        val = evaluate(args[1], env)
        if not isinstance(val, MacroProcedure):
            raise InterpreterError("defmacro value must be a macro")
        env.define(first.name, val)
        return None
    raise InterpreterError("Invalid defmacro syntax")


def _eval_begin(args, env):
    result = None
    for expr in args:
        result = evaluate(expr, env)
    return result


def _eval_and(args, env):
    for expr in args:
        val = evaluate(expr, env)
        if val is None or val is False:
            return val
    return True if args else True


def _eval_or(args, env):
    result = None
    for expr in args:
        val = evaluate(expr, env)
        if val is not None and val is not False:
            return val
        result = val
    return result


def _eval_call(expr, env):
    if not expr.elements:
        return []
    proc_val = evaluate(expr.elements[0], env)
    if isinstance(proc_val, MacroProcedure):
        raw_args = [arg for arg in expr.elements[1:]]
        expansion = proc_val.call(raw_args)
        return _eval_macro_result(expansion, env)
    arg_vals = [evaluate(arg, env) for arg in expr.elements[1:]]
    if isinstance(proc_val, UserProcedure):
        return proc_val.call(arg_vals)
    elif isinstance(proc_val, BuiltinProcedure):
        return proc_val.call(arg_vals)
    elif callable(proc_val):
        return proc_val(*arg_vals)
    raise InterpreterError(f"{proc_val} is not a procedure")


def _data_to_ast(data):
    if isinstance(data, list):
        return List([_data_to_ast(d) for d in data])
    if isinstance(data, str):
        return Symbol(data)
    if isinstance(data, (int, float)):
        return Number(data)
    if isinstance(data, bool):
        return Boolean(data)
    if data is None:
        return Nil()
    return data


def _eval_macro_result(result, env):
    ast = _data_to_ast(result)
    return evaluate(ast, env)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        for name, proc in BUILTINS.items():
            self.global_env.define(name, proc)

    def interpret(self, ast_nodes):
        results = []
        for node in ast_nodes:
            results.append(evaluate(node, self.global_env))
        return results[-1] if results else None

    def eval_expr(self, expr):
        return evaluate(expr, self.global_env)
