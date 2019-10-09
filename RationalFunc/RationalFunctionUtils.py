from RationalFunc import RFunc
from Poly import QPoly, qpoly_roots

# TODO: Partial fraction decomposition

def rfunc_roots(rfunc):
    """Approximate roots of a rational function"""
    assert type(rfunc) == RFunc
    return qpoly_roots(rfunc.N)


def rfunc_asymptotes(rfunc):
    """Approximate asymptots of a rational function"""
    assert type(rfunc) == RFunc
    dN = rfunc.N.degree()
    dD = rfunc.D.degree()
    
    out = []
    
    if dN == dD+1:
        out += [rfunc.N//rfunc.D]
    elif dN == dD:
        out += [QPoly( [rfunc.N[-1]/rfunc.D[-1]] )]
    elif dN < dD:
        out += [QPoly( [0] )]
    
    out += [QPoly([i]) for i in qpoly_roots(rfunc.D)]
    
    return out





if __name__ == '__main__':
    from random import sample
    coefs = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
    co1 = sample(coefs,6)
    co2 = sample(coefs,6)
    R = RFunc( co1, co2 )
    print(f"R = {R}")
    print(rfunc_roots(R))
    
    print(rfunc_asymptotes(R))