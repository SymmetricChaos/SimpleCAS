from Rational.RationalType import Rational
from Utility import gcd, first_where
import re



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





def digits_to_frac(S):
    """Convert a string of form a.b to Rational"""
    if type(S) != str:
        raise TypeError("Input {S} is {type(S)} not str")
    if "." not in S:
        S += "."
        
    m = re.fullmatch("-?\d*\.\d*",S)
    is_neg = 1
    if m:
        if m[0] == "-":
            is_neg = -1
            m = m[1:]
        D = len(S)-first_where(S,".")-1
        S = S.replace(".","")
        return Rational(int(S)*is_neg,10**D)
    else:
        raise Exception(f"Cannot coerce {S} to Rational")


def str_to_frac(S):
    """Convert a string of form a/b to Rational"""
    if type(S) != str:
        raise TypeError("Input {S} is {type(S)} not str")
    if "/" not in S:
        S += "/1"
        
    m = re.fullmatch("-?\d*\/\d*",S)
    is_neg = 1
    if m:
        if m[0] == "-":
            is_neg = -1
            m = m[1:]
        n,d = S.split("/")
        return Rational(int(n)*is_neg,int(d))
    else:
        raise Exception(f"Cannot coerce {S} to Rational")
        

def coerce_to_rational(T):
    """Best effort to transform input to a rational number"""
    
    if type(T) == Rational:
        return T
    elif type(T) == int:
        return Rational(T)
    elif type(T) == float:
        return coerce_to_rational(str(T))
    elif type(T) == str:
        try:
            return str_to_frac(T)
        except:
            return digits_to_frac(T)
    else:
        raise Exception(f"Could not coerce {T} to Rational")





def cfrac_convergents(L):
    """Rational convergents of a simple continued fraction."""
    assert type(L) == list
    for i in L:
        assert type(i) == int
        
    N = [1,L[0]]
    D = [0,1]
    con = 2
    
    yield Rational(N[-1],D[-1])
    
    while con < len(L)+1:
        N.append( L[con-1] * N[con-1] + N[con-2] )
        D.append( L[con-1] * D[con-1] + D[con-2] )

        yield Rational(N[-1],D[-1])
        
        con += 1


def cfrac_to_frac(L):
    """Convert a continued fraction to a Rational"""
    assert type(L) == list, f"tpye {type(L)} is not a list"
    for i in L:
        assert type(i) == int
    
    N = [1,L[0]]
    D = [0,1]
    con = 2
    
    while con < len(L)+1:
        N.append( L[con-1] * N[con-1] + N[con-2] )
        D.append( L[con-1] * D[con-1] + D[con-2] )
        con += 1
        
    return Rational(N[-1],D[-1])


def rational_seq(lo,hi,step):
    """Sequence of rational numbers"""
    lo   = coerce_to_rational(lo)
    hi   = coerce_to_rational(hi)
    step = coerce_to_rational(step)
    out = [lo]
    while out[-1]+step <= hi:
        out.append(out[-1]+step)
    return out


def rational_round(Q,dlim):
    """Best approximation of Q with denominator of d or less, by semi-convergents"""
    assert type(Q) == Rational
    assert type(dlim) == int
    if dlim < 1:
        raise ZeroDivisionError

    # https://shreevatsa.wordpress.com/2011/01/10/not-all-best-rational-approximations-are-the-convergents-of-the-continued-fraction/
    a = Q.cfrac()

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
    assert type(Q) == Rational
    
    if Q.n > 0:
        return 1
    elif Q.n < 0:
        return -1
    else:
        return 0





if __name__ == '__main__':
    a = Rational(13,6)
    b = Rational(3,4)
    G = rational_gcd(a,b)
    L = rational_lcm(a,b)
    print(f"gcd({a},{b}) = {G}")
    print(f"lcm({a},{b}) = {L}")
    
    d = "3.141592"
    r = digits_to_frac(d)
    print(f"{d} = {r} = {r.n/r.d}")

    print(rational_round(r,100))
    
    print(rational_seq(0,3,Rational(2,3)))