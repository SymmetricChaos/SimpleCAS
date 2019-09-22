from Poly.QPoly import QPoly
from Rational import Rational, rational_gcd
from Utility import factorization
from itertools import product

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


def kronecker_factorization(poly):
    # Degree of poly
    deg = poly.degree()
    # Degree of factor
    fdeg = deg//2 
    
    points = [i for i in range(fdeg+1)]
    ev = [poly(i) for i in points]
    F = [factorization(e.n//e.d) for e in ev]

    for evs in product(*F):
        L = lagrange_interpolation(points,evs)
        # Skip possible linear factors
        if len(L) == 1:
            continue
        # Skip possible rational factors
        if any(x.d != 1 for x in L):
            continue
        
        # Try the division
        q,r = divmod(poly,L)
        
        # Remainder must be zero
        if r == QPoly([0]):
            # all cofficients must be integers
            if all(x.d == 1 for x in q):
                print(f"{poly}\n{L}\n{q}\n")




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
    
    R = QPoly([2,1,1,0,1,1])
    kronecker_factorization(R)