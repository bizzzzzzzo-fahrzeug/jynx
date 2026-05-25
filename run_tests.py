#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
import tests.test_lexer
import tests.test_parser
import tests.test_interpreter

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(tests.test_lexer))
    suite.addTests(loader.loadTestsFromModule(tests.test_parser))
    suite.addTests(loader.loadTestsFromModule(tests.test_interpreter))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
