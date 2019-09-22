from RationalType import Rational
from Utility import gcd, first_where
import re

def _rational_gcd(A,B):
    """Largest rational such that both A and B are integer multiples of it"""
    assert type(A) == Rational
    assert type(B) == Rational
    return Rational(gcd(A.n*B.d,A.d*B.n),(A.d*B.d))


def rational_gcd(*args):
    
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
    return _rational_gcd(a,b)


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
    """Convert String to Rational"""
    assert type(S) == str
    if "." not in S:
        S += "."
        
    m = re.fullmatch("\d*\.\d*",S)
    if m:
        D = len(S)-first_where(S,".")-1
        S = S.replace(".","")
        return Rational(int(S),10**D)
    else:
        raise Exception(f"Cannot coerce {S} to Rational")
        
        
        
        
        
if __name__ == '__main__':
    a = Rational(13,6)
    b = Rational(3,4)
    G = rational_gcd(a,b)
    L = rational_lcm(a,b)
    print(f"gcd({a},{b}) = {G}")
    print(f"lcm({a},{b}) = {L}")
    
    d = "123.14"
    r = digits_to_frac(d)
    print(f"{d} = {r} = {r.n/r.d}")