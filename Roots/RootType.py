# Correct handling and evaluation of rational roots

from Rational import coerce_to_rational

class Root:
    
    def __init__(self,n,contents):
        self.n = coerce_to_rational(n).inv()
        self.contents = contents
    
#    # Need to have this interact with various types for content
#    def simplify()
    
    
    # TODO: handle various inputs in a pretty way
    def __str__(self):
        p = f"{self.n}" if self.n.d == 1 else f"({self.n})"
        return f"({self.contents})^{p}"
    

#    def __mul__(self,other):
        


if __name__ == '__main__':
    r = Root("1/2",8)
    print(r)