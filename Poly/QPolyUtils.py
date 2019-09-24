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


def rational_roots(poly):
    """Find all rational roots"""
    A0 = factorization(poly[0].n,negatives=True)
    Af = factorization(poly[-1].n,negatives=True)
    R = set()
    for i in A0:
        for j in Af:
            if poly(Rational(i,j)) == 0:
                R.add(Rational(i,j))
    return R


def kronecker_factorization(poly):
    deg = poly.degree()
    fdeg = deg//2
    
    
    # TODO: Need a better way to choose points
    # TODO: should search positive and negative and try to find values that 
    # evaluate to small numbers
    points = [i for i in range(fdeg+1)]
    val_at_points = [poly(i) for i in points]
    
    ## Probably better to use rational roots to search for linear factors
    # Check for linear factors
    # If we find one divide it out an continue
    for p,v in enumerate(val_at_points):
        if v == 0:
            P = QPoly([-p,1])
            B = kronecker_factorization(poly//P)
            return [P] + B
    
    F = [reversed(factorization(e.n,negatives=True)) for e in val_at_points]

    for evs in product(*F):
        L = lagrange_interpolation(points,evs)

        # Ignore trivial factors
        if L == QPoly([1]) or L == poly:
            continue
        if L == QPoly([-1]) or L == -poly:
            continue
        # Skip possible factors with non-integer coefficients
        if any(x.d != 1 for x in L):
            continue
        
        # Try the division
        q,r = divmod(poly,L)
        
        # Remainder must be zero
        if r == QPoly([0]):
            # all cofficients of the quotient must be integers
            if all(x.d == 1 for x in q):
                A = kronecker_factorization(L)
                B = kronecker_factorization(q)
                return A + B
            
    return [poly]


def poly_factor(poly):
    
    P = poly.copy()
    
    out = []
    # Divide out the content
    if P.content() != 1:
        out.append(P.content())
        P = P.primitive()
        
        print(f"Removed constant factor: {out[-1]}")
    
    # Use rational roots to find linear factors
    lin = rational_roots(poly)
    for f in lin:
        if f.d == 1:
            out.append(QPoly( [-f,1] ))
            P = P // out[-1]
            print(f"Removed linear factor: {out[-1]}")

    # Then do some Kronecker factorization on what's left
    out += kronecker_factorization(P)

    return out


if __name__ == '__main__':
    x = [1,2,3]
    y = [1,8,27]
    print(f"Lagrange Interpolation of\nx = {x}\ny = {y}")
    print(lagrange_interpolation(x,y))
    
    
    ## TODO: Find out why factoring sometimes fails or gives weird answers
    print()
    S = QPoly( [-1,1] ) * QPoly( [3,1] ) * QPoly( [3,3,3] )
    print(rational_gcd(S.coef))
    print(f"S = {S}")
    print(f"Factorization of S: {poly_factor(S)}")
    
    print()
    S = -S
    print(f"S = {S}")
    print(f"Factorization of S: {poly_factor(S)}")

    print()
    S = QPoly( [2,1,1,0,1,1] )
    print(f"S = {S}")
    print(f"Factorization of S: {poly_factor(S)}")
