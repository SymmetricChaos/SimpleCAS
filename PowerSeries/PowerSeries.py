from Rational import coerce_to_rational
from Poly import QPoly

class PSeries:
    
    def __init__(self,a,c=0):
        try: 
            iter(a)
        except:
            raise Exception(f"{a} is not iterable")
        self.a = a
        self.c = coerce_to_rational(c)
        
        
    def truncate(self,N):
        """Truncates the power series"""
        return PSeries(self.a[:N],self.c)


    def cast_to_poly(self,N):
        """Truncates the power series and returns a polynomial"""
        P = QPoly([0])
        x = QPoly([0,1])
        for pos,val in enumerate(self.a):
            if pos > N:
                break
            P += val*(x-self.c)**pos
        return P


    def evaluate(self,x,N=None):
        
        if N == None:
            try:
                N = len(self.a)
            except:
                raise Exception("When a has no len() N must be supplied")
        else:
            N = N
        
        x = coerce_to_rational(x)
        
        out = 0
        for pos,val in enumerate(self.a):
            if pos > N:
                break
            out += val*(x-self.c)**pos
            
        return out
        
        
if __name__ == '__main__':
    P = PSeries([1,1,1,1,1,1],4)
    print(P.a)
    print(P.c)
    
    print(P.cast_to_poly(3))
    print(P.evaluate(6))