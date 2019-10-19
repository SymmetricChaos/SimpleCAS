from Poly.QPoly import QPoly
from Rational import Rational, rational_gcd
from Utility import factorization
from itertools import product
from collections import Counter

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





def poly_egcd(P,Q):
    """Bézout's identity for two polynomials"""
    assert type(P) == QPoly
    assert type(Q) == QPoly
    
    if Q.degree() > P.degree():
        P,Q = Q,P

    r0, r1 = P,Q
    s0, s1 = 1,0
    t0, t1 = 0,1
    
    while r1 != QPoly([0]):
        q = r0//r1
        r0,r1 = r1, r0 - q*r1
        s0,s1 = s1, s0 - q*s1
        t0,t1 = t1, t0 - q*t1
    
    return r0.primitive_part, s0, t0


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





def complete_the_square(poly):
    """Returns a tuple (x,y,z) such that x(y)^2+z is equal to poly"""
    assert type(poly) == QPoly
    assert len(poly) == 3, "Must be a quadratic"
    assert poly[1] % 2 == Rational(0), "Linear coefficient must be even"
    a = poly[2]
    h = poly[1]//(2*a)
    k = poly[0]-a*(h*h)
    
    return a, QPoly( [h,1] ), k


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
    """Modified kroneck factorization"""
    deg = poly.degree()
    fdeg = deg//2
    
    # Skip constant and linear terms, these could be factored using Kronecker's
    # method but we will remove them before this.
    if fdeg <= 1:
        return [poly]
    
    
    # TODO: Need a better way to choose points
    # TODO: should search positive and negative and try to find values that 
    # evaluate to small numbers
    points = [i for i in range(fdeg+1)]
    val_at_points = [poly(i) for i in points]
    
    
    F = [reversed(factorization(e.n,negatives=True)) for e in val_at_points]

    for evs in product(*F):
        L = lagrange_interpolation(points,evs)


        # Ignore factors with negative leading coefficient
        if L[-1] < 0:
            continue
        # Ignore trivial factors
        if L == QPoly([1]) or L == poly:
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
    if P.content != 1:
        out.append(QPoly([P.content]))
        P = P.primitive_part

    # Use rational roots to find linear factors
    # A root may have multiplicity so we check each root until it doesn't
    # divide anymore
    lin = rational_roots(poly)
    for f in lin:
        while True:
            d,m = divmod(P,QPoly( [-f.n,f.d] ))
            if m == QPoly( [0] ):
                out.append(QPoly( [-f.n,f.d] ))
                P = P // out[-1]
            else:
                break

    # Then do some Kronecker factorization on what's left
    out += kronecker_factorization(P)
    out.sort(key=len,reverse=True)
    
    return out


# Deal with sorting
def factored_form(poly):
    F = poly_factor(poly)
    C = Counter(F)

    out = ""

    for poly,pwr in C.items():
        if str(poly) == "1":
            continue
        if len(poly) == 1:
            out += f"{poly}"
        elif pwr == 1:
            out += f"({poly}) "
        else:
            out += f"({poly})^{pwr} "

    print(out)





if __name__ == '__main__':
    
    S = QPoly([-1,1]) * QPoly([5,-7,3]) * QPoly([-1,1]) * QPoly([7,2]) * 3
    print(S)
    print("Factored version of S")
    factored_form(S)
    
#    x = [1,2,3]
#    y = [1,8,27]
#    print(f"Lagrange Interpolation of\nx = {x}\ny = {y}")
#    print(lagrange_interpolation(x,y))
#
#
#    print()
#    print()
#    S = QPoly( [-1,1] ) * QPoly( [3,3,3] ) * QPoly( [-1,2] ) * QPoly( [1,1,0,1] )
#    print(f"S = {S}")
#    print(f"Factorization of S: {poly_factor(S)}")
#
#
#    print()
#    print()
#    S = QPoly( [2,1,1,0,1,1] )
#    print(f"S = {S}")
#    print(f"Factorization of S: {poly_factor(S)}")
#
#
#    print()
#    print()
#    print("Completing the Square")
#    R = QPoly( [27,12,3] )
#    print(f"R = {R}")
#    sq = complete_the_square(R)
#    print(sq)
#    print(f"{sq[0]}({sq[1]})^2 + {sq[2]}")
#    
#    
#    print()
#    print()
#    print("Polynomial GCD")
#    A = QPoly( [6,13,8,1] ) * QPoly( [3,0,0,-2] ) * QPoly( [1,1,1] )
#    B = QPoly( [-6,-11,-4,1] ) * QPoly( [3,0,0,-2] )
#    print(f"A = {A}")
#    print(f"B = {B}")
#    print(f"poly_gcd(A,B) = {poly_gcd(A,B)}")
#    
#
#    print()
#    print()
#    print("Polynomial eGCD")
##    print(f"A = {A}")
##    print(f"B = {B}")
#    g, u, v = poly_egcd(A,B)
##    print(f"g = {g}")
#    print(f"u = {u}")
#    print(f"v = {v}")
#    bid = (A*u + B*v).primitive_part
#    print(f"(A*u + B*v) = {bid}")
#    print("The GCD is defined only up to scalar multiplication so only the primitive part of Bézout's identity is shown")