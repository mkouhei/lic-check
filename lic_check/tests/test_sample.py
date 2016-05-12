"""lic_check.tests.test_sample."""
import unittest
import sys
from lic_check import sample


class SampleTests(unittest.TestCase):
    """lic_check.sample tests."""

    def test_hello(self):
        """hello() test."""
        self.assertEqual(sample.hello('Alice'), 'Hello, Alice.')

    def test_bmi(self):
        """bmi test."""
        self.assertTrue(18.5 <= sample.bmi(1.68, 67.0) < 25)

    def test_bmi_zero_devide(self):
        """bmi zero devide."""
        with self.assertRaises(ZeroDivisionError) as exc:
            sample.bmi(0, 67.0)
        if sys.version_info < (3, 0):
            self.assertIsNotNone(exc.exception.message)
        else:
            self.assertIsNotNone(exc.exception.__str__())
