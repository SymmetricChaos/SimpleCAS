from Utility import mod_inv
from Poly import ZPoly

def lagrange_interpolation(X,Y,F):
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

# Use lagrange interpolation for Shamir's secret sharing

if __name__ == '__main__':
    F = 1613
    X = [1,2,3,4,5]
    Y = [1494,329,965,176,1188,775]
    
    print(lagrange_interpolation(X,Y,F))