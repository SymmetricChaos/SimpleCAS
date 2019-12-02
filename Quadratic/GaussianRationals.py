from Quadratic.GaussianIntegers import GaussInt
from Utility import gcd


class GaussRational:
    
    def __init__(self,n,d=1):
        
        if type(n) != GaussInt:
            raise TypeError("Numerator must be GaussInt.")
        if type(d) != GaussInt:
            raise TypeError("Denominator must be GaussInt.")
        if d == 0:
            raise ZeroDivisionError


        self.n = n
        self.d = d
#        self.make_primitive()
#        self.simplify()

    def make_primitive(self):
        """Primitive but not fully simplified fraction"""
        g = gcd(self.n.re,self.n.im,self.d.re,self.d.im)
        self.n = self.n//g
        self.d = self.d//g

#    def simplify(self):
#        """Convert fraction to simplest form"""
#        g = gcd(self.n,self.d)
#        self.n = self.n//g
#        self.d = self.d//g


    def copy(self):
        return GaussRational(self.n,self.d)


    def __str__(self):
        if self.d == 1:
            return str(self.n)
        
        if self.n.re == 0 or self.n.im == 0:
            num = f"{self.n}"
        else:
            num = f"({self.n})"
        
        if self.d.re == 0 or self.d.im == 0:
            den = f"{self.d}"
        else:
            den = f"({self.d})"
        
        return f"{num}/{den}"


    def __repr__(self):
        return str(self)

 
    def _pretty_name(self):
        """Format for LaTeX"""
        if self.d == 1:
            return f"${self.n}$"
        else:
            return f"$\dfrac{{{self.n}}}{{{self.d}}}$"


    def inv(self):
        return GaussRational(self.d,self.n)


    def __neg__(self):
        return GaussRational(-self.n,self.d)


    def __add__(self,addend):
        
        if type(addend) not in [GaussRational,int]:
            return NotImplemented
        
        if type(addend) == int:
            addend = GaussRational(addend)
        
        n = self.n*addend.d + addend.n*self.d
        d = self.d*addend.d

        return GaussRational(n,d)


    def __radd__(self,addend):
        if type(addend) == int:
            addend = GaussRational(addend)
        return self + addend


    def __sub__(self,addend):
        if type(addend) not in [GaussRational,int]:
            return NotImplemented
        return self + -addend


    def __rsub__(self,addend):
        return addend + -self


    def __mul__(self,multiplier):
        if type(multiplier) not in [GaussRational,int]:
            return NotImplemented
        
        if type(multiplier) == int:
            multiplier = GaussRational(multiplier)
            
        n = self.n * multiplier.n
        d = self.d * multiplier.d
        
        return GaussRational(n,d)


#    def __rmul__(self,multiplier):
#        if type(multiplier) == int:
#            multiplier = Rational(multiplier)
#        return self*multiplier
#
#
#    def __truediv__(self,divisor):
#        if type(divisor) not in [Rational,int]:
#            return NotImplemented
#
#        if divisor == 0:
#            raise ZeroDivisionError
#        if type(divisor) == int:
#            divisor = Rational(divisor)
#        return self*divisor.inv()
#    
#     
#    def __rtruediv__(self,dividend):
#        if self == 0:
#            raise ZeroDivisionError
#        if type(dividend) == int:
#            dividend = Rational(dividend)
#        return self.inv()*dividend
#
#
#    def __floordiv__(self,divisor):
#        if type(divisor) not in [Rational,int]:
#            return NotImplemented
#        
#        if divisor == 0:
#            raise ZeroDivisionError
#        if type(divisor) == int:
#            divisor = Rational(divisor)
#        q = self*divisor.inv()
#        v = q.n // q.d
#        return v
#
#
#    def __mod__(self,modulus):
#        if modulus == 0:
#            raise ZeroDivisionError
#        if type(modulus) == int:
#            modulus = Rational(modulus)
#        if modulus > self:
#            return self
#        else:
#            a = self.copy()
#            while a >= modulus:
#                a -= modulus
#            return a


    def __eq__(self,other):
        if type(other) == int:
            other = GaussRational(other)
        if self.n == other.n:
            if self.d == other.d:
                return True
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
            n = self.n**pwr
            d = self.d**pwr
            return GaussRational(n,d)


    def __hash__(self):
        return hash(f"CustomGaussRational{self}")
#
#
#    def __complex__(self):


    pretty_name = property(_pretty_name)





if __name__ == '__main__':

#    Explanation = open(r"Explanation.txt","r")
#    for i in Explanation.readlines():
#        print(i)
    a = GaussInt(0,1)
    b = GaussInt(1,2)
    R = GaussRational(a,b)
    print(R)
    print(R**2)