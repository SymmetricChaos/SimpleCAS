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


if __name__ == '__main__':
    F = 1613
    X = [2,4,5]
    Y = [1942,3402,4414]
    
    print(lagrange_interpolation(X,Y,F))