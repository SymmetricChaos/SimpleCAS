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
    

    def head(self,N):
        out = ""
        for pos,val in enumerate(self.a):
            if pos > N:
                break
            
            if val < 0:
                val = abs(val)
                sgn = " - "
            else:
                sgn = " + "
            
            if pos == 0:
                if sgn == " - ":
                    sgn = "-"
                if sgn == " + ":
                    sgn = ""
            
            out += sgn + term(val,self.c,pos)
            
        return out + " + ..."
    

    def truncate(self,N):
        """Truncates the power series"""
        return PSeries(self.a[:N],self.c)


    def cast_to_poly(self,N=None):
        """Truncates the power series and returns a polynomial"""
        
        if N == None:
            try:
                N = len(self.a)
            except:
                raise Exception(f"{self.a} has no len() so N must be supplied")
        else:
            N = N
        
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
                raise Exception(f"{self.a} has no len() so N must be supplied")
        else:
            N = N
        
        x = coerce_to_rational(x)
        
        out = 0
        for pos,val in enumerate(self.a):
            if pos > N:
                break
            out += val*(x-self.c)**pos
            
        return out
        
    
def term(a,c,p):
    if a == 0:
        return "0"
    
    if c == 0:
        if a == 1:
            if p == 0:
                return f"1"
            elif p == 1:
                return f"x"
            else:
                return f"x^{p}"
            
        else:
            if p == 0:
                return f"{a}"
            elif p == 1:
                return f"{a}x"
            else:
                return f"{a}x^{p}"
            
    else:
        if c < 0:
            c = f" + {abs(c)}"
        elif c > 0:
            c = f" - {c}"
            
        if a == 1:
            if p == 0:
                return f"1"
            elif p == 1:
                return f"(x{c})"
            else:
                return f"(x{c})^{p}"
            
        else:
            if p == 0:
                return f"{a}"
            elif p == 1:
                return f"{a}(x{c})"
            else:
                return f"{a}(x{c})^{p}"
        
        
        
if __name__ == '__main__':
    def sq():
        out = 0
        while True:
            yield out*out
            out += 1
    
    
    P = PSeries(sq(),1)
    print(P.a)
    print(P.c)
    
    print(P.head(3))
    
    print()
    print(P.cast_to_poly(4))
    print(P.evaluate("1/2",4))
