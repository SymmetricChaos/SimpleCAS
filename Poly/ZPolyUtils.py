from Utility import mod_inv
from Poly import ZPoly
from random import randint

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



if __name__ == '__main__':
    
    secret = 345
    min_parts = 3
    total_parts = 6
    F = 1613
    pts = make_shamir_secret(secret,min_parts,total_parts,F)
    
    print(f"We will use Shamir's method to break up the secret number {secret} into {total_parts} pieces such any {min_parts} pieces can be used to get the secret.")
    print(f"\nTo do this we create a random polynomial of degree {min_parts} that has constant term {secret} over a finite field and choose {total_parts} points on it.")
    
    print(f"\nUse a finite field of order {F} we get the points:")
    for i in pts:
        print(i)
    
    print(f"\nInterpolation gives us the answer:")
    print(get_shamir_secret(pts,F))