#!/usr/bin/env python3
import sys
from jynx.repl import REPL


def main():
    repl = REPL()
    if len(sys.argv) > 1:
        if sys.argv[1] == "--repl":
            repl.run_repl()
        else:
            path = sys.argv[1]
            code = repl.run_file(path)
            sys.exit(code)
    else:
        repl.run_repl()


if __name__ == "__main__":
    main()
