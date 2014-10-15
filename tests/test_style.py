from subprocess import call
from unittest import TestCase


class TestStyle(TestCase):

    def test_flake8(self):
        result = call(['flake8', '--exclude', 'migrations,src', '.'])
        self.assertEqual(result, 0, "Code is not flake8.")
