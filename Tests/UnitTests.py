from Rational import Rational
from Poly import QPoly
from Utility import unit_test


r = Rational(192,42)
s = Rational(12,2)
t = Rational(17,9)

rminitests = [ (r, "32/7" ),
               (s , "6"),
               (t , "17/9"),
               (1/r, "7/32"),
               (s.inv(), "1/6"),
               (r**3, "32768/343"),
               (s%2, "0"),
               (r/t, "288/119"),
               (r+s, "74/7"),
               (s*t, "34/3"),
               (-r, "-32/7"),
               (r-s, "-10/7")
            ]

P = QPoly(["3/2",0,1,"11.6"])
Q = QPoly([-5,1])

pminitests = [ (P, "58/5x^3 + x^2 + 3/2"),
               (Q, "x - 5"),
               (P+Q, "58/5x^3 + x^2 + x - 7/2"),
               (P*Q, "58/5x^4 - 57x^3 - 5x^2 + 3/2x - 15/2"),
               (P**2, "3364/25x^6 + 116/5x^5 + x^4 + 174/5x^3 + 3x^2 + 9/4"),
               (P.integral(0), "29/10x^4 + 1/3x^3 + 3/2x"),
               (P.derivative(), "174/5x^2 + 2x"),
               (P.content, "1/10"),
               (P.primitive_part, "116x^3 + 10x^2 + 15")
            ]




print("\nTest Rational")
unit_test(rminitests)
print("\nTest QPoly")
unit_test(pminitests)