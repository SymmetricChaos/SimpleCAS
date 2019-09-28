from Rational import Rational, coerce_to_rational


# Extension of the rationals by a quadratic
class QuadraticRational:
    
    def __init__(self,q,m=1,n=0):

        self.q = coerce_to_rational(q)
        # Multiple of the quadratic
        self.m = coerce_to_rational(m)
        # Integer part
        self.n = coerce_to_rational(n)


    def __str__(self):
        # If the quadratic part is zero
        if self.m == 0:
            return f"{self.n}"
        # If the quadratic part is negative
        elif self.m < 0:
            # Unit case
            if self.m == -1:
                if self.n == 0:
                    return f"-√{self.q}"
                else:
                    return f"{self.n} - √{self.q}"
            # General case
            if self.n == 0:
                return f"-{self.m}√{self.q}"
            else:
                return f"{self.n} - {abs(self.m)}√{self.q}"
        # If the quadratic part is positive
        else:
            # Unit case
            if self.m == 1:
                if self.n == 0:
                    return f"√{self.q}"
                else:
                    return f"{self.n} + √{self.q}"
            # General case
            if self.n == 0:
                return f"{self.m}√{self.q}"
            else:
                return f"{self.n} + {self.m}√{self.q}"


    def __add__(self,other):
        if type(other) != QuadraticRational:
            other = QuadraticRational(self.q,0,other)
            
        if other.q == self.q:
            return QuadraticRational(self.q,
                                     self.m+other.m,
                                     self.n+other.n)


    def __radd__(self,other):
        return self + other


    def __sub__(self,other):
        return self + -other


    def __rsub__(self,other):
        return -self + other


    def __mul__(self,other):
        if type(other) != QuadraticRational:
            other = QuadraticRational(self.q,0,other)
            
        if other.q == self.q:
            return QuadraticRational(self.q,
                                     self.n*other.m + other.n*self.m,
                                     self.n*other.n + self.m*other.m*self.q)


    def __rmul__(self,other):
        return self*other


    def __neg__(self):
        return self*-1
    
    
    def norm(self):
        return self.n*self.n - self.q*self.m*self.m


    def conjugate(self):
        return QuadraticRational(self.q,-self.m,self.n)
    
    
    
    
    
if __name__ == '__main__':
    q = QuadraticRational(5)
    print(f"q              = {q}")
    print(f"1+0*q          = {1+0*q}")
    print(f"0*q            = {0*q}")
    print(f"1+q            = {1+q}")
    print(f"1-q            = {1-q}")
    print(f"1-2*q          = {1-2*q}")
    print(f"q*q            = {q*q}")
    print(f"q+q            = {q+q}")
    print(f"q*(2+q)        = {q*(2+q)}")
    print(f"(2+q)*(3+2*q)  = {(2+q)*(3+2*q)}")
    print(f"(2+q)*(3-2*q)  = {(2+q)*(3-2*q)}")
    print(f"(2+q)+(3+2*q)  = {(2+q)+(3+2*q)}")
    print("1/3" * q + "1/2")