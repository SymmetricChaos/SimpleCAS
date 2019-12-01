class GaussInt:
    
    def __init__(self,re=0,im=1):
        assert type(re) == int
        assert type(im) == int
        
        # Real part
        self.re = re
        # Imaginary part
        self.im = im



    def __complex__(self):
        return self.re + self.im*1j


    def __str__(self):
        
        # If the imaginary part is zero return just the whole part
        if self.im == 0:
            return f"{self.re}"
        
        # If the imaginary part is negative
        elif self.im < 0:
            # Unit case
            if self.im == -1:
                if self.re == 0:
                    return f"-i"
                else:
                    return f"{self.re} - i"
            # General case
            if self.re == 0:
                return f"-{self.re}i"
            else:
                return f"{self.re} - {abs(self.im)}i"
        
        # If the quadratic part is positive
        else:
            # Unit case
            if self.im == 1:
                if self.re == 0:
                    return f"i"
                else:
                    return f"{self.re} + i"
            # General case
            if self.re == 0:
                return f"{self.im}i"
            else:
                return f"{self.re} + {self.im}i"

    
    def __add__(self,other):
        if type(other) == GaussInt:
            return GaussInt(self.re+other.re,
                            self.im+other.im)
        elif type(other) == int:
            return GaussInt(self.re+other,self.im)
        else:
            return NotImplemented
        
        
    def __sub__(self,other):
        return self + -other


    def __mul__(self,other):
        if type(other) == GaussInt:
            return GaussInt(self.re*other.re - self.im*other.im,
                            self.re*other.im + self.im*other.re)
        elif type(other) == int:
            return GaussInt(other*self.re,
                            other*self.im)
        else:
            return NotImplemented
        
    def __neg__(self):
        return GaussInt(-self.re,-self.im)
    
    
#    def __floordiv__(self,other):
        

    def __eq__(self,other):
        if type(other) == GaussInt:
            if self.re == other.re:
                if self.im == other.im:
                    return True
        return False


    def norm(self):
        return self.re*self.re + self.im*self.im


    def conjugate(self):
        return GaussInt(self.re,-self.im)



def gauss_egcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = gauss_egcd(b % a, a)
        return (g, x - (b // a) * y, y)



if __name__ == '__main__':
    Q = GaussInt(2)
    R = GaussInt(3,2)
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