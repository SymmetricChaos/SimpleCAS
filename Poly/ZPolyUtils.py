from Utility import mod_inv, prime_factorization
from Poly import ZPoly, ZPolyProd
from random import randint, sample


def zpoly_lagrange_interpolation(X,Y,F):
    """Lagrange Polynomial"""
    final = ZPoly([0],F)
    for x,y in zip(X,Y):
        out = ZPoly([y],F)
        for m in X:
            if m != x:
                d = mod_inv(x-m,F)
                P = ZPoly([-m,1],F)
                out *= P*d
        final += out
    return final


def make_shamir_secret(secret,k,n,F):

    if secret > F:
        raise ValueError("secret cannot be less than F or information will be lost")
    if k > n:
        raise ValueError("parts needed to reconstruct cannot be greater than total points created")
    if len(set(prime_factorization(F))) != 1:
        raise ValueError("Order for finite field must be a prime power")
        
    co = [secret] + [randint(0,F-1) for i in range(k-1)]

    P = ZPoly( co, F )
    
    pts = []
    for i in range(n):
        r = randint(0,F-1)
        pts.append( (r,P(r)) )
    
    return pts


def get_shamir_secret(pts,F):
    
    X = [i[0] for i in pts]
    Y = [i[1] for i in pts]
    
    return zpoly_lagrange_interpolation(X,Y,F)[0]





# Note that polynomial GCDs are unique only up to scalar multiplication so the
# output is standardized as being monic
def zpoly_gcd(P,Q):
    """GCD of two polynomials over the same finite field"""
    assert type(P) == ZPoly
    assert type(Q) == ZPoly
    assert P.F == Q.F
    
    if Q.degree() > P.degree():
        P,Q = Q,P
        
    # Check if we reached the end
    if Q == ZPoly([0], P.F):
        return P.monic_part
    if P == ZPoly([0], P.F):
        return Q.monic_part
    
    else:
        g = zpoly_gcd(P % Q, Q)
        return g.monic_part



def square_free_factorization(poly):
    assert type(poly) == ZPoly
#    C = poly[-1]
    M = poly.monic_part
    
    c = zpoly_gcd(M,M.derivative())
    w = M//c
    
    one = ZPoly([1],poly.F)
    R = ZPolyProd([one])
    i = 1
    
    while w != one:
        y = zpoly_gcd(w,c)
        z = w//y
        for ctr in range(i):
            R *= z
        w = y
        c = c//y
        i += 1
    print(R)
    print(c)


if __name__ == '__main__':
    
    secret = 72697680
    min_parts = 4
    total_parts = 6
    F = 104395301
    pts = make_shamir_secret(secret,min_parts,total_parts,F)
    
    print(f"We will use Shamir's method to break up the secret number {secret} into {total_parts} pieces such any {min_parts} pieces can be used to get the secret.")
    print(f"\nTo do this we create a random polynomial of degree {min_parts} that has constant term {secret} over a finite field and choose {total_parts} points on it.")
    
    print(f"\nUsing a finite field of order {F} we get the points:")
    for i in pts:
        print(i)
    
    print(f"\nPicking three of those we can reconstruct the answer:")
    rpts = sample(pts,min_parts)
    print(get_shamir_secret(rpts,F))


    print("\n\nGCD of ZPolys")
    P = ZPoly( [1,2,3], 5) * ZPoly( [2,4], 5)
    Q = ZPoly( [1,2,3], 5)
    print(P)
    print(Q)
    print(zpoly_gcd(P,Q))

    print("\n\nSquare-Free Factorization")
    P = ZPoly([1,0,2,2,0,1,1,0,2,2,0,1],3)
    print(P)
    square_free_factorization(P)

    print()