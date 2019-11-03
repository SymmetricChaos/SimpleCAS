from Utility import gcd, first_where

class Rational:
    
    def __init__(self,n,d=1):
        
        if type(n) != int:
            raise TypeError("Numerator must be int.")
        if type(d) != int:
            raise TypeError("Denominator must be int.")
        if d == 0:
            raise ZeroDivisionError

        if d < 0:
            d = abs(d)
            n = -n

        self.n = n
        self.d = d
        self.simplify()


    def simplify(self):
        """Convert fraction to simplest form"""
        g = abs(gcd(self.n,self.d))
        self.n = self.n//g
        self.d = self.d//g


    def copy(self):
        return Rational(self.n,self.d)


    def __str__(self):
        if self.d == 1:
            return str(self.n)
        return f"{self.n}/{self.d}"


    def _pretty_name(self):
        """Format for LaTeX"""
        if self.d == 1:
            return f"${self.n}$"
        else:
            return f"$\dfrac{{{self.n}}}{{{self.d}}}$"


    def __repr__(self):
        if self.d == 1:
            return str(self.n)
        return f"{self.n}/{self.d}"


    def inv(self):
        return Rational(self.d,self.n)


    def __neg__(self):
        return Rational(-self.n,self.d)


    def __add__(self,addend):
        
        # If we're adding a Rational to any other object we will instead use
        # the __radd__ method on that object.
        if type(addend) not in [Rational,int]:
            return NotImplemented
        
        if type(addend) == int:
            addend = Rational(addend)
        
        n = self.n*addend.d + addend.n*self.d
        d = self.d*addend.d

        return Rational(n,d)


    def __radd__(self,addend):
        if type(addend) == int:
            addend = Rational(addend)
        return self + addend


    def __sub__(self,addend):
        if type(addend) not in [Rational,int]:
            return NotImplemented
        return self + -addend


    def __rsub__(self,addend):
        return addend + -self
    

    def __mul__(self,multiplier):
        if type(multiplier) not in [Rational,int]:
            return NotImplemented
        
        if type(multiplier) == int:
            multiplier = Rational(multiplier)
            
        n = self.n * multiplier.n
        d = self.d * multiplier.d
        
        return Rational(n,d)


    def __rmul__(self,multiplier):
        if type(multiplier) == int:
            multiplier = Rational(multiplier)
        return self*multiplier


    def __truediv__(self,divisor):
        if type(divisor) not in [Rational,int]:
            return NotImplemented

        if divisor == 0:
            raise ZeroDivisionError
        if type(divisor) == int:
            divisor = Rational(divisor)
        return self*divisor.inv()
    
     
    def __rtruediv__(self,dividend):
        if self == 0:
            raise ZeroDivisionError
        if type(dividend) == int:
            dividend = Rational(dividend)
        return self.inv()*dividend


    def __floordiv__(self,divisor):
        if type(divisor) not in [Rational,int]:
            return NotImplemented
        
        if divisor == 0:
            raise ZeroDivisionError
        if type(divisor) == int:
            divisor = Rational(divisor)
        q = self*divisor.inv()
        v = q.n // q.d
        return v


    def __mod__(self,modulus):
        if modulus == 0:
            raise ZeroDivisionError
        if type(modulus) == int:
            modulus = Rational(modulus)
        if modulus > self:
            return self
        else:
            a = self.copy()
            while a >= modulus:
                a -= modulus
            return a


    def __eq__(self,other):
        if type(other) == int:
            other = Rational(other)
        if self.n == other.n:
            if self.d == other.d:
                return True
        return False
    
    
    def __le__(self, other):
        d = self-other
        if d.n >= 0:
            return False
        return True


    def __lt__(self, other):
        d = self-other
        if d.n > 0:
            return False
        return True


    def __ge__(self, other):
        d = self-other
        if d.n >= 0:
            return True
        return False
    
    
    def __gt__(self, other):
        d = self-other
        if d.n > 0:
            return True
        return False
    
    
    def __pow__(self,pwr):
        if type(pwr) != int:
            raise TypeError(f"pwr must be an integer not {type(pwr)}")
        
        # For negative powers invert then use recursion
        if pwr < 1:
            return self.inv()**abs(pwr)
        elif pwr == 0:
            return Rational(1)
        elif pwr == 1:
            return self
        else:
            n = self.n**pwr
            d = self.d**pwr
            return Rational(n,d)


    def __hash__(self):
        return hash("CustomRational"+str(self))


    def __float__(self):
        return self.n/self.d
    
    
    def __abs__(self):
        """Absolute value"""
        return Rational(abs(self.n),self.d)
    
    
    def __floor__(self):
        """Greatest smaller integer"""
        return self.n // self.d


    def _whole_part(self):
        """The whole part of the fraction"""
        return self.n // self.d


    def _fractional_part(self):
        """The fractional part of the fraction"""
        return Rational(self.n % self.d, self.d)
    
    
    def mixed_form(self):
        """Whole and fractional part"""
        w = self.whole_part
        f = self.fractional_part
        return w,f
    
        
    def _mixed_name(self):
        """Format for LaTeX as a mixed fraction"""
        if self.d == 1:
            return str(self.n)
        else:
            w,f = self.mixed_form()
            return f"${w}\dfrac{{{f.n}}}{{{f.d}}}$"
    
    
    def digits(self,n):
        """Return the decimal representation of the fraction out to n digits past the decimal point"""
        
        if n == 0:
            return self.whole_part
        
        N = abs(self.n)
        D = self.d

        sgn = "-" if N != self.n else ""

        digits = []
        
        for ctr in range(n+1):
            digits.append(N//D)
            N = (N % D)*10
        
        x1 = str(digits[0])
        x2 = "".join(str(e) for e in digits[1:])
        out = f"{sgn}{x1}.{x2}"

        return out


    def _decimal_expansion(self):
        """The complete decimal expansion of the rational, with repeating part"""
        
        # Quickly deal with integers
        if self.d == 1:
            return str(self.n)
        
        N = abs(self.n)
        D = self.d

        sgn = "-" if N != self.n else ""

        # Keep track of digits and remainders
        digits = []
        rems = []
        
        # Get digits until a remainder repeats which means we've gotten to the
        # end of repeating part of the decimal (if it exists) or the end of the
        # decimal expansion (if it terminates)
        while N not in rems:
            rems.append(N)
            digits.append(N//D)
            N = (N % D)*10
        # Locate the start of the repeating section
        nonrep = first_where(rems,N)
        
        x1 = str(digits[0])
        x2 = "".join(str(e) for e in digits[1:nonrep])
        x3 = "".join(str(e) for e in digits[nonrep:])
        
        # If the repeating section is 0 ignore it
        # Otherwise put it in parentheses to indicate it is repeating
        if x3 == "0":
            x3 = ""
        else:
            x3 = f"({x3})"
            
        out = f"{sgn}{x1}.{x2}{x3}"

        return out


    def cfrac(self):
        """Canonical simple continued fraction representation"""
        tmp = Rational(self.n,self.d)
        L = []
        while True:
            w,f = tmp.mixed_form()
            L.append(w)
            if f == 0:
                break
            tmp = f.inv()
    
        return L


    pretty_name = property(_pretty_name)
    whole_part = property(_whole_part)
    fractional_part = property(_fractional_part)
    mixed_name = property(_mixed_name)
    decimal_expansion = property(_decimal_expansion)


if __name__ == '__main__':

#    Explanation = open(r"Explanation.txt","r")
#    for i in Explanation.readlines():
#        print(i)
    R = Rational(5,7)
    print(R**2)
    print(R**-3)
    print(R)