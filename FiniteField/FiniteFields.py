from Poly import ZPoly, zpoly_egcd



class FiniteField:
    
    def __init__(self,poly,R):
        self.poly = poly % R
        self.R = R


    def __str__(self):
        return f"{self.poly}"
    
    
    def __repr__(self):
        return f"{self.poly}"


    def __add__(self,other):
        return FiniteField(self.poly+other.poly,self.R)


    def __mul__(self,other):
        return FiniteField(self.poly*other.poly,self.R)


    def __sub__(self,other):
        return FiniteField(self.poly-other.poly,self.R)
    

    def __truediv__(self,other):
        return FiniteField(ff_div(self.poly,other.poly,self.R),self.R)



def finite_field_example(P):


    S = FiniteField(ZPoly([0,1],P.M),P)
    out = FiniteField(ZPoly([1],P.M),P)
    
    L = []
    
    elems = (P.M)**(len(P)-1)
    
    for i in range(1,elems):
        if out in L:
            raise Exception("Not a finite field")
        L.append(out)
        out = (out * S)

    for i in L:
        print(i)
    
    return L




def ff_inv(a, R):
    """Modular Multiplicative Inverse"""
    
    a = a % R
    
    g, x, _ = zpoly_egcd(a, R)
    if g != ZPoly([1],a.M):
        raise ValueError(f"Multiplicative inverse of {a} mod {R} does not exist")
    else:
        return x % R
    
    
def ff_div(a,b,R):
    if b == R or str(b) == "0":
        raise ZeroDivisionError
    return (a * ff_inv(b,R)) % R




    

    
if __name__ == '__main__':
    import random

    P = ZPoly( [1,0,0,1,0,1], 2 )
    L = finite_field_example(P)
    
    print(f"\n\nFinite Field of Characteristic 2 reduced by {P}")

    print("\n\nIn a field of characteristic two every element is its own additive inverse.")
    for i in range(3):
        a, = random.sample(L,1)
        print(f"({a}) + ({a}) = {(a+a)}")
        print()
        
    print("\n\nExamples of Division over the Finite Field")
    for i in range(3):
        a,b = random.sample(L,2)
        if str(b) == "0":
            continue
        print(f"({a}) / ({b}) = {a/b}")
        print()
