from math import sqrt

class QuadInt:
    
    def __init__(self,q,m=1,n=0):
        assert type(q) == int
        assert type(m) == int
        assert type(n) == int
        
        # Quadratic extension
        self.q = q
        # Multiple of the quadratic
        self.m = m
        # Integer part
        self.n = n


    def __float__(self):
        return self.n + self.m*sqrt(self.q)


    def __str__(self):
        
        # If the quadratic part is zero return just the whole part
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
        if type(other) == QuadInt:
            if self.q == other.q:
                return QuadInt(self.q,
                               self.m+other.m,
                               self.n+other.n)
        elif type(other) == int:
            return QuadInt(self.q,self.m,self.n+other)
        else:
            return NotImplemented
        
        
    def __sub__(self,other):
        return self + -other


    def __mul__(self,other):
        if type(other) == QuadInt:
            if self.q == other.q:
                return QuadInt(self.q,
                               self.n*other.m + other.n*self.m,
                               self.n*other.n + self.m*other.m*self.q)
        elif type(other) == int:
            return QuadInt(self.q,
                           other*self.m,
                           other*self.n)
        else:
            return NotImplemented


    def __neg__(self):
        return QuadInt(self.q,-self.m,-self.n)
        

    def __eq__(self,other):
        if type(other) == QuadInt:
            if self.q == other.q:
                if self.m == other.m:
                    if self.n == other.n:
                        return True
        return False


    def conjugate(self):
        return QuadInt(self.q,-self.m,self.n)





if __name__ == '__main__':
    Q = QuadInt(2)
    R = QuadInt(2,3,2)
    print(Q)
    print(R)
    print(Q+R)
    print(Q*R)
    print(Q*Q)
    print(R*R)
    print(R.norm())
    print(R.conjugate())
    print(Q+2)
    print(R*2)
    print(-R)
    print(float(R))
    print(R-Q)