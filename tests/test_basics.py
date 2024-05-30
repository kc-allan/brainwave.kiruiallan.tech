import unittest
from flask import current_app
from app import create_app
from app.models import storage

class BasicsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        storage.__init__()
        
    def tearDown(self) -> None:
        storage.close()
        self.app_context.pop()
    
    def test_app_exists(self):
        self.assertFalse(current_app is None)
        
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])