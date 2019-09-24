from Poly import QPoly, poly_factor

class RationalFunc:
    
    def __init__(self,N,D):
        assert type(N) == QPoly
        assert type(D) == QPoly
        self.N = N
        self.D = D
        
#    def simplify(self):
#        NF = poly_factor(self.N)
#        DF = poly_factor(self.D)
#        
#        for F in DF:
            
if __name__ == '__main__':
    pass