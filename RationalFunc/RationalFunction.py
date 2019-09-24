from Poly import QPoly, poly_factor

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
        return str(self.N) + "  /  " + str(self.D)





if __name__ == '__main__':
    P = QPoly( [1,0,1] ) * QPoly( [-1,1] ) * 4
    Q = QPoly( [1,0,1] ) * QPoly( [-2,3] )
    
    R = RationalFunc(P,Q)
    
    print(R)