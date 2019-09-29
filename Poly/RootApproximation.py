from Poly.QPoly import QPoly
from Rational import coerce_to_rational, rational_round

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


if __name__ == '__main__':
    R = QPoly( [-3,1,1] )
    approx_root = newtons_method(R,2)
    
    print(f"R = {R}")
    print(f"by Newton's method R has a root at approximately: {approx_root}\nwhich is {approx_root.digits(5)}")
    print(f"Approximation has an error of about {float(R(approx_root))}")
    
    
    R = QPoly( [-3,1,1] )
    approx_root = bisection_method(R,0,2)
    print(float(approx_root[0]))