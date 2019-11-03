from Rational.RationalType import Rational
from Utility import first_where
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

        
def rep_dec_to_frac(S):
    """Convert a string representing a repeating decimal to Rational"""

    m = re.fullmatch("-?\d*\.\d*\(\d*\)",S)
    is_neg = 1
    if m:
        
        if S[0] == "-":
            is_neg = -1
            S = S[1:]
        D = first_where(S,".")-1 # pos of decimal
        R = first_where(S,"(")+1 # pos of repeating part
        
        # String representing the non-repeating and repeating parts
        fpart = S[:R-1].replace(".","")
        rpart = S[R:-1]
        
        # Fraction representing the non-repeating part
        fR = Rational(int(fpart),10**(D+1))
        # Fraction represent the repeating part
        rR = Rational(int(rpart),int("9"*len(rpart)+"0"*(D+1)))

        return is_neg*(fR + rR)
    

    else:
        return None


def ratio_to_frac(S):
    """Convert a string of form a/b to Rational"""
        
    m = re.fullmatch("-?\d*\/\d*",S)
    is_neg = 1
    if m:
        if m[0] == "-":
            is_neg = -1
            m = m[1:]
        n,d = S.split("/")
        return Rational(int(n)*is_neg,int(d))
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
    elif type(T) == str:
        for func in [ratio_to_frac,int_str_to_frac,rep_dec_to_frac,term_dec_to_frac]:
            out = func(T)
            if type(out) == Rational:
                return out
        raise ValueError(f"Could not cast {T} to Rational")
    else:
        raise ValueError(f"Could not cast {T} to Rational")
        




if __name__ == '__main__':

    
    
    d = "3"
    r = cast_to_rational(d)
    print(f"{d} = {r} = {r.n/r.d}")
    
    d = "3.141592"
    r = cast_to_rational(d)
    print(f"{d} = {r} = {r.n/r.d}")
#
#    
#    print()
#    print()
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