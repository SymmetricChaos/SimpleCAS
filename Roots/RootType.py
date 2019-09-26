# Correct handling and evaluation of rational roots

from Rational import Rational, str_to_frac, digits_to_frac

class Root:
    
    def __init__(self,n,contents):
        if type(n) == Rational:
            pass
        elif type(n) == int:
            n = Rational(n)
        elif type(n) == str:
            try:
                n = str_to_frac(n)
            except:
                n = digits_to_frac(n)
        else:
            raise Exception(f"Could not coerce {n} to Rational")

        self.n = n
