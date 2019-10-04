from Poly import QPoly, poly_factor

class RationalFunc:
    
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
        DF = poly_factor(self.D)

        for F in DF:
            if self.N % F == QPoly( [0] ):
                self.N //= F
                self.D //= F


    def __str__(self):
        if str(self.N) == "0":
            return "0"
        if str(self.D) == "1":
            return str(self.N)

        if len(self.N) == 1:
            n = str(self.N)
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
        return RationalFunc(self.D,self.N)


    def __mul__(self,other):
        if type(other) == RationalFunc:
            return RationalFunc(self.N * other.N, self.D * other.D)
        else:
            return self * RationalFunc(other)
    
    
    def __truediv__(self,other):
        if type(other) == RationalFunc:
            return self * other.inv()
        else:
            return self / RationalFunc(other)


    def __neg__(self):
        return self*-1


    def __add__(self,other):
        if type(other) == RationalFunc:
            return RationalFunc(self.N*other.D + other.N*self.D, self.D*other.D)
        else:
            return self + RationalFunc(other)


    def __sub__(self,other):
        if type(other) == RationalFunc:
            return self + -other
        else:
            return self - RationalFunc(other)


    def degree(self):
        return max(self.N.degree(),self.D.degree())


    def pretty_name(self):
        if str(self.N) == "0":
            return "0"
        elif str(self.D) == "1":
            return str(self.N)
        else:
            return f"$\dfrac{{{self.N}}}{{{self.D}}}$"





# TODO: Turn these into proper unit tests
# need to include: roots with multiplicity, multiplication by negative numbers,
# division by zero, division by 1, division by int, 0 divided by Qpoly,
# int divided by Qpoly        
if __name__ == '__main__':
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * QPoly( [7,3] ) * 4
    Q = QPoly( [1,0,1] ) * QPoly( [-2,1] ) * QPoly( [-1,1] ) * QPoly( [-1,1] )
    R = RationalFunc(P,Q)
    
    print(f"P   = {P}\n")
    print(f"Q   = {Q}\n")
    print(f"P/Q = {R}\n")

    
    print(f"R   = {R}\n")
    print(f"R*P = {R*P}\n")
    print(f"R+P = {R+P}\n")
    
    print()
    print(f"R(3) = {R(3)}")
    print()
        
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * 4
    
    print(f"P   = {P}")
    print(f"P/2 = {RationalFunc(P,2)}")
    
    print("\nRationalFunc can accept lists and coerce them to QPoly")
    print("RationalFunc([1,0,1,1,2,0,1],[1,0,1])")
    print(RationalFunc([1,0,1,1,2,0,1],[1,0,1]))