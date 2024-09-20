import unittest
from flask import Flask

def register(app: Flask):
    @app.cli.command
    def test():
        """Run unit tests"""
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)