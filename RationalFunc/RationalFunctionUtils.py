from RationalFunc import RFunc
from Poly import QPoly, qpoly_roots, poly_egcd, poly_factor


def partial_fraction(rfunc):
    """Partial fraction decomposition of a rational function"""
    #f/g = Df/P + Cf/Q
    #g = P*Q
    #D and P from Bezout's identity

    f = rfunc.N
    g = rfunc.D
    
    F = poly_factor(g)
    print("factors",F)
    
    gcd, C, D = poly_egcd(F[0],F[1])
    print("gcd",gcd)
    print("C",C)
    print("D",D)

    norm = F[0]*C + F[1]*D
    print("normalizing factor",norm)
    C = C//norm
    D = D//norm
    
    t0 = RFunc( D*f, F[0] )
    t1 = RFunc( C*f, F[1] )
    out = f"{t0}  +  {t1}"

    print(out)
    print(t0+t1)
    


def rfunc_roots(rfunc):
    """Approximate roots of a rational function"""
    assert type(rfunc) == RFunc
    return qpoly_roots(rfunc.N)


def rfunc_asymptotes(rfunc):
    """Approximate asymptotes of a rational function"""
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
    print("Roots",rfunc_roots(R))
    print("Asymptotes",rfunc_asymptotes(R))
    
    print()
    R = RFunc( [1], [-3,2,1] )
    print(R)
    partial_fraction(R)