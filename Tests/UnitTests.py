from Rational import Rational
from Poly import QPoly, ZPoly, RFunc
from Utility import unit_test


######################
## Rational Numbers ##
######################

r = Rational(192,42)
s = Rational(12,2)
t = Rational(17,9)
u = Rational(-423,13)
v = Rational(1,144)
w = Rational(1,477)

r_minitests = [ (r, "32/7" ), #simplify
                (s , "6"), # integer case
                (t , "17/9"),
                (1/r, "7/32"), # inversion
                (s.inv(), "1/6"), # inversion
                (r**0, "1"), #power
                (r**3, "32768/343"), #power
                (s%2, "0"), # modulus
                (r/t, "288/119"), # division
                (r+s, "74/7"), # addition
                (s*t, "34/3"), # multiplication
                (-r, "-32/7"), # negation
                (r-s, "-10/7"), #subtraction
                (u.digits(5),"-32.53846"), # decimals for negatives
                (r.digits(5),"4.57142"),   # decimals for positives
                (r.pretty_name,"$\\dfrac{32}{7}$"), #pretty name
                (s.decimal_expansion,"6"), # expansion of integer
                (u.decimal_expansion,"-32.(538461)"), # expansion for negative
                (v.decimal_expansion,"0.0069(4)"), # expansion with some nonrepeating part
                (w.decimal_expansion,"0.(0020964360587)")
              ]



##################
## Polynonmials ##
##################

P = QPoly(["3/2",0,1,"11.6"])
Q = QPoly([-5,1])

p_minitests = [ (P, "58/5x^3 + x^2 + 3/2"),
                (Q, "x - 5"),
                (P+Q, "58/5x^3 + x^2 + x - 7/2"),
                (P*Q, "58/5x^4 - 57x^3 - 5x^2 + 3/2x - 15/2"),
                (P**0, "1"),
                (P**2, "3364/25x^6 + 116/5x^5 + x^4 + 174/5x^3 + 3x^2 + 9/4"),
                (P.integral(2), "29/10x^4 + 1/3x^3 + 3/2x + 2"),
                (P.derivative(), "174/5x^2 + 2x"),
                (P.content, "1/10"),
                (P.primitive_part, "116x^3 + 10x^2 + 15"),
                (P.monic_part, "x^3 + 5/58x^2 + 15/116"),
                (P/Q,"(58/5x^3 + x^2 + 3/2) / (x - 5)")
              ]



########################
## Rational Functions ##
########################

R = RFunc( [1,1], [2,3] )
S = RFunc( [-28,16,-16,16,12],[-2,5,-6,6,-4,1] )
T = RFunc( [3,5,1], [1] )
U = RFunc( ["1/8"], ["1/3","5/4"] )

rf_minitests = [ (R, "(x + 1) / (3x + 2)"),
                 (S, "(12x + 28) / (x^2 - 3x + 2)"), #simplify
                 (T, "x^2 + 5x + 3"), # denominator one
                 (U, "1/8 / (5/4x + 1/3)"),
                 (U.primitive_part, "12 / (120x + 32)")
               ]

###########
## ZPoly ##
###########


F = 27
P = ZPoly( [50,0,-8,121,9], F )
Q = ZPoly( [25,1,8], F )
#print(f"P = {P} (mod {F})")
#print(f"Q = {Q} (mod {F})")
#print()
#print(f"P//Q = {P//Q}")
#print(f"P%Q  = {P%Q}")

z_minitests = [ (P, "9x^4 + 13x^3 + 19x^2 + 23"),
                (Q, "8x^2 + x + 25"),
                (P+Q, "9x^4 + 13x^3 + x + 21"),
              ]

#######################
## Integration Tests ##
#######################

r = Rational(32,7)
P = QPoly(["3/2",0,1,"11.6"])
Q = QPoly([2])
R = RFunc( [1,1], [2,3] )

i_minitests = [ (P+r, "58/5x^3 + x^2 + 85/14" ),
                (r+P, "58/5x^3 + x^2 + 85/14" ),
                (P*r, "1856/35x^3 + 32/7x^2 + 48/7" ),
                (r*P, "1856/35x^3 + 32/7x^2 + 48/7" ),
                (P//r, "203/80x^3 + 7/32x^2 + 21/64" ),
                (r//Q, "16/7"),
                (R+P, "(174/5x^4 + 131/5x^3 + 2x^2 + 11/2x + 4) / (3x + 2)"),
                (P+R, "(174/5x^4 + 131/5x^3 + 2x^2 + 11/2x + 4) / (3x + 2)"),
              ]






print("\nTest Rational")
unit_test(r_minitests)
print("\nTest QPoly")
unit_test(p_minitests)
print("\nTest RFunc")
unit_test(rf_minitests)
print("\nTest ZPoly")
unit_test(z_minitests)
print("\nIntegration Tests")
unit_test(i_minitests)