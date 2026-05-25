# Spec: Jynx Programming Language

## Objective

Jynx is a Lisp-like (S-expression-based) programming language that combines the expressiveness of Python, the ubiquity of JavaScript, and deep Linux system integration — all in one coherent language.

It aims to be a **batteries-included scripting language** with built-in support for web serving, networking, file I/O, process management, and more.

**Success criteria for v1 (foundation):**
- S-expression lexer, parser, and tree-walking interpreter
- Core data types: numbers, strings, booleans, nil, symbols, lists
- Variables (`define`, `set!`)
- Arithmetic (`+`, `-`, `*`, `/`, `%`)
- Comparison (`=`, `<`, `>`, `<=`, `>=`)
- Conditionals (`if`, `cond`)
- Functions (`lambda`, named `define`)
- Recursion support
- REPL (Read-Eval-Print Loop) with history
- Print / display output
- Test suite covering all components

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Implementation | Python 3.11+ |
| Testing | pytest |
| Packaging | Standard Python module |
| Parser | Hand-written recursive descent |

## Commands

```bash
# Run a Jynx file
python -m jynx <file.jynx>

# Start REPL
python -m jynx

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=jynx -v
```

## Project Structure

```
jynx/
├── SPEC.md                ← This specification
├── main.py                ← Entry point: `python main.py <file>` or REPL
├── jynx/
│   ├── __init__.py
│   ├── lexer.py           ← Source text → token stream
│   ├── parser.py          ← Token stream → AST
│   ├── ast.py             ← AST node definitions
│   ├── interpreter.py     ← Tree-walking evaluator
│   ├── env.py             ← Environment (scope/closure support)
│   ├── builtins.py        ← Built-in functions (+, *, print, etc.)
│   ├── repl.py            ← Interactive REPL
│   └── stdlib/            ← Standard library written in Jynx
│       └── ...
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_interpreter.py
└── examples/
    └── hello.jynx
```

## Syntax (S-expressions)

Jynx uses Lisp-style prefix notation with parentheses.

```
; Comments use semicolons

; Literals
42           ; integer
3.14         ; float
"hello"      ; string
true         ; boolean
false        ; boolean
nil          ; null/empty
(1 2 3)      ; list
(a b c)      ; quoted list

; Arithmetic
(+ 1 2)              ; → 3
(* (+ 1 2) 3)        ; → 9

; Variables
(define x 42)
(set! x 99)

; Conditionals
(if (> x 10)
    (print "big")
    (print "small"))

; Functions
(define (square x)
    (* x x))

(define greet
    (lambda (name)
        (string-append "Hello, " name)))

; OOP (v2)
(define-class Point (x y)
    (define (distance)
        (sqrt (+ (* x x) (* y y)))))
```

## Core Data Types

| Type | Examples | Notes |
|------|----------|-------|
| Integer | `42`, `-1`, `0` | Arbitrary precision |
| Float | `3.14`, `-0.5` | IEEE 754 double |
| String | `"hello"`, `""` | Double-quoted |
| Boolean | `true`, `false` | |
| Nil | `nil` | Null/empty |
| Symbol | `foo`, `+`, `define` | Evaluated as variable ref |
| List | `(1 2 3)`, `(+ 1 x)` | First element is procedure call |
| Procedure | `<proc>` | Built-in or user-defined |
| Error | `<error>` | Runtime error |

## Evaluation Rules

1. **Self-evaluating:** numbers, strings, booleans, nil evaluate to themselves
2. **Symbols:** evaluate to the value they name in the current environment
3. **Lists:** first element is evaluated as a procedure, rest as arguments
4. **Special forms** (`define`, `set!`, `if`, `cond`, `lambda`, `quote`, `begin`): their own evaluation rules

## Built-in Functions (v1)

**Arithmetic:** `+`, `-`, `*`, `/`, `%`
**Comparison:** `=`, `<`, `>`, `<=`, `>=`
**Logical:** `and`, `or`, `not`
**List:** `cons`, `car`, `cdr`, `list`, `length`, `append`
**I/O:** `print`, `display`, `read-line`
**String:** `string-append`, `string-length`, `string-slice`
**Type:** `type-of`, `number?`, `string?`, `list?`, `boolean?`, `nil?`, `procedure?`
**Conversion:** `number->string`, `string->number`
**Misc:** `eval`, `apply`, `exit`

## Testing Strategy

- **Framework:** pytest
- **Test levels:** Unit tests for lexer, parser, interpreter
- **Coverage target:** >80% for core modules
- **Test files mirror source:** `tests/test_lexer.py` tests `jynx/lexer.py`, etc.

## Boundaries

- **Always:**
  - Run tests before declaring completion
  - Handle errors with meaningful messages
  - Support Unicode in strings
  - Maintain Lisp-style prefix syntax

- **Ask first:**
  - Adding dependencies
  - Changing syntax significantly
  - Adding complex features beyond v1 scope

- **Never:**
  - Break backward compatibility without notice
  - Use eval on untrusted input without sandboxing
  - Leave TODO or FIXME without tracking as issue

## Open Questions

- [ ] Should strings support escape sequences (\n, \t, etc.)? → Yes, v1
- [ ] Should we support multi-line strings? → Yes, v1

## Future Roadmap (post-v1)

- OOP with classes and inheritance
- Macros (hygienic)
- Networking: TCP sockets, HTTP server
- Linux system integration: processes, signals, file descriptors
- Async/event loop (JS-style)
- Web crawling library
- Package manager
- Web framework (Sinatra-like)
- Static hosting capabilities
- File watching / hot reload
