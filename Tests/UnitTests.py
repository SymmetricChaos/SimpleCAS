from Rational import Rational
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





unit_test(rminitests)