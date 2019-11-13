from Poly.ZPoly import ZPoly
import pprint
import random


# word in division, gcd for polynomials

def finite_field_example():
    print("GF(16)")

    
    P = ZPoly( [1,1,0,0,1], 2 )
    S = ZPoly( [0,1], 2 )
    out = ZPoly( [1], 2 )
    
    F = {0:P}
    
    for i in range(1,16):
        F[i] = out
        out = (out * S) % P
        
    pprint.pprint(F)
    
    print()
    for i in range(10):
        N = random.sample(list(F),2)
        z = F[0]
        a = F[N[0]]
        b = F[N[1]]
        print( ( a * b ) % z ) 
        print()
    
if __name__ == '__main__':
    
    finite_field_example()