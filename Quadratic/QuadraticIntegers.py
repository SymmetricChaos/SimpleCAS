class QuadInt:
    
    def __init__(self,q,m=1,n=0):
        assert type(q) == int
        assert type(m) == int
        assert type(n) == int
        
        # Quadratic extension
        self.q = q
        # Multiple of the quadratic
        self.m = m
        # Integer part
        self.n = n
    
    
    
    def __add__(self,other):
        if from_same_ring(self,other):
            return QuadInt(self.q,
                                self.m+other.m,
                                self.n+other.n)
    def __mul__(self,other):
        if from_same_ring(self,other):
            return QuadInt(self.q,
                           self.n*other.m + other.n*self.m,
                           self.n*other.n + self.m*other.m*self.q)


def from_same_ring(A,B):
    if type(A) == QuadInt:
        if type(B) == QuadInt:
            return A.q == B.q
    return False