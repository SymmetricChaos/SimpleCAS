# Field of rational functions with rational coefficients

from Poly import QPoly, poly_gcd

# TODO: make RFunc interact correctly with QPoly as much as possible

class RFunc:
    
    def __init__(self,N,D=QPoly([1])):
        
        if type(N) == QPoly:
            pass
        elif type(N) == list:
            N = QPoly( N )
        else:
            try:
                N = QPoly( [N] )
            except:
                raise Exception(f"Could not coerce {N} to QPoly")
        
        if type(D) == QPoly:
            pass
        elif type(D) == list:
            D = QPoly( D )
        else:
            try:
                D = QPoly( [D] )
            except:
                raise Exception(f"Could not coerce {D} to QPoly")
            
        self.N = N
        self.D = D

        self.simplify()


    def simplify(self):
        G = poly_gcd(self.N,self.D)
        self.N //= G
        self.D //= G


    def copy(self):
        return RFunc(self.N.copy(),self.D.copy())


    def __str__(self):
        if str(self.N) == "0":
            return "0"
        if str(self.D) == "1":
            return str(self.N)

        if len(self.N) == 1:
            n = str(self.N)
        else:
            if self.N.content < 0:
                n = f"-({-self.N})"
            else:  
                n = f"({self.N})"

        if len(self.D) == 1:
            d = str(self.D)
        else:
            d = f"({self.D})"

        return f"{n} / {d}"


    def __call__(self,val):
        n = self.N(val)
        d = self.D(val)
        
        if d == 0:
            return float('NaN')
        else:
            return n/d


    def evaluate(self,val):
        assert type(val) == list
        return [self(v) for v in val]
    

    def inv(self):
        return RFunc(self.D,self.N)


    def __mul__(self,other):
        if type(other) == RFunc:
            return RFunc(self.N * other.N, self.D * other.D)
        else:
            return self * RFunc(other)


    def __rmul__(self,other):
        return self*other
    
    
    def __pow__(self,pwr):
        if type(pwr) != int:
            raise TypeError(f"pwr must be an integer not {type(pwr)}")

        if pwr == 0:
            return RFunc([1],[1])
        else:
            out = self.copy()
            for i in range(abs(pwr)-1):
                out *= self
        
        if pwr < 0:
            return out.inv()
            
        return out
        
    
    def __truediv__(self,other):
        if type(other) == RFunc:
            return self * other.inv()
        else:
            return self / RFunc(other)


    def __neg__(self):
        return self*-1


    def __add__(self,other):
        if type(other) == RFunc:
            return RFunc(self.N*other.D + other.N*self.D, self.D*other.D)
        elif type(other) == QPoly:
            return self + RFunc(other)
        else:
            return self + RFunc([other])
        

    def __radd__(self,other):
        return self + other


    def __sub__(self,other):
        if type(other) == RFunc:
            return self + -other
        else:
            return self - RFunc(other)


    def degree(self):
        return max(self.N.degree(),self.D.degree())


    def derivative(self):
        N = (self.D * self.N.derivative()) - (self.N * self.D.derivative())
        D = self.D * self.D
        return RFunc(N,D)


    def _pretty_name(self):
        if str(self.N) == "0":
            return "0"
        elif str(self.D) == "1":
            return str(self.N)
        else:
            if self.N.content < 0:
                sgn = "-"
                n = -self.N
            else:
                sgn = ""
                n = self.N
            return f"${sgn}\dfrac{{{n}}}{{{self.D}}}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)





# TODO: Turn these into proper unit tests
# need to include: roots with multiplicity, multiplication by negative numbers,
# division by zero, division by 1, division by int, 0 divided by Qpoly,
# int divided by Qpoly        
if __name__ == '__main__':
    
    print("Rational functions are in simplest form")
    P = QPoly( [-28,16,-16,16,12] )
    Q = QPoly( [-2,5,-6,6,-4,1] )
    print(f"P          = {P}\n")
    print(f"Q          = {Q}\n")
    print(f"RFunc(P,Q) = {RFunc(P,Q)}")
    
    
    print("\n\nRational functions can quickly be created just by supplying lists")
    R = RFunc([1,0,1,1,2],[2,0,1])
    print("R = RFunc([1,0,1,1,2],[2,0,1])")
    print(f"R = {R}")


    print(f"\n\nderivative of R =\n{R.derivative()}")

    
    print("\n\nTest Operations")
    R = RFunc( [28,12], [2,-3,1] )
    S = RFunc( [1,0,0,1], [2,4,3] )
    P = QPoly( [3,5,1] )
    print(f"R      = {R}")
    print(f"S      = {S}")
    print(f"P      = {P}")
    print(f"-R     = {-R}")
    print(f"R+2    = {R+2}")
    print(f"2+R    = {2+R}")
    print(f"R+S    = {R+S}")
    print(f"S+R    = {S+R}")
    print(f"R*2    = {R*2}")
    print(f"2*R    = {2*R}")
    print(f"S**2   = {S**2}")
    print(f"S**-2  = {S**-2}")
    print(f"S+Q    = {S+Q}")