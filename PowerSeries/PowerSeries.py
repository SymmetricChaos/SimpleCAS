from Rational import cast_to_rational
from Poly import QPoly
import types

class PSeries:
    
    def __init__(self,a,c=0):
        if not isinstance(a, types.GeneratorType):
            raise Exception(f"{a} is not iterable")
        self.a = a
        self.c = cast_to_rational(c)
    

    def __str__(self):
        return self.head(2)


    def head(self,N):
        out = ""
        for pos,val in enumerate(self.a):
            if pos > N:
                break
            
            if val == 0:
                continue
            
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


    def cast_to_poly(self,N):
        """Truncates the power series and returns a polynomial"""
                
        P = QPoly([0])
        x = QPoly([0,1])
        for pos,val in enumerate(self.a):
            if pos > N:
                break
            P += val*(x-self.c)**pos
        return P


    def evaluate(self,x,N):
        """Truncates the power series and evakuates it"""
                
        x = cast_to_rational(x)

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
            c = f"+{abs(c)}"
        elif c > 0:
            c = f"-{c}"
            
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
        out = 1
        while True:
            yield out*out
            out += 1
    
    
    P = PSeries(sq(),1)
    print(P)
    print(f"P.head(3) = {P.head(3)}")
    print(f"\nCast the first four terms to a polynomial:\n{P.cast_to_poly(4)}")
    print(f"\nEvaluate the first four terms at x = 1:\n{P.evaluate('1/2',4)}")
