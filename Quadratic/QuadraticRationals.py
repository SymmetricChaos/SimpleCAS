from Quadratic.QuadraticIntegers import QuadInt


class QuadRational:
    
    def __init__(self,q,n=0,d=1):
        
        if type(n) not in [QuadInt,int]:
            raise TypeError(f"Numerator must be QuadInt or int not {type(n)}.")
        if type(d) not in [QuadInt,int]:
            raise TypeError(f"Denominator must be QuadInt or int not {type(d)}.")
        if type(q) != int:
            raise TypeError(f"Quadratic extension must be int not {type(q)}.")
        
        if d == 0:
            raise ZeroDivisionError

        if type(n) == int:
            n = QuadInt(q,n,0)

        if type(d) == int:
            d = QuadInt(q,d,0)
            
        if n == d:
            n = d = QuadInt(q,0,1)

        self.q = q
        self.n = n
        self.d = d
#        self.make_primitive()
#        self.simplify()

#
#    def make_primitive(self):
#        """Primitive but not fully simplified fraction"""
#        g = gcd(self.n.n,self.n.m,self.d.n,self.d.m)
#        self.n = QuadInt(self.n.m//g,self.n.n//g)
#        self.d = QuadInt(self.d.m//g,self.d.n//g)


#    def simplify(self):
#        """Convert fraction to simplest form"""
#        g = gcd(self.n,self.d)
#        self.n = self.n//g
#        self.d = self.d//g


    def _pretty_name(self):
        """Format for LaTeX"""
        if self.d == 1:
            return f"${self.n}$"
        else:
            return f"$\dfrac{{{self.n}}}{{{self.d}}}$"


    def copy(self):
        return QuadRational(self.q,self.n,self.d)


    def __str__(self):
        if self.d == 1:
            return str(self.n)
        
        if self.n.n == 0 or self.n.m == 0:
            num = f"{self.n}"
        else:
            num = f"({self.n})"
        
        if self.d.n == 0 or self.d.m == 0:
            den = f"{self.d}"
        else:
            den = f"({self.d})"
        
        return f"{num}/{den}"


    def __repr__(self):
        return str(self)


    def inv(self):
        return QuadRational(self.q,self.d,self.n)


    def __neg__(self):
        return QuadRational(self.q,-self.n,self.d)


    def __add__(self,addend):
        
        if type(addend) not in [QuadRational,int]:
            return NotImplemented
        
        if type(addend) == int:
            addend = QuadRational(self.q,addend)
        
        n = self.n*addend.d + addend.n*self.d
        d = self.d*addend.d

        return QuadRational(self.q,n,d)


    def __radd__(self,addend):
        if type(addend) == int:
            addend = QuadRational(self.q,addend)
        return self + addend


    def __sub__(self,addend):
        if type(addend) not in [QuadRational,int]:
            return NotImplemented
        return self + -addend


    def __rsub__(self,addend):
        return addend + -self


    def __mul__(self,multiplier):
        if type(multiplier) not in [QuadRational,int]:
            return NotImplemented
        
        if type(multiplier) == int:
            multiplier = QuadRational(self.q,multiplier)
            
        n = self.n * multiplier.n
        d = self.d * multiplier.d
        
        return QuadRational(self.q,n,d)


    def __rmul__(self,multiplier):
        if type(multiplier) == int:
            multiplier = QuadRational(self.q,multiplier)
        return self*multiplier


    def __truediv__(self,divisor):
        if type(divisor) not in [QuadRational,int]:
            return NotImplemented

        if type(divisor) == int:
            if divisor == 0:
                raise ZeroDivisionError
            divisor = QuadRational(self.q,divisor)
            
        return self*divisor.inv()
    
     
    def __rtruediv__(self,dividend):
        if self == QuadInt(0,0):
            raise ZeroDivisionError
        if type(dividend) == int:
            dividend = QuadRational(self.q,dividend)
        return self.inv()*dividend


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
            other = QuadRational(self.q,other)
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
            return QuadRational(self.q,1)
        elif pwr == 1:
            return self
        else:
            n = self.n**pwr
            d = self.d**pwr
            return QuadRational(self.q,n,d)


    def __hash__(self):
        return hash(f"CustomQuadRational{self}")



    pretty_name = property(_pretty_name)





if __name__ == '__main__':


    a = QuadInt(5,0,1)
    b = QuadInt(5,1,2)
    R = QuadRational(5,a,b)
    print(R)
    print(R.inv())
    print(R.inv()*R)
    print(R**2)
    print(R.pretty_name)
    print(R/2)
    
    print()
    
    n = QuadInt(5,1,1)
    d = QuadInt(5,0,2)
    G = QuadRational(5,n,d)
    print(G)
    print(G**2)
    print(G+1)