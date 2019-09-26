from Rational import Rational
import unittest

# TODO: Turn this into proper unit tests
# test:  subtration, division, error catch, methods

class TestRationals(unittest.TestCase):
    
    def test_eq(self):
        self.assertEqual(Rational(32,7),Rational(32,7))

    def test_simp(self):
        self.assertEqual(Rational(6188,7140),Rational(13,15))

    def test_mul(self):
        r1 = Rational(728,590)
        r2 = Rational(137,730)
        pr = Rational(24934,107675)
        self.assertEqual(r1*r2,pr)
        
    def test_sum(self):
        r1 = Rational(687,889)
        r2 = Rational(211,170)
        sm = Rational(304369,151130)
        self.assertEqual(r1+r2,sm)


if __name__ == '__main__':
    unittest.main()
