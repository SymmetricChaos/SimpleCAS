from Utility import mod_inv, prime_factorization
from Poly import ZPoly, ZPolyProd, zpoly_gcd
from random import randint, sample
from itertools import product

def zpoly_lagrange_interpolation(X,Y,M):
    """Use lagrange polynomial to interpolate points of a zpoly"""
    final = ZPoly([0],M)
    for x,y in zip(X,Y):
        out = ZPoly([y],M)
        for m in X:
            if m != x:
                d = mod_inv(x-m,M)
                P = ZPoly([-m,1],M)
                out *= P*d
        final += out
    return final


def make_shamir_secret(secret,k,n,M):
    """Take a number and produce k ordered pairs such that n can be used to reconstruct the number"""
    if secret > M:
        raise ValueError("secret cannot be less than M or information will be lost")
    if k > n:
        raise ValueError("parts needed to reconstruct cannot be greater than total points created")
    if len(prime_factorization(M)) != 1:
        raise ValueError("Order for finite field must be a prime")
        
    co = [secret] + [randint(0,M-1) for i in range(k-1)]

    P = ZPoly( co, M )
    
    pts = []
    for i in range(n):
        r = randint(0,M-1)
        pts.append( (r,P(r)) )
    
    return pts


def get_shamir_secret(pts,M):
    """Take some ordered and reconstruct the secret number"""
    X = [i[0] for i in pts]
    Y = [i[1] for i in pts]
    
    return zpoly_lagrange_interpolation(X,Y,M)[0]   


## TODO: primitive and monic modes
## TODO: support for M == None
def zpoly_egcd(a, b):
    """Extended Euclidean Algorithm for ZPolys"""
    M = a.M
    if a == ZPoly([0],M):
        return (b, ZPoly([0],M), ZPoly([1],M))
    else:
        g, y, x = zpoly_egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def square_free_decomposition(poly):
    assert type(poly) == ZPoly
    print("!")
    
    if len(poly) == 1:
        print(poly)
        return poly
    
    d = poly.derivative()
    
    if d != ZPoly([0],poly.M):
        g = zpoly_gcd(poly,d)
        print(g)
        if g == ZPoly([1],poly.M):
            print("!!!")
            print(poly)
            return poly
        else:
            print(poly//g)
            return square_free_decomposition(g)
        
    else:
        pwr = 1
        while True:
            for g in all_monic_zpolys(poly.M):
                p = g**(poly.M**pwr)
                if p == poly and g.derivative() != ZPoly([0],poly.M):
                    return square_free_decomposition(g)
                if len(p) > len(poly):
                    pwr += 1
                    break


def all_monic_zpolys(M):
    """Generator for all monic polynomials over M"""
    
    yield ZPoly([1],M)
    co = [i for i in range(M)]
    
    l = 1
    while True:
        P = product(co,repeat=l)
        for p in P:
            coefs = [i for i in reversed((1,)+p)]
            yield ZPoly(coefs,M)
        l += 1


def all_zpolys(M):
    """Generator for all polynomials over M"""
    
    co = [i for i in range(M)]
    for c in co:
        yield ZPoly([c],M)
    
    l = 1
    while True:
        P = product(co,repeat=l)
        for p in P:
            for c in co[1:]:
                coefs = [i for i in reversed((c,)+p)]
                yield ZPoly(coefs,M)
        l += 1


def all_irreducible_mod2():
    """Sieve of Eratosthenes for polynomials in Z/2Z"""
    out = [ZPoly([1,1,1],2)]
    
    yield ZPoly([0,1],2)
    
    yield ZPoly([1,1],2)
    
    all_p = all_zpolys(2)
    for i in range(7):
        next(all_p)
    
    while True:
        poly = next(all_p)
        
        if poly(0) == poly(1) == 1:

            for i in out:
                
                if len(i) > len(poly) // 2:
                    out.append(poly)
                    yield poly
                    break
                
                r = poly%i
                if r == ZPoly([0],2):
                    out.append(poly)
                    yield poly
                    break





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


    print("\n\nSquare-Free Decomposition")
    P = ZPoly([1,0,2,2,0,1,1,0,2,2,0,1],3)
    print(P)
    print(square_free_decomposition(P))


    print("\nAll monic polynomials over Z/3Z with degree less than 3")
    for poly in all_monic_zpolys(3):
        if len(poly) > 3:
            break
        print(poly)

    print("\nAll irreducible polynomials over Z/2Z with degree less than 6")
    for poly in all_irreducible_mod2():
        if len(poly) > 6:
            break
        print(poly)
        
    
    print("\nTest Sorting Polynomials")
    P = ZPoly([1,4,1],5) 
    Q = ZPoly([1,2,3],5)
    R = ZPoly([4,1],5) 
    S = ZPoly([3],5)
    T = ZPoly([0,0,2],5)
    U = ZPoly([0,1,0,0,0,1],5)
    
    L = [P,Q,R,S,T,U]
    print(L)
    print(sorted(L))