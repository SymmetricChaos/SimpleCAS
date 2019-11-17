from Poly import ZPoly
from collections import Counter
from Utility import sort_by_nth, gcd
import re


# Needs to factor out gcd of terms
class ZPolySum:
    
    def __init__(self,terms,M=None):
        if type(terms) == list:
            self.terms = Counter(terms)
            
        elif type(terms) == ZPoly:
            self.terms = Counter([terms])
            
        elif type(terms) == Counter:
            self.terms = terms
            
        else:
            raise TypeError(f"Couldn't use type {type(terms)}")
        
        
        self.simplify_mult()
        self.simplify_const()
        self.M = M


    def simplify_const(self):
        """Deal with constant terms"""
        const = 1
        remv = []
        for i in self.terms.items():
            if len(i[0]) == 1:
                const += i[0]*i[1]
                remv.append(i[0])
        
        for t in remv:
            del self.terms[t]
            
        self.terms[const] = 1

        del self.terms[1]


    def simplify_mult(self):
        """Remove common factor of coefficients"""
        remv = []
        newc = []
        for i in self.terms.items():
            g = gcd(i[0].coef)
            if g != 1 and g != 0:
                remv.append(i[0])
                newc.append( Counter( {i[0]//g:g*i[1]} ) )

        for t in remv:
            del self.terms[t]


        for n in newc:
            self.terms += n


    def cast_to_poly(self):
        """Add everything together as a ZPoly"""
        out = ZPoly([0],self.M)
        for val,mul in self.terms.items():
            out += mul*val
        return out


    def __add__(self,other):
        
        A = self.terms.copy()
        
        if type(other) == int:
            return self + ZPoly([other],self.M)

        if type(other) == ZPoly:
            if other.M == self.M:
                A.update([other])
            else:
                raise ValueError("Values of M do not match")

        elif type(other) == ZPolySum:
            A.update(other.terms)

        else:
            return NotImplemented
        
        return ZPolySum(A,self.M)
    
    
    def __radd__(self,other):
        return self+other


    def __len__(self):
        out = 0
        for i in self.terms:
            out += len(i)
        return out


    def __str__(self):
        out = []
        
        S = []
        for i in self.terms.items():
            S.append(i)
        S = sort_by_nth(S,0)
        
        
        for t,mul in S:
            
            if mul == 1:
                # If there aremultiple terms and the scalar is 1 ignore it
                if len(self) > 1 and str(t) == "1":
                    continue
                # Scalar terms in every other case
                elif len(t) == 1:
                    out.append(str(t))
                # Non-scalar terms
                else:
                    out.append(f"({t})")
            # Non-scalar terns raised to a power
            else:
                out.append(f"{mul}({t})")
        
        return " + ".join(out)


    def _full_name(self):
        if self.M != None:
            return f"{self} [mod {self.M}]"
        else:
            return str(self)
        

    def __hash__(self):
        return hash(f"CustomZPolySum{self.full_name}")


    def _pretty_name(self):
        out = []
        
        S = []
        for i in self.terms.items():
            S.append(i)
        # Sort S by the number of terms in each polynomial
        S = sort_by_nth(S,0,len)
        
        for t,mul in S:
            if mul == 1:
                # If there aremultiple terms and the scalar is 1 ignore it
                if len(self) > 1 and str(t) == "1":
                    continue
                # Scalar terms in every other case
                elif len(t) == 1:
                    out.append(str(t))
                # Non-scalar terms
                else:
                    out.append(f"({t.pretty_name})")
            # Non-scalar terns raised to a power
            else:
                out.append(f"{mul}({t.pretty_name})")
        
        
        # Join everything
        out = " + ".join(out)
        # Remove the modulo terms
        out = re.sub(" \(mod \d*\)","",out)
        # Remove $ signs
        out = out.replace("$","")
        if self.M:    
            return f"${out}$ [mod {self.M}]"
        else:
            return f"${out}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    full_name = property(_full_name)





class ZPolyProd:
    
    def __init__(self,terms,M=None):
        if type(terms) == list:
            self.terms = Counter(terms)
            
        elif type(terms) == ZPoly:
            self.terms = Counter([terms])
            
        elif type(terms) == Counter:
            self.terms = terms
            
        else:
            raise TypeError(f"Couldn't use type {type(terms)}")
            
        self.simplify_const()
        self.M = M


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

        del self.terms[1]
        

    def cast_to_poly(self):
        """Multiply everything together as a ZPoly"""
        out = ZPoly([1],self.M)
        for val,pwr in self.terms.items():
            out *= val**pwr
        return out


    def __mul__(self,other):
        
        A = self.terms.copy()
        
        if type(other) == int:
            return self * ZPoly([other],self.M)

        if type(other) == ZPoly:
            if other.M == self.M:
                A.update([other])
            else:
                raise ValueError("Values of M do not match")

        elif type(other) == ZPolyProd:
            A.update(other.terms)

        else:
            return NotImplemented
        
        return ZPolyProd(A,self.M)
    
    
    def __rmul__(self,other):
        return self*other

    
    def __pow__(self,other):
        if type(other) != int:
            raise TypeError("Power of ZPolyProd must be an integer")
        if other < 0:
            raise TypeError("Power of ZPolyProd must be non-negative")
        
        if other == 0:
            return ZPolyProd( ZPoly([1],self.M), self.M)
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
        for i in self.terms.items():
            S.append(i)
        S = sort_by_nth(S,0)
        
        
        for t,pwr in S:
            
            if pwr == 1:
                # If there aremultiple terms and the scalar is 1 ignore it
                if len(self) > 1 and str(t) == "1":
                    continue
                # Scalar terms in every other case
                elif len(t) == 1:
                    out.append(str(t))
                # Non-scalar terms
                else:
                    out.append(f"({t})")
            # Non-scalar terns raised to a power
            else:
                out.append(f"({t})^{pwr}")
        
        return "".join(out)


    def _full_name(self):
        if self.M != None:
            return f"{self} [mod {self.M}]"
        else:
            return str(self)
        

    def __hash__(self):
        return hash(f"CustomZPolyProd{self.full_name}")


    def _pretty_name(self):
        out = []
        
        S = []
        for i in self.terms.items():
            S.append(i)
        # Sort S by the number of terms in each polynomial
        S = sort_by_nth(S,0,len)
        
        for t,pwr in S:
            if pwr == 1:
                # If there aremultiple terms and the scalar is 1 ignore it
                if len(self) > 1 and str(t) == "1":
                    continue
                # Scalar terms in every other case
                elif len(t) == 1:
                    out.append(str(t))
                # Non-scalar terms
                else:
                    out.append(f"({t.pretty_name})")
            # Non-scalar terns raised to a power
            else:
                out.append(f"({t.pretty_name})^{{{pwr}}}")
        
        
        # Join everything
        out = "".join(out)
        # Remove the modulo terms
        out = re.sub(" \(mod \d*\)","",out)
        # Remove $ signs
        out = out.replace("$","")
        if self.M:    
            return f"${out}$ [mod {self.M}]"
        else:
            return f"${out}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    full_name = property(_full_name)









if __name__ == '__main__':
    P = ZPoly( [1,2,3], 19)
    Q = ZPoly( [2,4], 19)
    C = ZPolyProd([P,Q],19)
    print(P)
    print(Q)
    print(C)
    print(C*Q)
    print(C*C)
    print(C**3)
    print(C*2)
    
    D = 2*C*Q
    print(D)
    print(D**0)
    print(D.pretty_name)
    print(D.full_name)
    
    

    P = ZPoly([1,2,3],5)
    Q = ZPoly([1,4,1],5) 
    R = ZPoly([4,1],5) 
    S = ZPoly([3],5)
    T = ZPoly([0,0,2],5)
    U = ZPoly([0,1,0,0,0,1],5)
    
    print("\n\nProducts")
    C = ZPolyProd([P,Q,R,S,T,U],5)
    C = C * P * S * T * T
    print(C.full_name)
    
    print("\n\nSums")
    C = ZPolySum([P,Q,R,S,T,U],5)
    C = C + P + S + T + T + P
    print(C.full_name)
