from Utility import prime_factorization

class GaussInt:
    
    def __init__(self,re=1,im=0):
        assert type(re) == int
        assert type(im) == int
        
        # Real part
        self.re = re
        # Imaginary part
        self.im = im


    def __complex__(self):
        return complex(self.re,self.im)


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


    def __pow__(self,pwr):
        if type(pwr) != int:
            raise TypeError(f"pwr must be a non-negative positive integer not {type(pwr)}")
        if pwr < 0:
            raise ValueError("pwr must be non-negative")
        
        # For negative powers invert then use recursion
        if pwr == 0:
            return GaussInt(1)
        elif pwr == 1:
            return self
        else:
            out = self
            for i in range(pwr-1):
                out *= self
            return out


#    def __floordiv__(self,other):
#        if type(other) == int:
#            return
#        if type(other) == GaussInt:
#            return
#        else:
#            return NotImplemented
        

    def __eq__(self,other):
        if type(other) == GaussInt:
            if self.re == other.re:
                if self.im == other.im:
                    return True
        return False


    def __hash__(self):
        return hash(f"CustomGaussInt{self}")
    

    def _norm(self):
        return self.re*self.re + self.im*self.im


    def _conjugate(self):
        return GaussInt(self.re,-self.im)
    
    norm = property(_norm)
    conjugate = property(_conjugate)



def factor_gauss(a):
    
    # Factors of the norm of the number must be the norms of the factors of the
    # number
    F = prime_factorization(a.norm)
    print(F)
    
    # Residue mod 4
    res = [f%4 for f in F]
    print(res)
    

## TODO: Ideally should be 
def all_gauss_int():
    diag = 1
    prev = set()
    while True:
        a = 0
        b = diag
        for i in range(-diag,diag+1):
            r = GaussInt(a,b)
            if r not in prev:
                if b == 0 or a == 0:
                    prev.add(r)
                    yield r
                    prev.add(-r)
                    yield -r
                else:
                    prev.add(r)
                    yield r
                    prev.add(-r)
                    yield -r
                    prev.add(r.conjugate)
                    yield r.conjugate
                    prev.add(-r.conjugate)
                    yield -r.conjugate
            a += 1
            b -= 1
        diag += 1


#def ideals(a):
#    yield GaussInt(0)
#    yield a
    


#def steins_gauss_gcd(a,b,d=1):
#    """A slightly faster gcd algorithm"""
#    if a == b or a == -b:
#        return d*a
#    if b.norm() == 1:
#        return d
#    if b == GaussInt(0):
#        return d*a
#    if a.re % 2 == 0 and re.im % 2 == 0:
#        return steins_gauss_gcd()
#    
#    if a.re % 2 == 0 and re.im % 2 == 1:
#        
#    if a.re % 2 == 1 and re.im % 2 == 0:
#        
#    if a.re % 2 == 1 and re.im % 2 == 1:
        



if __name__ == '__main__':
#    Q = GaussInt(2)
#    R = GaussInt(3,2)
#    print(Q)
#    print(R)
#    print(Q+R)
#    print(Q*R)
#    print(Q*Q)
#    print(R*R)
#    print(R.norm)
#    print(R.conjugate)
#    print(Q+2)
#    print(R*2)
#    print(-R)
#    print(R-Q)
#    print(R**2)
#    print(R*R)
#    print(R.re)
#    print(R.im)
#    
#    G = GaussInt(440,-55)
#    factor_gauss(G)
    
    for i,j in enumerate(all_gauss_int()):
        if i > 20:
            break
        print(j)