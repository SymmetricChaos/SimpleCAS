from Poly.QPoly import QPoly
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


## TODO use for sturm's method of root isolation
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


def sturm_roots(poly,lo,hi):
    assert type(poly) == QPoly
    
    hi = coerce_to_rational(hi)
    lo = coerce_to_rational(lo)
    
    L = [i for i in sturm_sequence(poly)]
        
    
        
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
        out += sturm_roots(poly,lo,mid)
    if rts_hi > 1:
        out += sturm_roots(poly,mid,hi)
    
    return out
    
    


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
    P = QPoly( [0,1,0,"-1/6",0,"1/120",0,"-1/5040"] )
    print(f"P = {P}")
    print(f"The roots of P are within the intervals: {sturm_roots(P,-10,10)}")
        
    print("\n\n")
    P = QPoly( [-1,-1,1,1] )
    print(f"P = {P}")
    print(f"by Descarte's Rule of Signs, P has at most {descartes_rule(P)} positive real roots")
    
