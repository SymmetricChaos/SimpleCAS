from Rational import Rational
from Poly import QPoly, QPolyQuo
from Utility import unit_test

r = Rational(32,7)
P = QPoly(["3/2",0,1,"11.6"])
Q = QPoly([2])
R = QPolyQuo( [1,1], [2,3] )

i_minitests = [ (P+r, "58/5x^3 + x^2 + 85/14" ),
                (r+P, "58/5x^3 + x^2 + 85/14" ),
                (P*r, "1856/35x^3 + 32/7x^2 + 48/7" ),
                (r*P, "1856/35x^3 + 32/7x^2 + 48/7" ),
                (P//r, "203/80x^3 + 7/32x^2 + 21/64" ),
                (r//Q, "16/7"),
                (R+P, "(174/5x^4 + 131/5x^3 + 2x^2 + 11/2x + 4) / (3x + 2)"),
                (P+R, "(174/5x^4 + 131/5x^3 + 2x^2 + 11/2x + 4) / (3x + 2)"),
              ]



print("\nTest Objects Together")
unit_test(i_minitests)