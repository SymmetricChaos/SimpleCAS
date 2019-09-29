from Poly.QPoly import QPoly
from Rational import coerce_to_rational, rational_round

def newtons_method(poly,start,den_lim=1000,iter_lim=10):
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

if __name__ == '__main__':
    R = QPoly( [-3,1,1] )
    approx_root = newtons_method(R,2,1000)
    
    print(f"R = {R}")
    print(f"R has a root at approximately: {approx_root}\nwhich is {approx_root.digits(5)}")
    print(f"Approximation has an error of about {R(approx_root)}")