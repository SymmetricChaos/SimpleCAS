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


def sturm_chain(poly):
    assert type(poly) == QPoly
    
    p0 = poly
    p1 = poly.derivative()
    
    yield p0

    while True:
        p0, p1 = p1, -(p0 % p1)
        yield p0
        
        if len(p0) == 1:
            break
        




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
    
    print("Sturm Chain")
    for i in sturm_chain( QPoly( [-1,-1,0,1,1] ) ):
        print(i)