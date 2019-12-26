from Quadratic.GaussianIntegers import GaussInt, gauss_gcd, str_to_gauss


class GaussRational:
    
    def __init__(self,n,d=1):
        
        if type(n) == str:
            n = str_to_gauss(n)
        
        if type(d) == str:
            d = str_to_gauss(d)
        
        if type(n) not in [GaussInt,int]:
            raise TypeError("Numerator must be GaussInt.")
        if type(d) not in [GaussInt,int]:
            raise TypeError("Denominator must be GaussInt.")
        if d == 0:
            raise ZeroDivisionError

        if type(n) == int:
            n = GaussInt(n,0)

        if type(d) == int:
            d = GaussInt(d,0)

        self.n = n
        self.d = d
        self.simplify()


    def simplify(self):
        """Convert fraction to simplest form"""
        g = gauss_gcd(self.n,self.d)
        self.n = self.n//g
        self.d = self.d//g


    def _pretty_name(self):
        """Format for LaTeX"""
        if self.d == 1:
            return f"${self.n}$"
        else:
            return f"$\dfrac{{{self.n}}}{{{self.d}}}$"


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


    def __rmul__(self,multiplier):
        if type(multiplier) == int:
            multiplier = GaussRational(multiplier)
        return self*multiplier


    def __truediv__(self,divisor):
        if type(divisor) not in [GaussRational,int]:
            return NotImplemented

        if type(divisor) == int:
            if divisor == 0:
                raise ZeroDivisionError
            divisor = GaussRational(divisor)
            
        return self*divisor.inv()
    
     
    def __rtruediv__(self,dividend):
        if self == GaussInt(0,0):
            raise ZeroDivisionError
        if type(dividend) == int:
            dividend = GaussRational(dividend)
        return self.inv()*dividend


    # Because GCD is not unique we need to modify equality checking
    def __eq__(self,other):
        if type(other) == int:
            other = GaussRational(other)
        if type(other) == GaussRational:
            return self.n*other.d == self.d*other.n
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
            n = self.n**pwr
            d = self.d**pwr
            return GaussRational(n,d)


    def __hash__(self):
        return hash(f"CustomGaussRational{self}")

    pretty_name = property(_pretty_name)





if __name__ == '__main__':


    R = GaussRational("-3-3i","2+4i")
    print(R)
    print(R.inv())
    print(R.inv()*R)
    print(R**2)
    print(R.pretty_name)
    print(R/2)