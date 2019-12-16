from Utility import gcd

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
        
        # If the real part is zero just return the imaginary part
        if self.re == 0:
            if self.im == 1:
                return "i"
            elif self.im == -1:
                return "-i"
            else:
                return f"{self.im}i"
        
        # If the imaginary part is negative
        elif self.im < 0:
            # Unit case
            if self.im == -1:
                return f"{self.re} - i"
            # General case
            else:
                return f"{self.re} - {abs(self.im)}i"
        
        # If the imaginary part is positive
        else:
            # Unit case
            if self.im == 1:
                return f"{self.re} + i"
            # General case
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


    # Division need to follow the division theorem and produce a number that 
    # has a smaller norm
    def __floordiv__(self,other):
        if type(other) == int:
            return GaussInt(self.re//other,self.im//other)
        if type(other) == GaussInt:
            s = self*other.conjugate
            n = other.norm
            return GaussInt(round_div(s.re,n),round_div(s.im,n))
        else:
            return NotImplemented


    def __mod__(self,other):
        return self - (other*(self//other))
        

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
    conj = property(_conjugate)
    conjugate = property(_conjugate)





def all_gauss_int():
    """Generate a spiral of gaussian integers"""
    
    R = 1
    D = 1
    L = 2
    U = 2
    x = 0
    y = 0
    
    yield GaussInt(x,y)
    
    while True:

        for i in range(R):
            x += 1
            yield GaussInt(x,y)
        R += 2
        
        for i in range(D):
            y -= 1
            yield GaussInt(x,y)
        D += 2
        
        for i in range(L):
            x -= 1
            yield GaussInt(x,y)
        L += 2
        
        for i in range(U):
            y += 1
            yield GaussInt(x,y)
        U += 2


def ideal(a):
    """Generate the ideal of a given gaussian integer"""
    for i in all_gauss_int():
        yield i*a
    

def round_div(a,b):

    t = ((a % b)*10)//b
    if t >= 5:
        return (a//b)+1
    else:
        return a//b
    
    
    



if __name__ == '__main__':
    
    print("Generator of Gaussian Integers")
    for i,j in enumerate(all_gauss_int()):
        if i > 20:
            break
        print(j)
    

    
    print("\n\n\nDemonstrate Gaussian Integer Arithmetic")
    Q = GaussInt(1,2)
    R = GaussInt(3,2)
    
    
    print("\n\nBasic operations:")
    print(f"Q   = {Q}")
    print(f"R   = {R}")
    print(f"Q+R = {Q+R}")
    print(f"Q-R = {Q-R}")
    print(f"Q*R = {Q*R}")
    print(f"Q^2 = {Q**2}")
    print(f"-Q  = {-Q}")
    

    
    print("\n\nNonstandard operations:")
    
    print(f"R      = {R}")
    print(f"R.norm = {R.norm}")
    print(f"R.conj = {R.conj}")
    print(f"R.re   = {R.re}")
    print(f"R.im   = {R.im}")  
    

        
    print("\n\n\nCheck that division works")
    
    
    print(f"Q   = {Q}")
    print(f"R   = {R}")
    print(f"R/Q = {R//Q}")
    print(f"R%Q = {R%Q}")
    
    print(f"\n({Q}) * ({R//Q}) = {Q*(R//Q)}")
    print(f"\n({Q}) * ({R//Q}) + {R%Q} = {Q*(R//Q)+R%Q}")
    
    
    print("\n\nThe division theorem says that it is always the case that for the numbers a and b we can find numbers x and y such that:")
    print("a = b*x + y\nand\ny.norm < b.norm")
    
    a = GaussInt(27,-23)
    b = GaussInt(8,1)
    
    print("\n\n")
    print(a)
    print(b)
    print(a//b)
    print(a%b)
    
    print((a%b).norm)
    print((b).norm)
    