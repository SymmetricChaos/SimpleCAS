from Poly import ZPoly
from collections import Counter

class ZPolyProd:
    
    def __init__(self,terms,F):
        if type(terms) == list:
            self.terms = Counter(terms)
            
        elif type(terms) == ZPoly:
            self.terms = Counter([terms])
            
        elif type(terms) == Counter:
            self.terms = terms
            
        else:
            raise TypeError(f"Couldn't use type {type(terms)}")
            
        self.simplify_const()
        self.F = F
        del self.terms[1]


    def simplify_const(self):
        """Deal with constant terms"""
        const = 1
        remv = []
        for i in self.terms.items():
            if len(i[0]) == 1:
                const *= i[0]**i[1]
                remv.append(i[0])
        
        for t in remv:
            del self.terms[t]
            
        self.terms[const] = 1


    def cast_to_poly(self):
        """Multiply everything together as a ZPoly"""
        out = ZPoly([1])
        for val,pwr in self.terms.items():
            out *= val**pwr
        return out


    # TODO: Scalar multiplication needed
    def __mul__(self,other):
        if type(other) == ZPoly:
            A = self.terms.copy()
            A.update([other])
            return ZPolyProd(A,5)
        elif type(other) == ZPolyProd:
            A = self.terms.copy()
            A.update(other.terms)
            return ZPolyProd(A,5)
        else:
            return NotImplemented

    
    def __pow__(self,other):
        if type(other) != int:
            raise TypeError("Power of ZPolyProd must be an integer")
        if other < 1:
            raise TypeError("Power of ZPolyProd must be non-negative")
        
#        if other == 0:
#            issue with polys that might have different values of F
        if other == 1:
            return self
        else:
            out = self
            for i in range(other-1):
                out *= self
            return out
        

    def __len__(self):
        out = 0
        for i in self.terms:
            out += len(i)
        return out


    def __str__(self):
        out = []
        
        S = []
        for i in self.terms.keys():
            S.append(i)
        S.sort(key=len)
        
        for i in S:
            pwr = self.terms[i]
                        
            
            if pwr == 1:
                if len(i) == 1:
                    out.append(str(i))
                else:
                    out.append(f"({i})")
            else:
                if len(i) == 1:
                    out.append(f"{i}^{pwr}")
                else:
                    out.append(f"({i})^{pwr}")
        
        return "".join(out)


    # TODO: Need to guarantee that identical objects will have an indentical hash
#    def __hash__(self):
#        return hash(f"CustomZPolyProd{self}")


    def _pretty_name(self):
        out = []
        
        S = []
        for i in self.terms.keys():
            S.append(i)
        S.sort(key=len)
        
        for i in S:
            pwr = self.terms[i]
            
            if pwr == 1:
                if len(i) == 1:
                    out.append(str(i))
                else:
                    out.append(f"({i.pretty_name})")
            else:
                if len(i) == 1:
                    out.append(f"{i.pretty_name}^{{{pwr}}}")
                else:
                    out.append(f"({i.pretty_name})^{{{pwr}}}")
        
        J = "\;".join(out)
        J = J.replace("$","")
        return f"${J}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    
    
if __name__ == '__main__':
    P = ZPoly( [1,2,3], 5)
    Q = ZPoly( [2,4], 5)
    C = ZPolyProd([P,Q],5)
    print(P)
    print(Q)
    print(C)
    print(C*Q)
    print(C*C)
    print(C**3)
    print(C)