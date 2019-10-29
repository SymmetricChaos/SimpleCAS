from collections import Counter
from Poly import QPoly



class QPolySum:
    
    def __init__(self,terms):
        if type(terms) == list:
            for i in terms:
                assert type(i) in [QPoly,QPolyProd]
            self.terms = Counter(terms)
            
        elif type(terms) == QPoly:
            self.terms = Counter([terms])
            
        elif type(terms) == QPolyProd:
            self.terms = Counter([terms])
            
        elif type(terms) == Counter:
            self.terms = terms
            
        else:
            raise TypeError(f"Couldn't use type {type(terms)}")
            
        self.simplify_const()
                
        del self.terms[0]


    def simplify_const(self):
        """Deal with constant terms"""
        const = 0
        remv = []
        for i in self.terms.items():
            if len(i[0]) == 1:
                const += i[0]*i[1]
                remv.append(i[0])
        
        for t in remv:
            del self.terms[t]
        
        self.terms[const] = 1


    def cast_to_poly(self):
        """Add everything together as a QPoly"""
        out = QPoly([0])
        for val,mul in self.terms.items():
            out += val*mul
        return out
    
    
    def copy(self):
        """Copy the sum"""
        return QPolySum(self.terms.copy())
    
    
    def __add__(self,other):
        A = self.terms.copy()
        A.update(other.terms)
        return QPolySum(A)
    
    
    def __mul__(self,other):
        assert type(other) == int
        
        if other == 0:
            return QPolySum([QPoly([0])])
        
        A = self.terms.copy()
        B = A.copy()
        for i in range(other-1):
            A.update(B)
        return QPolySum(A)
    
    
    def __len__(self):
        out = 0
        for i in self.terms:
            out += len(i)
        return out
    
    
    def __hash__(self):
        return hash("CustomPolySum"+str(self))
    

    def __str__(self):
        out = []
        
        S = []
        for i in self.terms.keys():
            S.append(i)
        S.sort(key=len,reverse=True)
        
        for i in S:
            mul = self.terms[i]
            
            if type(i) == QPoly:
            
                if mul == 1:
                    if len(i) == 1:
                        out.append(str(i))
                    else:
                        out.append(f"({i})")
                else:
                    if len(i) == 1:
                        out.append(f"{mul}*{i}")
                    else:
                        out.append(f"{mul}({i})")
                        
            else:
                if mul == 1:
                    out.append(f"{i}")
                else:
                    if len(i) == 1:
                        out.append(f"{mul}*{i}")
                    else:
                        out.append(f"{mul}({i})")
        
        return " + ".join(out)


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
                    out.append(f"{pwr}*{i.pretty_name}")
                else:
                    out.append(f"{pwr}({i.pretty_name})")
        
        J = "\;+\;".join(out)
        J = J.replace("$","")
        return f"${J}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)





class QPolyProd:
    
    def __init__(self,terms):
        if type(terms) == list:
            for i in terms:
                assert type(i) in [QPoly,QPolySum]
            self.terms = Counter(terms)
            
        elif type(terms) == QPoly:
            self.terms = Counter([terms])
            
        elif type(terms) == QPolySum:
            self.terms = Counter([terms])
            
        elif type(terms) == Counter:
            self.terms = terms
            
        else:
            raise TypeError(f"Couldn't use type {type(terms)}")
            
        self.simplify_const()
                
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
        """Multiply everything together as a QPoly"""
        out = QPoly([1])
        for val,pwr in self.terms.items():
            out *= val**pwr
        return out


    def copy(self):
        return QPolyProd(self.terms.copy())


    def __len__(self):
        out = 0
        for i in self.terms:
            out += len(i)
        return out


    def __mul__(self,other):
        
        A = self.terms.copy()
        
        if type(other) == int:
            return self * QPoly([other])

        if type(other) == QPoly:
            A.update([other])

        elif type(other) == QPolyProd:
            A.update(other.terms)

        else:
            return NotImplemented
        
        return QPolyProd(A)
    
    
    def __rmul__(self,other):
        return self*other


    def __pow__(self,other):
        assert type(other) == int
        
        if other == 0:
            return QPolySum([QPoly([0])])
        
        A = self.terms.copy()
        B = A.copy()
        for i in range(other-1):
            A.update(B)
        return QPolyProd(A)
    

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


    def __hash__(self):
        return hash("CustomPolyProd"+str(self))


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
        
        J = "".join(out)
        J = J.replace("$","")
        return f"${J}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)





if __name__ == '__main__':

    P = QPoly([1,2,3])
    Q = QPoly([6,-2])
    R = QPoly([5])
    S = QPoly([7])
    
    sum_of_polys = QPolySum([P,S,Q,P,R,R,R])
    print(sum_of_polys)
    print(sum_of_polys.cast_to_poly())
    print()
    
    prod_of_polys1 = QPolyProd([P,S,R])
    prod_of_polys2 = QPolyProd([P,S])
    print(prod_of_polys1)
    print(prod_of_polys1.cast_to_poly())
    
    T = QPolySum([prod_of_polys1,prod_of_polys2])
    print()
    print(T)
    
    U = QPolyProd([])
    U = U * P * Q * R * P * R
    print(P)
    print(Q)
    print(U)
    
    print(U**2)