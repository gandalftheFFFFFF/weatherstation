import unittest

# Run from project dir: nosetests test/

class TestSomething(unittest.TestCase):
    
    def test_something(self):
        self.assertTrue(1, 1)

    def test_somthing_broken(self):
        self.assertTrue(1, 2)

