from Rational.RationalType import Rational

class CFrac:
    
    def __init__(self,terms):
    
        if type(terms) == Rational:
            self.terms = frac_to_cfrac(terms)
        else:
            try:
                iter(terms)
            except:
                terms = [terms]
                
            for i in terms:
                if type(i) != int:
                    raise TypeError(f"all values of L must be int not {type(i)}")
    
            self.terms = terms


    def __str__(self):
        out = str(self.terms)
        out = out.replace(",",";",1)
        return out
    
    
    def __len__(self):
        return len(self.terms)
    
    
    def __getitem__(self,n):
        """Make CFrac accessible by indexing"""
        return self.terms[n]


    def __setitem__(self,n,val):
        """Allow valid terms to be set"""    
        if type(val) != int:
            raise TypeError(f"Values must be integers not {type(val)}")
        self.terms[n] = val
        

    def __delitem__(self,n):
        """Remove items"""    
        del self.terms[n]

    
    def insert(self,n,val):
        """Insert item"""
        if type(val) != int:
            raise TypeError(f"Values must be integers not {type(val)}")
        self.terms.insert(n,val)
    
    
    def __add__(self,other):
        if type(other) == list:
            return CFrac(self.terms + other)
        else:
            return NotImplemented
        
        
    def append(self,other):
        if type(other) == list:
            self.terms += other
        else:
            raise TypeError(f"Can only append list not {type(other)}")


    def _pretty_name(self):
        """Name formatted for LaTeX"""

        if len(self) == 1:
            return str(self[0])
        
        else:
        
            prm = "#+\cfrac{1}{*}"
            out = "*"
            for i in self[:-1]:
                out = out.replace("*",prm)
                out = out.replace("#",str(i))
            out = out.replace("*",str(self[-1]))
            return out
        

    pretty_name = property(_pretty_name)


def frac_to_cfrac(R):
    """Canonical simple continued fraction representation"""
    if type(R) != Rational:
        raise TypeError(f"Input must be Rational not {type(R)}")
   
    L = []
    while True:
        w,f = R.mixed_form()
        L.append(w)
        if f == 0:
            break
        R = f.inv()
    return L


def cfrac_to_frac(C):
    """Convert a continued fraction to a Rational"""
    if type(C) != CFrac:
        raise TypeError(f"Input must be CFrac not {type(C)}")

    L = C.terms
    
    N = [1,L[0]]
    D = [0,1]
    con = 2
    
    while con < len(C)+1:
        N.append( L[con-1] * N[con-1] + N[con-2] )
        D.append( L[con-1] * D[con-1] + D[con-2] )
        con += 1
        
    return Rational(N[-1],D[-1])


def cfrac_convergents(C):
    """Rational convergents of a simple continued fraction."""
    if type(C) != CFrac:
        raise TypeError(f"Input must be CFrac not {type(C)}")
    
    T = C.terms
    N = [1,T[0]]
    D = [0,1]
    con = 2
    
    yield Rational(N[-1],D[-1])
    
    while con < len(C)+1:
        N.append( T[con-1] * N[con-1] + N[con-2] )
        D.append( T[con-1] * D[con-1] + D[con-2] )

        yield Rational(N[-1],D[-1])
        
        con += 1
        
        
def cfrac_semiconvergents(C):
    """Rational semiconvergents of a simple continued fraction."""
    
    if type(C) != CFrac:
        raise TypeError(f"Input must be CFrac not {type(C)}")
    
    a = C.terms
    Q = cfrac_to_frac(C)

    prev = Rational(a[0])
    for pos,val in enumerate(a):
        # Try appending the floor of half the next convergent
        semi = a[:pos]+[(val-1)//2+1]
        semi = CFrac(semi)
        
        # If it is worse than the last semiconvergent add 1
        if abs(cfrac_to_frac(semi) - Q)  >  abs(prev - Q):
            semi.terms[pos] += 1
            
        while semi.terms[pos] <= val:
            yield prev
            prev = cfrac_to_frac(semi)
            semi.terms[pos] += 1
    yield Q




if __name__ == '__main__':

    C = CFrac([8,11,4,2,7])
    print(C)
    print(C.pretty_name)
    
    
    
#    print(f"\n\nSemiconvergents of {R}")
#    for i in cfrac_semiconvergents(C):
#        print(i)
#    
#    print()
#    print(C)
#    C += [1,1]
#    print(C)
#    C.insert(3,5)
#    print(C)
#    C[1] = 7
#    print(C)
#    C[2] += 9
#    print(C)
#    del C[6]
#    print(C)

        