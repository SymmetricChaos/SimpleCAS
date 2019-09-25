from Poly import QPoly, poly_factor

class RationalFunc:
    
    def __init__(self,N,D=QPoly([1])):
        
        if type(N) == QPoly:
            pass
        else:
            try:
                N = QPoly( [N] )
            except:
                raise ValueError(f"Could not coerce {N} to QPoly")
        if type(D) == QPoly:
            pass
        else:
            try:
                D = QPoly( [D] )
            except:
                raise ValueError(f"Could not coerce {D} to QPoly")
            
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


    # TODO: accept other types
    def __add__(self,other):
        if type(other) == RationalFunc:
            return RationalFunc(self.N*other.D + other.N*self.D, self.D*other.D)
        else:
            return self + RationalFunc(other)


    # TODO: accept other types
    def __sub__(self,other):
        if type(other) == RationalFunc:
            return self + -other
        else:
            return self - RationalFunc(other)







# TODO: Turn these into proper unit tests
# need to include: roots with multiplicity, multiplication by negative numbers,
# division by zero, division by 1, division by int, 0 divided by Qpoly,
# int divided by Qpoly        
if __name__ == '__main__':
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * QPoly( [7,3] ) * 4
    Q = QPoly( [1,0,1] ) * QPoly( [-2,1] ) * QPoly( [-1,1] ) * QPoly( [-1,1] )
    R = RationalFunc(P,Q)
    
    print(P)
    print(Q)
    print(R)
    
    print(f"R(3) = {R(3)}")
    
    print(f"R*R = {R*R}")
    print(f"R+R = {R+R}")
    
    print()
    
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * 4
    
    print(f"P   = {P}")
    print(f"P/2 = {RationalFunc(P,2)}")