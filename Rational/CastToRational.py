from Rational.RationalType import Rational
from Utility import first_where
from CFracType import CFrac
import re


def int_str_to_frac(S):
    """Convert a string representing an integer to Rational"""
    m = re.fullmatch("-?\d+",S)
    if m:
        return Rational(int(S))
    else:
        return None
        
def term_dec_to_frac(S):
    """Convert a string representing a terminating decimal to Rational"""
    
    m = re.fullmatch("-?\d*\.\d*",S)
    is_neg = 1
    if m:
        if S[0] == "-":
            is_neg = -1
            S = S[1:]
        D = len(S)-first_where(S,".")-1
        S = S.replace(".","")
        return Rational(int(S)*is_neg,10**D)
    else:
        return None


# conceptual basis for 
#x = 3.14(26)
#
#10000x = 31426.(26)
#  100x =   314.(26)
# 9900x = 31426-314
# 
#
# 
# 
#x = 31.(26)
#
#100x = 3126.(26)
#   x =   31.(26)
# 99x = 3126-31

def rep_dec_to_frac(S):
    """Convert a string representing a repeating decimal to Rational"""

    m = re.fullmatch("-?\d*\.\d*\(\d+\)",S)
    is_neg = 1
    if m:

        if S[0] == "-":
            is_neg = -1
            S = S[1:]

        T = re.sub("\(|\)|\.","",S)

        D = first_where(S,".")-1 # pos of decimal
        R = first_where(S,"(")-2 # pos of repeating part
        
        A = int(T)
        B = int(T[:R+1])
        
        mul_full = 10**(len(T)-1)
        mul_rep = 10**R
        mul_dec = 10**D

        return Rational(A-B,(mul_full-mul_rep) )*mul_dec*is_neg

    else:
        return None


def ratio_to_frac(S):
    """Convert a string of form a/b to Rational"""
        
    m = re.fullmatch("-?\d+\/\d+",S)
    is_neg = 1
    if m:
        if m[0] == "-":
            is_neg = -1
            m = m[1:]
        n,d = S.split("/")
        return Rational(int(n)*is_neg,int(d))
    else:
        return None
    

def scientific_to_frac(S):
    """Convert a string formatted as e notation to Rational"""
    S = re.sub("e|⏨|\*\^","E",S)
    m = re.fullmatch("-?\d\.\d+E-?\d+",S)

    if m:
        L,R = S.split("E")

        
        significand = term_dec_to_frac(L)
        power = Rational(10)**int(R)

        return significand*power
    else:
        return None



        

def cast_to_rational(T):
    """Best effort to transform input to a rational number"""
    
    if type(T) == Rational:
        return T
    
    elif type(T) == int:
        return Rational(T)
    
    elif type(T) == float:
        return cast_to_rational(str(T))
    
    elif type(T) == CFrac:
        return T.as_rational()
    
    elif type(T) == str:
        for func in [ratio_to_frac,
                     int_str_to_frac,
                     term_dec_to_frac,
                     rep_dec_to_frac,
                     scientific_to_frac]:
            out = func(T)
            if type(out) == Rational:
                return out
        raise ValueError(f"Could not cast {T} to Rational")
        
    else:
        raise ValueError(f"Could not cast {T} to Rational")
        




if __name__ == '__main__':

    for d in ["3","3.141592","3.14(26)","311.(26)","1.24e-5","1.21e2"]:
        r = cast_to_rational(d)
        print(f"\n\n{d} = {r} = {r.n/r.d}")
        r = cast_to_rational("-"+d)
        print(f"\n-{d} = {r} = {r.n/r.d}")


#    
#    d = Rational(-16,25).decimal_expansion
#    r = digits_to_frac(d)
#    print(f"{d} = {r} = {r.n/r.d}")
#    print(r.decimal_expansion)
#        
#    
#    print()
#    print("")
#    
#    d = Rational(137,126).decimal_expansion
#    r = digits_to_frac(d)
#    print(f"{d} = {r} = {r.n/r.d}")
#    print(r.decimal_expansion)