from Quadratic.GaussianIntegers import GaussInt, gauss_gcd, str_to_gauss
from Rational import Rational, rational_gcd, cast_to_rational

class GaussRational:
    
    def __init__(self,re,im):
        
        self.re = cast_to_rational(re)
        self.im = cast_to_rational(im)

#        self.simplify()


#    def simplify(self):
#        """Convert fraction to one of its reduced forms"""
#        g = gauss_gcd(self.n,self.d)
#        
#        # Divide out GCD
#        if g != 1 and g != -1:
#            self.n = self.n//g
#            self.d = self.d//g
#
#        # Force lower coefficient to have positive real part
#        if self.d.re < 0:
#            self.n = -self.n
#            self.d = -self.d
        

    def _pretty_name(self):
        """Format for LaTeX"""
        # If the imaginary part is zero return just the whole part
        if self.im == Rational(0):
            return f"${self.re}$"
        
        # If the real part is zero just return the imaginary part
        if self.re == Rational(0):
            if self.im == Rational(1):
                return "$i$"
            elif self.im == Rational(-1):
                return "$-i$"
            else:
                return f"${self.im}i$"
        
        # If the imaginary part is negative
        elif self.im < Rational(0):
            # Unit case
            if self.im == Rational(-1):
                return f"${self.re} - i$"
            # General case
            else:
                return f"${self.re} - {abs(self.im)}i$"
        
        # If the imaginary part is positive
        else:
            # Unit case
            if self.im == Rational(1):
                return f"${self.re} + i$"
            # General case
            else:
                return f"${self.re} + {self.im}i$"


    def copy(self):
        return GaussRational(self.re,self.im)


    def __str__(self):
        
        # If the imaginary part is zero return just the whole part
        if self.im == Rational(0):
            return f"{self.re}"
        
        # If the real part is zero just return the imaginary part
        if self.re == Rational(0):
            if self.im == Rational(1):
                return "i"
            elif self.im == Rational(-1):
                return "-i"
            else:
                return f"{self.im}i"
        
        # If the imaginary part is negative
        elif self.im < Rational(0):
            # Unit case
            if self.im == Rational(-1):
                return f"{self.re} - i"
            # General case
            else:
                return f"{self.re} - {abs(self.im)}i"
        
        # If the imaginary part is positive
        else:
            # Unit case
            if self.im == Rational(1):
                return f"{self.re} + i"
            # General case
            else:
                return f"{self.re} + {self.im}i"


    def __repr__(self):
        return str(self)


    def inv(self):
        a = self.re.n
        b = self.re.d
        c = self.im.n
        d = self.im.d
        
        e = self.re**2 + self.im**2


        A = a/(b*e)
        B = -c/(d*e)

        return GaussRational(A,B)


    def __neg__(self):
        return self*-1


    def __add__(self,other):
        if type(other) == GaussRational:
            return GaussRational(self.re+other.re,
                                 self.im+other.im)
        elif type(other) == int:
            return GaussRational(self.re+other,self.im)
        elif type(other) == Rational:
            return GaussRational(self.re+other,self.im)
        elif type(other) == GaussInt:
            return GaussRational(self.re+other.re,
                                 self.im+other.im)
        else:
            return NotImplemented


    def __radd__(self,addend):
        return self + addend


    def __sub__(self,addend):
        return self + -addend


    def __rsub__(self,addend):
        return addend + -self


    def __mul__(self,other):
        if type(other) == GaussRational:
            return GaussRational(self.re*other.re - self.im*other.im,
                                 self.re*other.im + self.im*other.re)
        elif type(other) == GaussInt:
            return GaussRational(self.re*other.re - self.im*other.im,
                                 self.re*other.im + self.im*other.re)
        elif type(other) == int:
            return GaussRational(other*self.re,
                                 other*self.im)
        elif type(other) == Rational:
            return GaussRational(other*self.re,
                                 other*self.im)
        else:
            return NotImplemented


    def __rmul__(self,multiplier):
        return self*multiplier


    def __truediv__(self,divisor):
        if type(divisor) in [GaussInt,int]:
            divisor = GaussRational(divisor)
        
        if type(divisor) != GaussRational:
            return NotImplemented

        if divisor in [0,GaussInt(0,0),GaussRational(0,1)]:
            raise ZeroDivisionError
            
        return self*divisor.inv()
    
     
    def __rtruediv__(self,dividend):
        return self.inv()*dividend


    def __eq__(self,other):
        if type(other) in [int,Rational,GaussInt,GaussRational]
            return str(self) == str(other)
        else:
            return False


    def __pow__(self,pwr):
        if type(pwr) != int:
            raise TypeError(f"pwr must be an integer not {type(pwr)}")
        
        # For negative powers invert then use recursion
        if pwr < 0:
            return self.inv()**abs(pwr)
        elif pwr == 0:
            return GaussRational(1)
        elif pwr == 1:
            return self
        else:
            out = self.copy()
            for i in range(pwr-1):
                out *= self
            return out


    def __hash__(self):
        return hash(f"CustomGaussRational{self}")


    pretty_name = property(_pretty_name)





if __name__ == '__main__':

    R = GaussRational("1/2","7/5")
    S = GaussRational("4","9/7")
    print(f"R = {R}")
    print(f"-R = {-R}")
    print(f"1/R = {1/R}")
    print(f"1/(1/R) = {1/(1/R)}")
    print(f"R * 1/R = {R*1/R}")
    print(f"R*i = {R*GaussInt(0,1)}")
    print(f"R**2 = {R**2}")
    print(f"S = {S}")
    print(f"R*S = {R*S}")
    print(f"R/S = {R/S}")
    print(R.pretty_name)
    print(S.pretty_name)
