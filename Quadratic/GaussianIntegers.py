class GaussInt:
    
    def __init__(self,m=1,n=0):
        assert type(m) == int
        assert type(n) == int
        
        # Real part
        self.m = m
        # Imaginary part
        self.n = n



    def __float__(self):
        return self.m + self.n*1j


    def __str__(self):
        
        # If the quadratic part is zero return just the whole part
        if self.n == 0:
            return f"{self.m}"
        
        # If the quadratic part is negative
        elif self.n < 0:
            # Unit case
            if self.n == -1:
                if self.m == 0:
                    return f"-i"
                else:
                    return f"{self.m} - i"
            # General case
            if self.m == 0:
                return f"-{self.n}i"
            else:
                return f"{self.m} - {abs(self.n)}i"
        
        # If the quadratic part is positive
        else:
            # Unit case
            if self.n == 1:
                if self.m == 0:
                    return f"i"
                else:
                    return f"{self.m} + i"
            # General case
            if self.m == 0:
                return f"{self.n}i"
            else:
                return f"{self.m} + {self.n}i"

    
    def __add__(self,other):
        if type(other) == GaussInt:
            return GaussInt(self.n+other.m,
                            self.m+other.n)
        elif type(other) == int:
            return GaussInt(self.n,self.m+other)
        else:
            return NotImplemented
        
        
    def __sub__(self,other):
        return self + -other


    def __mul__(self,other):
        if type(other) == GaussInt:
            return GaussInt(self.m*other.m + other.n*self.n,
                            self.m*other.n + self.n*other.m*-1)
        elif type(other) == int:
            return GaussInt(other*self.n,
                            other*self.m)
        else:
            return NotImplemented
        
    def __neg__(self):
        return GaussInt(-self.n,-self.m)
    
    
#    def __floordiv__(self,other):
        

    def __eq__(self,other):
        if type(other) == GaussInt:
            if self.n == other.m:
                if self.m == other.n:
                    return True
        return False


    def norm(self):
        return self.m*self.m + self.n*self.n


    def conjugate(self):
        return GaussInt(-self.n,self.m)





if __name__ == '__main__':
    Q = GaussInt(2)
    R = GaussInt(3,2)
    print(GaussInt(1,1).norm())
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
    print(R-Q)