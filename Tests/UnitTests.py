from Rational import Rational
from Poly import QPoly
from RationalFunc import RFunc
from Utility import unit_test


r = Rational(192,42)
s = Rational(12,2)
t = Rational(17,9)
u = Rational(-423,13)
v = Rational(1,144)
w = Rational(1,477)


r_minitests = [ (r, "32/7" ),
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
               (r-s, "-10/7"),
               (u.digits(5),"-32.53846"), # make sure decimals for natives work
               (r.digits(5),"4.57142"),
               (r.pretty_name,"$\\dfrac{32}{7}$"),
               (s.decimal_expansion,"6"),
               (u.decimal_expansion,"-32.(538461)"),
               (v.decimal_expansion,"0.0069(4)"),
               (w.decimal_expansion,"0.(0020964360587)")
            ]

P = QPoly(["3/2",0,1,"11.6"])
Q = QPoly([-5,1])

p_minitests = [ (P, "58/5x^3 + x^2 + 3/2"),
               (Q, "x - 5"),
               (P+Q, "58/5x^3 + x^2 + x - 7/2"),
               (P*Q, "58/5x^4 - 57x^3 - 5x^2 + 3/2x - 15/2"),
               (P**2, "3364/25x^6 + 116/5x^5 + x^4 + 174/5x^3 + 3x^2 + 9/4"),
               (P.integral(2), "29/10x^4 + 1/3x^3 + 3/2x + 2"),
               (P.derivative(), "174/5x^2 + 2x"),
               (P.content, "1/10"),
               (P.primitive_part, "116x^3 + 10x^2 + 15"),
               (P.monic_part, "x^3 + 5/58x^2 + 15/116")
            ]


R = RFunc( [1,1], [2,3] )

rf_minitests = [ (R, "(x + 1) / (3x + 2)")
            ]

print("\nTest Rational")
unit_test(r_minitests)
print("\nTest QPoly")
unit_test(p_minitests)
print("\nTest RFunc")
unit_test(rf_minitests)