from Rational import Rational
from Poly import QPoly
from Utility import unit_test

r = Rational(32,7)
P = QPoly(["3/2",0,1,"11.6"])


i_minitests = [ (P+r, "58/5x^3 + x^2 + 85/14" ),
                (r+P, "58/5x^3 + x^2 + 85/14" ),
              ]

print(r)
print(P)

print("\nTest Objects Together")
unit_test(i_minitests)