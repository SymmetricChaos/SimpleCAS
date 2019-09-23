from Utility import gcd

class Rational:
    
    def __init__(self,n,d=1):
        assert type(n) == int, "Numerator must be int."
        assert type(d) == int, "Denominator must be int."
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


    def inv(self):
        return Rational(self.d,self.n)


    def __neg__(self):
        return Rational(-self.n,self.d)


    def __str__(self):
        if self.d == 1:
            return str(self.n)
        return str(self.n) + "/" + str(self.d)


    def __repr__(self):
        if self.d == 1:
            return str(self.n)
        return str(self.n) + "/" + str(self.d)


    def __mul__(self,multiplier):
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
        if type(divisor) == int:
            divisor = Rational(divisor)
        return self*divisor.inv()
    
    
    def __rtruediv__(self,dividend):
        if type(dividend) == int:
            dividend = Rational(dividend)
        return self.inv()*dividend


    def __floordiv__(self,divisor):
        if type(divisor) == int:
            divisor = Rational(divisor)
        q = self*divisor.inv()
        v = q.n // q.d
        return v


    def __mod__(self,modulus):
        if type(modulus) == int:
            modulus = Rational(modulus)
        if modulus > self:
            return self
        else:
            a = self.copy()
            while a > modulus:
                a -= modulus
            return a


    def __add__(self,addend):
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
        return self + -addend


    def __rsub__(self,addend):
        return addend + -self


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
    
    
    def __pow__(self,power):
        assert type(power) == int,"Only powers of integers are supported"
        if power == 0:
            return Rational(1)
        if power == 1:
            return self
        else:
            n = self.n**power
            d = self.d**power
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


    def whole_part(self):
        """The whole part of the fraction"""
        return self.n // self.d


    def fractional_part(self):
        """The fractional part of the fraction"""
        return Rational(self.n % self.d, self.d)
    
    
    def mixed_form(self):
        """Whole and fractional part"""
        w = self.whole_part()
        f = self.fractional_part()
        return w,f
    
    
    def digits(self,n):
        """Return the decimal representation of the fraction out to n digits"""
        N = self.n
        D = self.d
                
        pos = 0
        digits = []
        m = []
        ctr = 0
        
        for ctr in range(n):
            digits.append(N//D)
            N = (N % D)*10
            m.append(N)
        
        if(pos == 0):
            x1 = str(digits[0])
            x2 = "".join(str(e) for e in digits[1:])
            out = "{}.{}".format(x1,x2)
            
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






if __name__ == '__main__':
    r = Rational(32,7)
    print(f"r   = {r}")
    print(f"1/r = {1/r}")
    print(f"3/r = {3/r}")

    