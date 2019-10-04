from RationalFunc import RFunc
from Poly import qpoly_roots

def rfunc_roots(rfunc):
    """Approximate roots of a rational function"""
    assert type(rfunc) == RFunc
    return qpoly_roots(rfunc.N)


# TODO find asymptotes of a rational function
def asymptote(rfunc):
    """Approximate asymptotes of a rational function"""
    assert type(rfunc) == RFunc
    dN = rfunc.N.degree()
    dD = rfunc.D.degree()
    
    if dN > dD:
        pass
    elif dN == dD:
        pass
    elif dN < dD:
        pass
    
if __name__ == '__main__':
    from random import sample
    coefs = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
    co1 = sample(coefs,6)
    co2 = sample(coefs,6)
    R = RFunc( co1, co2 )
    print(f"R = {R}")
    print(rfunc_roots(R))