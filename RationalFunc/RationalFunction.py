from Poly import QPoly, poly_factor
from Rational import Rational

class RationalFunc:
    
    def __init__(self,N,D):
        assert type(N) == QPoly
        assert type(D) == QPoly
        self.N = N
        self.D = D

        self.simplify()


    def simplify(self):
        NF = poly_factor(self.N)
        DF = poly_factor(self.D)
        
        for F in DF:
            ## TODO: account for roots with multiplicity
            if F in NF:
                self.N //= F
                self.D //= F


    def __str__(self):
        if str(self.D) == "1":
            return f"{self.N}"
        return f"({self.N}) / ({self.D})"
    
    
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
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * 4
    Q = QPoly( [1,0,1] ) * QPoly( [-2,3] )
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