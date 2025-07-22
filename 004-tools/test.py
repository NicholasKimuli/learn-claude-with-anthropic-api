import unittest
from main import calculate_pi

class TestPiCalculation(unittest.TestCase):
    
    def test_default_precision(self):
        """Test that the default precision is 5 digits"""
        pi_value = calculate_pi()
        self.assertEqual(pi_value, 3.14159)
    
    def test_custom_precision(self):
        """Test calculating pi with different precision levels"""
        self.assertEqual(calculate_pi(2), 3.14)
        self.assertEqual(calculate_pi(4), 3.1416)
        self.assertEqual(calculate_pi(6), 3.141593)
    
    def test_against_known_value(self):
        """Test against the known value of pi to 10 digits"""
        # The actual value of pi to 10 digits is 3.1415926536
        pi_10_digits = calculate_pi(10)
        self.assertAlmostEqual(pi_10_digits, 3.1415926536, places=10)
    
    def test_return_type(self):
        """Test that the function returns a float"""
        self.assertIsInstance(calculate_pi(), float)

if __name__ == "__main__":
    unittest.main()