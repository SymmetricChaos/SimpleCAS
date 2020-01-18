from Utility import round_div, int_root
import re
from math import sqrt, atan

class GaussInt:
    
    def __init__(self,re=0,im=0):
        assert type(re) == int
        assert type(im) == int
        
        # Real part
        self.re = re
        # Imaginary part
        self.im = im


    def __complex__(self):
        """Convert to a normal Python complex number"""
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


    def __repr__(self):
        return str(self)


    def __add__(self,other):
        if type(other) == GaussInt:
            return GaussInt(self.re+other.re,
                            self.im+other.im)
        elif type(other) == int:
            return GaussInt(self.re+other,self.im)
        else:
            return NotImplemented


    def __radd__(self,other):
        return self+other
        
        
    def __sub__(self,other):
        return self + -other
    
    
    def __rsub__(self,other):
        return other + -self


    def __mul__(self,other):
        if type(other) == GaussInt:
            return GaussInt(self.re*other.re - self.im*other.im,
                            self.re*other.im + self.im*other.re)
        elif type(other) == int:
            return GaussInt(other*self.re,
                            other*self.im)
        else:
            return NotImplemented


    def __rmul__(self,other):
        return self*other


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


    # Note unusual form of division used in order to make the Division Theorem
    # hold
    def __floordiv__(self,other):
        """Euclidean division"""
        if other in [0,GaussInt(0,0)]:
            return ZeroDivisionError
        if type(other) == int:
            return GaussInt(self.re//other,self.im//other)
        if type(other) == GaussInt:
            s = self*other.conj
            n = other.norm
            return GaussInt(round_div(s.re,n),round_div(s.im,n))
        else:
            return NotImplemented


    def __mod__(self,other):
        """Remainder after Euclidean division"""
        return self - (other*(self//other))
        

    def __eq__(self,other):
        """Check for equality"""
        if type(other) == GaussInt:
            if self.re == other.re:
                if self.im == other.im:
                    return True
        elif type(other) == int:
            if self.re == other and self.im == 0:
                return True
        return False


    def __hash__(self):
        return hash(f"CustomGaussInt{self}")
    

    def _norm(self):
        """The norm of the number"""
        return self.re*self.re + self.im*self.im


    def _conjugate(self):
        """The conjugate of the number"""
        return GaussInt(self.re,-self.im)
    
    
    def _modulus(self):
        """Distance from the origin, returns a float"""
        return sqrt(self.norm)


    def _argument(self):
        """Angle relative to the positive reals, returns a float"""
        return atan(self.im/(self.modulus+self.re))
    
    
    norm = property(_norm)
    conj = property(_conjugate)
    modulus = property(_modulus)
    argument = property(_argument)





def all_gauss_int():
    """Generate a spiral of gaussian integers"""
    
    R, L = 1, 2
    D, U = 1, 2
    x, y = 0, 0
    
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
    

# GCD is ambiguous in the gaussian integers, there can be up to four, though
# all are unit multiple of each other
def gauss_gcd(a,b):
    """Returns a greatest common divisor of two gaussian integers"""
    if a == GaussInt(0,0):
        return b
    else:
        return gauss_gcd(b%a,a)


def str_to_gauss(S):
    
    S = S.replace(" ","")
    
    if S == "i":
        return GaussInt(0,1)
    
    p = re.findall("-?\d+",S)
    if re.fullmatch("-?\d+\+\d*i",S):
        return GaussInt(int(p[0]),int(p[1]))
    
    elif re.fullmatch("-?\d+-\d*i",S):
        return GaussInt(int(p[0]),int(p[1]))
    
    elif re.fullmatch("-?\d+",S):
        return GaussInt(int(S))
    
    elif re.fullmatch("-?\d+i",S):
        return GaussInt(0,int(S[:-1]))
    
    else:
        raise Exception("Not a valid input")


def associates(a):
    """Integer multiples of a"""
    L = {a}
    for i in range(3):
        a *= GaussInt(0,1)
        L.add(a)

    return L


def all_with_norm(n):
    """Yield all gaussian integers with a given norm"""
    out = set()
    
    for a in range(int_root(n)+1):
        B = n - a**2
        b = int_root(B)
        if b**2 == B:
            out = out.union(associates(GaussInt(a,b)))
            out = out.union(associates(GaussInt(b,a)))

    for i in out:
        yield i


if __name__ == '__main__':
    
    import random
    
    Q = GaussInt(1,2)
    R = GaussInt(3,2)
    
    print("Spiral of first twenty four gaussian integers")
    for i,j in enumerate(all_gauss_int()):
        if i > 24:
            break
        print(j)
    
    
    print(f"\n\nFrist ten ideals of {R}")
    for i,j in enumerate(ideal(R)):
        if i > 10:
            break
        print(j)
    
    print("\n\n\nDemonstrate Gaussian Integer Arithmetic")

    
    print("\nBasic operations:")
    print(f"Q   = {Q}")
    print(f"R   = {R}")
    print(f"Q+R = {Q+R}")
    print(f"Q-R = {Q-R}")
    print(f"Q*R = {Q*R}")
    print(f"Q^2 = {Q**2}")
    print(f"-Q  = {-Q}")
    
    print("\n\nThe Division Theorem for Gaussian integers says that it is always the case that for the numbers a and b we can find numbers x and y such that:")
    print("\na = b*x + y\nand\ny.norm < b.norm")
    
    a = GaussInt(27,-23)
    b = GaussInt(8,1)
    
    print()
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a//b = {a//b}")
    
    print()
    print(f"{a} = ({b})*({a//b}) + ({a%b})")
    
    print()
    print(f"N({a%b})   = {(a%b).norm}")
    print(f"N({b}) = {b.norm}")
    

    print("\n\nNonstandard operations:")
    print(f"R      = {R}")
    print(f"R.norm = {R.norm}")
    print(f"R.conj = {R.conj}")
    print(f"R.re   = {R.re}")
    print(f"R.im   = {R.im}")
    print(f"R.modulus = {R.modulus:.4}")
    print(f"R.argument = {R.argument:.4}")
    
    
    print("\n\nGCD")
    a = GaussInt(-6,6)
    b = GaussInt(3,-9)
    print(f"a = {a}")
    print(f"b = {b}")
    g = gauss_gcd(a,b)
    print(f"gcd = {g}")
    print(f"a//g = {a//g}")
    print(f"b//g = {b//g}")
    print(f"a = {(a//g)*g}")
    print(f"b = {(b//g)*g}")
    
    
    print("\n\nCheck str_to_gauss inputs")
    for g in ["6","7i","2 -7i","1 + 2i","i","b","5j"]:
        try:
            x = str_to_gauss(g)
            print(f"{g} gives {g}",type(x))
        except:
            print(f"{g} gave an error")


    G = GaussInt(-5,2)
    print(f"\n\nAssociates of {G}")
    print(associates(G))
            
        
    m = GaussInt(1,2)
    print(f"\n\nZ[i]/({m})")
    for i in range(10):
        a,b = random.randint(10,30), random.randint(10,30)
        g = GaussInt(a,b)
        print(f"{g} = {g%m}")