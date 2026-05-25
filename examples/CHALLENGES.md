# Jynx — 20 Challenges (Easy → Extra Hard)

## Level 1 — Warm-up (Easy)

**1** Print `"hello world"` using print.

**2** Compute `((10 + 5) × 3) − (20 ÷ 4)` in one expression.

**3** Define a variable `name` with your name, then print `"Hello, <name>!"`.

**4** Write an `if` expression that prints `"even"` if a number is even, `"odd"` otherwise. (Hint: `(% n 2)`)

**5** Write a `cond` that classifies a number as `"negative"`, `"zero"`, or `"positive"`.

---

## Level 2 — Functions (Medium)

**6** Define a function `(double x)` that returns `x * 2`. Call it on 21.

**7** Define a recursive function `(sum-to n)` that sums numbers from 1 to n. `(sum-to 100)` → 5050.

**8** Write a lambda that takes two numbers and returns the larger one. Call it immediately: `((lambda ...) 10 20)`.

**9** Define `(range n)` that returns a list from n down to 1. Then use it with `map` and `double`.

**10** Use `filter` to return only numbers > 5 from `(list 3 7 1 9 4 6)`.

---

## Level 3 — Closures & Lists (Hard)

**11** Make a closure `(make-adder x)` that returns a function adding `x` to its argument. Test: `(define add5 (make-adder 5))`, then `(add5 10)`.

**12** Write `(flatten lst)` that flattens nested lists: `(flatten (list 1 (list 2 3) 4))` → `(1 2 3 4)`.

**13** Implement `(take n lst)` returning first n elements, and `(drop n lst)` skipping first n.

**14** Write `(zip a b)` that pairs elements: `(zip (list 1 2 3) (list "a" "b" "c"))` → `((1 "a") (2 "b") (3 "c"))`.

**15** Make a counter with `(get-count)`, `(inc)`, `(reset)` using closures and message passing.

---

## Level 4 — Advanced Algorithms (Extra Hard)

**16** Write `(merge-sort lst)` — merge sort. You'll need `(merge a b)` helper.

**17** Implement `(permutations lst)` that returns all permutations of a list.

**18** Write `(subsets lst)` that returns all subsets (power set) of a list.

**19** Implement `(eval-expr expr)` that evaluates simple math expressions like `(+ 1 (* 2 3))` represented as lists. Use the Jynx interpreter itself!

**20** Write a `(time fn arg)` that measures and prints how long `fn` takes on `arg`. This requires using Python's time via a new builtin — extend the language by adding `(clock)` to builtins.py that returns current time in seconds, then implement timing in Jynx itself.

---

### How to test

```bash
# In REPL
python3 main.py

# Or write a file and run it
python3 main.py my_challenge.jynx
```
