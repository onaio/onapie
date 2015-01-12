from subprocess import call
from unittest import TestCase


class TestStyle(TestCase):

    def test_flake8(self):
        result = call(['flake8', '--exclude', 'migrations,src,env', '.'])
        self.assertEqual(result, 0, "Flake8 ain't happy with your code style.")
