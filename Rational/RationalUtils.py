from Rational.RationalType import Rational
from Rational.CastToRational import cast_to_rational
from Utility import gcd
from Rational.CFracType import CFrac, cfrac_to_frac


def _rational_gcd(A,B):
    """Largest rational such that both A and B are integer multiples of it"""
    assert type(A) == Rational
    assert type(B) == Rational
    return Rational(gcd(A.n*B.d,A.d*B.n),(A.d*B.d))


def rational_gcd(*args):
    """Greatest common divisor"""
    
    # Handle the case that a list is provided
    if len(args) == 1 and type(args[0]) is list:
        return rational_gcd(*args[0])
    
    # the gcd of a number with itself is iself
    if len(args) == 1:
        return args[0]
    
    # calculate gcd for two numbers
    if len(args) == 2:
        a = args[0]
        b = args[1]
        g = _rational_gcd(a,b)
        return g
    
    # if more than two break it up recursively
    a = rational_gcd(*args[0:2])
    b = rational_gcd(*args[2:])
    return rational_gcd(a,b)


def _rational_lcm(A,B):
    """Smallest rational such that it is an integer multiple of A and of B"""
    assert type(A) == Rational
    assert type(B) == Rational
    return abs(A*B)/_rational_gcd(A,B)


def rational_lcm(*args):
    """Least Common Multiple"""
    
    # Handle the case that a list is provided
    if len(args) == 1 and type(args[0]) is list:
        return rational_lcm(*args[0])
    
    # the lcm of a number with itself is iself
    if len(args) == 1:
        return args[0]
    
    # calculate lcm for two numbers
    if len(args) == 2:
        a = args[0]
        b = args[1]
        g = _rational_gcd(a,b)
        return abs(a*b)/g
    
    # if more than two break it up recursively
    a = rational_lcm(*args[0:2])
    b = rational_lcm(*args[2:])
    return _rational_lcm(a,b)





def rational_seq(lo,hi,step):
    """Sequence of rational numbers"""
    lo   = cast_to_rational(lo)
    hi   = cast_to_rational(hi)
    step = cast_to_rational(step)
    out = [lo]
    while out[-1]+step <= hi:
        out.append(out[-1]+step)
    return out


def rational_round(Q,dlim):
    """Best approximation of Q with denominator of d or less, by semi-convergents"""
    if type(Q) != Rational:
        raise TypeError("Q must be Rational not {type(Q)}")
  
    assert type(dlim) == int
    if dlim < 1:
        raise ZeroDivisionError

    # https://shreevatsa.wordpress.com/2011/01/10/not-all-best-rational-approximations-are-the-convergents-of-the-continued-fraction/
    a = CFrac(Q)

    prev = Rational(a[0])
    for pos,val in enumerate(a):
        # Try appending the floor of half the next convergent
        semi = a[:pos]+[(val-1)//2+1]
        # If it is worse than the last semiconvergent add 1
        if abs(cfrac_to_frac(semi) - Q)  >  abs(prev - Q):
            semi[pos] += 1
        while semi[pos] <= val:
            if cfrac_to_frac(semi).d > dlim:
                semi[pos] -= 1
                return prev
            prev = cfrac_to_frac(semi)
            semi[pos] += 1
    return Q


def sign(Q):
    """Sign of a rational number"""
    if type(Q) != Rational:
        raise TypeError("Q must be Rational not {type(Q)}")
  
    if Q.n > 0:
        return 1
    elif Q.n < 0:
        return -1
    else:
        return 0
    

def all_pos_rationals():
    """Generate all positive rational numbers"""
    yield Rational(0)
    diag = 1
    prev = set()
    while True:
        N = 1
        D = diag
        for i in range(diag):
            r = Rational(N,D)
            if r not in prev:
                prev.add(r)
                yield r
            N += 1
            D -= 1
        diag += 1


def all_rationals():
    """Generate all rational numbers"""
    yield Rational(0)
    diag = 1
    prev = set()
    while True:
        N = 1
        D = diag
        for i in range(diag):
            r = Rational(N,D)
            if r not in prev:
                prev.add(r)
                yield r
                yield -r
            N += 1
            D -= 1
        diag += 1





if __name__ == '__main__':
    
    print("GCD and LCM")
    a = Rational(13,6)
    b = Rational(3,4)
    G = rational_gcd(a,b)
    L = rational_lcm(a,b)
    print(f"gcd({a},{b}) = {G}")
    print(f"lcm({a},{b}) = {L}")
    
    
    print("\n\nRational Sequence")
    print(rational_seq(0,3,Rational(2,3)))
    

    print("\n\nAll Positive Rational Numbers")
    for pos,val in enumerate(all_pos_rationals()):
        if pos > 20:
            break
        print(val)