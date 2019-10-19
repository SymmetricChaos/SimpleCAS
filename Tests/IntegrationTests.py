from Rational import Rational
from Poly import QPoly
from Utility import unit_test

r = Rational(32,7)
P = QPoly(["3/2",0,1,"11.6"])


i_minitests = [ (P+r, "58/5x^3 + x^2 + 85/14" ),
                (r+P, "58/5x^3 + x^2 + 85/14" ),
                (P*r, "1856/35x^3 + 32/7x^2 + 48/7" ),
                (r*P, "1856/35x^3 + 32/7x^2 + 48/7" ),
              ]



print("\nTest Objects Together")
unit_test(i_minitests)