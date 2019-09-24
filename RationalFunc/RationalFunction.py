from Poly import QPoly, poly_factor

class RationalFunc:
    
    def __init__(self,N,D):
        assert type(N) == QPoly
        assert type(D) == QPoly
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

        return f"{n}/{d}"


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





if __name__ == '__main__':
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * QPoly( [7,3] ) * 4
    Q = QPoly( [1,0,1] ) * QPoly( [-2,3] ) * QPoly( [-1,1] ) * QPoly( [-1,1] )
    R = RationalFunc(P,Q)
    
    print(P)
    print(Q)
    print(R)
    
    print(f"R(3) = {R(3)}")
    
    print()
    
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * 4
    Q = QPoly( [2] )
    R = RationalFunc(P,Q)
    
    print(P)
    print(Q)
    print(R)