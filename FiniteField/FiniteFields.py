from Poly import ZPoly, zpoly_egcd



class FF2:
    
    def __init__(self,poly,R):
        if poly.M != 2:
            raise ValueError("Field must be of characteristic 2")
        if R.M != 2:
            raise ValueError("Field must be of characteristic 2")
        self.poly = poly % R
        self.R = R


    def __str__(self):
        return str(self.poly)

    
    def __repr__(self):
        return str(self.poly)

    
    def bitstring(self):
        s = self.poly.coef + [0] * (len(self.R) - len(self.poly.coef) - 1)
        return "".join([str(i) for i in reversed(s)])

    
    def __add__(self,other):
        return FF2(self.poly+other.poly,self.R)


    def __mul__(self,other):
        return FF2(self.poly*other.poly,self.R)


    def __sub__(self,other):
        return FF2(self.poly-other.poly,self.R)
    

    def __truediv__(self,other):
        return FF2(ff_div(self.poly,other.poly,self.R),self.R)



def finite_field_example(P):


    S = FF2(ZPoly([0,1],P.M),P)
    out = FF2(ZPoly([1],P.M),P)
    
    L = [FF2(P,P)]
    
    elems = (P.M)**(len(P)-1)
    
    for i in range(1,elems):
        if out in L:
            raise Exception("Not a finite field")
        L.append(out)
        out = (out * S)

#    for i in L:
#        print(i)
    
    return L





def ff_inv(a, R):
    """Modular Multiplicative Inverse"""
    
    a = a % R
    
    g, x, _ = zpoly_egcd(a, R)
    if g != ZPoly([1],a.M):
        raise ValueError(f"Multiplicative inverse of {a.full_name} mod {R.full_name} does not exist")
    else:
        return x % R
    
    
def ff_div(a,b,R):
    if b == R or str(b) == "0":
        raise ZeroDivisionError
    return (a * ff_inv(b,R)) % R




    

    
if __name__ == '__main__':
    import random

    P = ZPoly( [1,1,1,0,0,0,0,1,1], 2 )
    L = finite_field_example(P)
    
    print(f"\n\nFinite Field of Characteristic 2 with {len(L)} elements\nReducing Polynomial: {P}")
        
    print("\n\nAddition and Subtraction and identical")
    for i in range(3):
        a,b = random.sample(L,2)
        print(f"{a.bitstring()} + {b.bitstring()} = {(a+b).bitstring()}")
        print(f"{a.bitstring()} - {b.bitstring()} = {(a-b).bitstring()}")
        print()
        
        
    print("\n\nExamples of Multiplication over the Finite Field")
    for i in range(3):
        a,b = random.sample(L,2)
        print(f"{a.bitstring()} * {b.bitstring()} = {(a*b).bitstring()}")
        print()
        
    print("\n\nExamples of Division over the Finite Field")
    for i in range(3):
        a,b = random.sample(L,2)
        if str(b) == "0":
            continue
        print(f"{a.bitstring()} / {b.bitstring()} = {(a/b).bitstring()}")
        print()

