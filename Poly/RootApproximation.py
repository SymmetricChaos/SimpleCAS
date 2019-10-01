from Poly.QPoly import QPoly
from Poly.QPolyUtils import rational_roots
from Rational import coerce_to_rational, rational_round, sign

def bound_of_roots(poly):
    """Cauchy's forumla for bounds on roots"""
    assert type(poly) == QPoly
    
    co = reversed(poly.coef.copy())
    lim = 0
    for i in co:
        if abs(i/poly[-1]) > lim:
            lim = abs(i/poly[-1])
    
    return lim+1


def newtons_method(poly,start,den_lim=100,iter_lim=100):
    """Approximate a root by Newton's method limited by denominator and number of iterations"""
    assert type(poly) == QPoly
    
    p  = poly
    dp = poly.derivative()
    
    r = coerce_to_rational(start)
    for i in range(iter_lim):
        rold = rational_round(r - p(r)/dp(r),den_lim)
        if rold == r:
            return r
        r = rold
    
    return r


## TODO: make sure this actually makes sense
## TODO: denominator limit
## TODO: test with higher order polynomials
def bisection_method(poly,lo,hi,iter_lim=10):
    assert type(poly) == QPoly
    
    lo = coerce_to_rational(lo)
    hi = coerce_to_rational(hi)
    
    # Signs of the limits must differ in order to guarantee a root
    if poly(lo) > 0 and poly(hi) > 0:
        return []
    if poly(lo) < 0 and poly(hi) < 0:
        return []
    
    mid = (hi+lo)/2
    
    if iter_lim == 0:
        return [mid]
    
    out = []
    out += bisection_method(poly,lo,mid,iter_lim=iter_lim-1)
    out += bisection_method(poly,mid,hi,iter_lim=iter_lim-1)

    return out


def sturm_sequence(poly):
    """Sequence of polynomials used for Sturm's Theorem"""
    assert type(poly) == QPoly
    
    p0 = poly
    p1 = poly.derivative()
    
    yield p0

    while True:
        p0, p1 = p1, -(p0 % p1)
        yield p0
        
        if len(p0) == 1:
            break
        
        
def sturm_sign_changes(L,A):
    """Given a Sturm sequence and a point check how many changes of sign there
    are in the sequences of polynomials evaluated at that point"""
    cur_sgn = sign(L[0](A))
    n = 0
    for poly in L[1:]:
        if sign(poly(A)) == 0:
            continue
        if sign(poly(A)) != cur_sgn:
            n += 1
            cur_sgn = sign(poly(A))
    
    return n


def _sturm_roots(poly,lo,hi,L):
    """Recursive function to using Sturm's Theorem to isolate real roots"""
    mid = (lo+hi)/2
    Va = sturm_sign_changes(L,lo)
    Vb = sturm_sign_changes(L,hi)
    Vc = sturm_sign_changes(L,mid)
    
    rts_lo = abs(Va - Vc)
    rts_hi = abs(Vc - Vb)
    
    out = []
    
    if rts_lo == 1:
        out += [ (lo,mid) ] 
    if rts_hi == 1:
        out += [ (mid,hi) ] 
    
    if rts_lo > 1:
        out += _sturm_roots(poly,lo,mid,L)
    if rts_hi > 1:
        out += _sturm_roots(poly,mid,hi,L)
    
    return out


def sturm_root_isolation(poly):
    """Find disjoint intervals containing each root"""
    
    assert type(poly) == QPoly
    
    # Place a bound on the absolute value of the the roots, this tells us the
    # largest interval we need to search
    B = bound_of_roots(poly)
    
    L = [i for i in sturm_sequence(poly)]
    
    return _sturm_roots(poly,-B,B,L)


def descartes_rule(poly):
    """Use descartes rule of signs to estimate number of positive roots"""
    assert type(poly) == QPoly
    
    co = poly.coef.copy()
    n = 0
    cur_sgn = sign(co[0])
    for i in co[1:]:
        if sign(i) != cur_sgn:
            n += 1
            cur_sgn = sign(i)
    
    return n


def all_roots(poly):
    
    P = poly.copy()
    rr = rational_roots(poly)
    
    roots = []
    
    for i in rr:
        roots.append(i)
        P = P//QPoly( [-i,1] )

    intervals = sturm_root_isolation(P)
    
    for i in intervals:
        roots.append(newtons_method(P, (i[0]+i[1])/2 ))


    return sorted(roots)

def critical_points(poly):
    assert type(poly) == QPoly
    
    if poly.degree() == 0:
        return [0]
    
    elif poly.degree() == 1:
        return [0]

    else:
        
        Pd = poly.derivative()
        return all_roots(Pd)
        
        





if __name__ == '__main__':
    
    R = QPoly( [-3,1,1] )
    approx_root = newtons_method(R,2)
    
    print(f"R = {R}")
    print(f"by Newton's method R has a root at approximately: {approx_root}\nwhich is {approx_root.digits(5)}")
    print(f"Approximation has an error of about {float(R(approx_root))}")



    print("\n\n")
    approx_root = bisection_method(R,0,2,10)[0]
    print(f"R = {R}")
    print(f"by the bisection method R has a root at approximately: {approx_root}\nwhich is {approx_root.digits(5)}")
    print(f"Approximation has an error of about {float(R(approx_root))}")



    print("\n\n")
    b = bound_of_roots(R)
    print(f"All roots of {R} have absolute value {b} or less")



    print("\n\n")
    print("Sturm Chain")
    for i in sturm_sequence( QPoly( [-1,-1,0,1,1] ) ):
        print(i)



    print("\n\n")
    P = QPoly( [-4,1] ) * QPoly( [3,1] ) * QPoly( [1,1] )
    print(f"P = {P}")
    print(f"The roots of P are within the intervals: {sturm_root_isolation(P)}")



    print("\n\n")
    P = QPoly( [-1,-1,1,1] )
    print(f"P = {P}")
    print(f"by Descarte's Rule of Signs, P has at most {descartes_rule(P)} positive real roots")



    print("\n\n")
    P = QPoly( [0,-6,3,2] )
    print(f"P = {P}")
    print(f"The roots of P are approximately {all_roots(P)}")
    
