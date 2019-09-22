from Poly.QPoly import QPoly
from Rational import Rational, rational_gcd

def content(poly):
    """Rational GCD of the coefficients, negative if leading coef is negative,
    makes the polynomial have integer coefs"""
    assert type(poly) == QPoly
    return rational_gcd(poly.coef) * (-1 if poly.coef[-1] < 0 else 1)


def primitive(poly):
    """Divide out the content"""
    assert type(poly) == QPoly
    cont = content(poly)
    return poly//cont

    
def monic(poly):
    """Return the monic version of the polynomial with positive leading coef"""
    assert type(poly) == QPoly
    return poly//poly.coef[-1]


def lagrange_interpolation(X,Y):
    """Lagrange Polynomial"""
    final = QPoly([0])
    for x,y in zip(X,Y):
        out = QPoly([y])
        for m in X:
            if m != x:
                d = Rational(1,(x-m))
                P = QPoly([-m,1])
                out *= P*d
        final += out
    return final



if __name__ == '__main__':
    Q = QPoly([-5,1,-3])
    print(f"\nQ          = {Q}")
    print(f"integral   = {Q.integral(0)}")
    print(f"derivative = {Q.derivative()}")
    print(lagrange_interpolation([1,2,3],[1,8,27]))
    
    P = QPoly([0,2,0,-6,-2])
    P //= 3
    P[1] = Rational(3,5)
    print(f"\nP            = {P}")
    print(f"content(P)   = {content(P)}")
    print(f"primitive(P) = {primitive(P)}")