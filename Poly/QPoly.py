# Univariate polynomials with coefficients from the field of rationals


from Rational import Rational, rational_gcd, cast_to_rational
from Utility import poly_add, poly_mult, poly_print, poly_print_pretty
from collections import Counter

class QPoly:
    
    def __init__(self,coef):
        assert type(coef) == list
        self.coef = []
        for c in coef:
            self.coef.append(cast_to_rational(c))
        self.normalize()


    def __getitem__(self,n):
        """Make polynomial accessible by indexing"""
        return self.coef[n]


    def __setitem__(self,n,val):
        """Allow valid coefficients to be set"""    
        self.coef[n] = cast_to_rational(val)


    def __call__(self,x):
        """Evaluate the polynomial at a given point"""
        out = 0
        for pwr,co in enumerate(self.coef):
            out = out + co*(x**pwr)
        return out


    def __str__(self):
        """Print nicely in descending written form"""
        return poly_print(self)


    def __repr__(self):
        """Print nicely in descending written form"""
        return poly_print(self)
    
    
    def __hash__(self):
        return hash(str(self))


    def __len__(self):
        """Number of coefficients"""
        return len(self.coef)


    def __neg__(self):
        """Additive inverse of each coefficient"""
        L = [-c for c in self.coef]
        return QPoly(L)


    def __add__(self,poly):
        """Add a polynomial to a polynomial"""
        # If we can turn the other into a rational do that
        if type(poly) in [int,str,float,Rational]:
            poly = QPoly( [cast_to_rational(poly)] )
            L = poly_add(self.coef,poly.coef)
            return QPoly(L)
        # If its another QPoly just add them
        elif type(poly) == QPoly:
            L = poly_add(self.coef,poly.coef)
            return QPoly(L)
        # Otherwise check if the other object can have QPoly added to it
        # This is probably a bad idea in general but everything we care about
        # is commutative.
        else:
            return poly + self


    def __radd__(self,poly):
        """Polynomial addition is commutative"""
        return self + poly


    def __sub__(self,poly):
        """Subtract a polynomial from a polynomial"""
        if type(poly)  == int or type(poly) == Rational:
            poly = QPoly([poly])

        L = poly_add(self.coef,[-c for c in poly.coef])
        return QPoly(L)


    def __rsub__(self,poly):
        """Subtract a polynomial from a polynomial"""
        if type(poly)  == int or type(poly) == Rational:
            poly = QPoly([poly])

        L = poly_add(self.coef,[-c for c in poly.coef])
        return QPoly(L)


    def __mul__(self,poly):
        """Multiply a polynomial by polynomial"""
        if type(poly)  == int or type(poly) == Rational:
            poly = QPoly([poly])
            
        L = poly_mult(self.coef,poly.coef)
        return QPoly(L)


    def __rmul__(self,poly):
        """Multiply a polynomial by polynomial"""
        return self*poly


    def __pow__(self,pwr):
        """Multiply a polynomial by itself"""
        if type(pwr) != int:
            raise TypeError(f"pwr must be an integer not {type(pwr)}")
        if pwr < 0:
            raise TypeError(f"pwr must be positive")

        if pwr == 0:
            return QPoly([1])
        elif pwr == 1:
            return self
        else:
            out = self.copy()
            for i in range(pwr-1):
                out *= self
        return out


    def __eq__(self,poly):
        """Check if two polynomials have the same coefficients"""
        if len(self) == len(poly):
            if all([x == y for x,y in zip(self.coef,poly.coef)]):
                return True
        return False


    def __divmod__(self,poly):
        """Algorithm for euclidean division of polynomials"""

        # Cast integer to poly if needed
        if type(poly) == int or type(poly) == Rational:
            poly = QPoly([poly])
        assert type(poly) == QPoly, f"Could not cast {poly} to QPoly"

        # Check for division by zero    
        if poly.coef == [0]:
            raise ZeroDivisionError

        # We can only divide a longer polynomial by a shorter one
        if len(self) < len(poly):
            return QPoly([0]), self.copy()

        # Copy inputs
        P = self.coef[:]
        Q = poly.coef[:]

        # Case of a single int or rational
        if len(poly) == 1:
            return QPoly([p/Q[0] for p in P]), QPoly([0])
        # Use polynomial division algorithm, rationals are a field so this is
        # always defined
        else:
            dP = len(P)-1
            dQ = len(Q)-1
            if dP >= dQ:
                qt = [0] * dP
                while dP >= dQ:
                    d = [0]*(dP - dQ) + Q
                    mult = qt[dP - dQ] = P[-1] / d[-1]
                    d = [coeff*mult for coeff in d]
                    P = [ coeffN - coeffd for coeffN, coeffd in zip(P, d)]
                    while P[-1] == 0 and len(P) > 1:
                        if len(P) == 1:
                            break
                        P.pop()
                    dP = len(P)-1
            return QPoly(qt), QPoly(P)


    # Using __floordiv__ since there can be a remainder not because we round down
    def __floordiv__(self,poly):
        """Euclidean division of polynomials"""
        return divmod(self,poly)[0]


    def __mod__(self,poly):
        """Remainder of Euclidean division of polynomials"""
        return divmod(self,poly)[1]
    
    
    # __truediv__ isn't a closed operation so we get a QPolyQou object
    def __truediv__(self,poly):
        """Truedivision of polynomials"""
        return QPolyQuo(self,poly)


    def normalize(self):
        """Remove trailing zeroes"""
        if self.coef == []:
            self.coef = [0]
        while self.coef[-1] == 0 and len(self.coef) > 1:
            if len(self.coef) == 1:
                break
            self.coef.pop()


    def copy(self):
        """Copy the polynomial"""
        return QPoly(self.coef[:])


    def derivative(self):
        """Calculate the derivative of the polynomial"""
        co = self.coef.copy()
        for i in range(len(co)):
            co[i] *= i
        return QPoly(co[1:])


    def integral(self,C):
        """Calculate the integral of the polynomial"""
        co = self.coef.copy()
        co.insert(0,C)
        for pos,val in enumerate(co[1:],start=1):
            co[pos] = val/(pos)
        return QPoly(co)


    def evaluate(self,X):
        """Evaluate the polynomial at a given list of points"""
        assert type(X) == list
        out = [0]*len(X)
        for pwr,coef in enumerate(self.coef):
            for pos,x in enumerate(X):
                out[pos] = (out[pos] + coef*(x**pwr))
        return out


    def degree(self):
        """Degree of the polynomial"""
        return len(self)-1


    def is_monic(self):
        """Check if the polynomial is monic"""
        return self[-1] == 1 or self[-1] == -1
    
    
    def _monic_part(self):
        C = self.copy()
        C.make_monic()
        return C

    
    def make_monic(self):
        C = self[-1]
        for i in range(len(self)):
            self[i] /= C


    def _content(self):
        """Rational GCD of the coefficients, negative if leading coef is negative,
        makes the polynomial have integer coefs"""
        return abs(rational_gcd(self.coef)) * (-1 if self.coef[-1] < 0 else 1)
    

    def _primitive_part(self):
        """Smallest rational multiple of the polynomial with integer coefficients
        that have no common factors"""
        return self//self.content
    
    
    def is_primitive(self):
        """Convenience function to check if a polynomial is primitive"""
        return self.content == 1


    def make_primitive(self):
        C = self.content
        for i in range(len(self)):
            self[i] /= C


    def _pretty_name(self):
        """Formatted for LaTeX"""
        return poly_print_pretty(self)


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    content = property(_content)
    primitive_part = property(_primitive_part)
    monic_part = property(_monic_part)





############################
## Fundamental Operations ##
############################
    
# GCD is defined as primitive part
# It could also be defined as the monic part but primitive works even when one
# wishes to work with integer polynomials
def poly_gcd(P,Q):
    """GCD of two polynomials"""
    assert type(P) == QPoly
    assert type(Q) == QPoly
    
    if Q.degree() > P.degree():
        P,Q = Q,P
        
    # Check if we reached the end
    if Q == QPoly([0]):
        return P.primitive_part
    if P == QPoly([0]):
        return Q.primitive_part
    
    else:
        g = poly_gcd(P % Q, Q)
        return g.primitive_part





#######################
## Combining Objects ##
#######################

# I think these have to be here to avoid circular reference issues

class QPolySum:
    
    def __init__(self,terms):
        if type(terms) == list:
            self.terms = Counter(terms)
        elif type(terms) == QPoly:
            self.terms = Counter([terms])
        elif type(terms) == Counter:
            self.terms = terms
        else:
            raise TypeError("Not a Counter or list")
            
        self.simplify_const()


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
    

    def __str__(self):
        out = []
        
        S = []
        for i in self.terms.keys():
            S.append(i)
        S.sort(key=len,reverse=True)
        
        for i in S:
            mul = self.terms[i]
            
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
        assert type(terms) == list
        self.terms = Counter(terms)
        self.simplify_const()


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





# Better known as Rational Functions
class QPolyQuo:
    
    
    def __init__(self,N,D=QPoly([1])):
        
        if type(N) == QPoly:
            pass
        elif type(N) == list:
            N = QPoly( N )
        else:
            try:
                N = QPoly( [N] )
            except:
                raise Exception(f"Could not coerce {N} to QPoly")
        
        if type(D) == QPoly:
            pass
        elif type(D) == list:
            D = QPoly( D )
        else:
            try:
                D = QPoly( [D] )
            except:
                raise Exception(f"Could not coerce {D} to QPoly")
            
        self.N = N
        self.D = D

        self.simplify()


    def simplify(self):
        # Remove common factors
        G = poly_gcd(self.N,self.D)
        self.N //= G
        self.D //= G
        
    
    # Not really a thing for Rational Functions but still useful
    def _content(self):
        return self.N.content * self.D.content


    def _primitive_part(self):
        return QPolyQuo( self.N // self.content, self.D // self.content )
        

    def copy(self):
        return QPolyQuo(self.N.copy(),self.D.copy())


    def __str__(self):
        if str(self.N) == "0":
            return "0"
        if str(self.D) == "1":
            return str(self.N)

        if len(self.N) == 1:
            n = str(self.N)
        else:
            if self.N.content < 0:
                n = f"-({-self.N})"
            else:  
                n = f"({self.N})"

        if len(self.D) == 1:
            d = str(self.D)
        else:
            d = f"({self.D})"

        return f"{n} / {d}"


    def __call__(self,val):
        n = self.N(val)
        d = self.D(val)
        
        if d == 0:
            return float('NaN')
        else:
            return n/d


    def evaluate(self,val):
        assert type(val) == list
        return [self(v) for v in val]
    

    def inv(self):
        return QPolyQuo(self.D,self.N)


    def __mul__(self,other):
        if type(other) == QPolyQuo:
            return QPolyQuo(self.N * other.N, self.D * other.D)
        else:
            return self * QPolyQuo(other)


    def __rmul__(self,other):
        return self*other
    
    
    def __pow__(self,pwr):
        if type(pwr) != int:
            raise TypeError(f"pwr must be an integer not {type(pwr)}")

        if pwr == 0:
            return QPolyQuo([1],[1])
        else:
            out = self.copy()
            for i in range(abs(pwr)-1):
                out *= self
        
        if pwr < 0:
            return out.inv()
            
        return out
        
    
    def __truediv__(self,other):
        if type(other) == QPolyQuo:
            return self * other.inv()
        else:
            return self / QPolyQuo(other)


    def __neg__(self):
        return self*-1


    def __add__(self,other):
        if type(other) == QPolyQuo:
            return QPolyQuo(self.N*other.D + other.N*self.D, self.D*other.D)
        elif type(other) == QPoly:
            return self + QPolyQuo(other)
        else:
            return self + QPolyQuo([other])
        

    def __radd__(self,other):
        return self + other


    def __sub__(self,other):
        if type(other) == QPolyQuo:
            return self + -other
        else:
            return self - QPolyQuo(other)


    def degree(self):
        return max(self.N.degree(),self.D.degree())


    def derivative(self):
        N = (self.D * self.N.derivative()) - (self.N * self.D.derivative())
        D = self.D * self.D
        return QPolyQuo(N,D)


    def _pretty_name(self):
        if str(self.N) == "0":
            return "0"
        elif str(self.D) == "1":
            return str(self.N)
        else:
            if self.N.content < 0:
                sgn = "-"
                n = -self.N
            else:
                sgn = ""
                n = self.N
            return f"${sgn}\dfrac{{{n}}}{{{self.D}}}$"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    content = property(_content)
    primitive_part = property(_primitive_part)





if __name__ == '__main__':

    P = QPoly([1,2,3])
    Q = QPoly([6,-2])
    R = QPoly([5])
    S = QPoly([7])
    
    sum_of_polys = QPolySum([P,S,Q,P,R,R,R])
    print(sum_of_polys)
    print(sum_of_polys.cast_to_poly())
    
    print()
    
    prod_of_polys = QPolyProd([Q,S,Q,P,S])
    print(prod_of_polys)
    print(prod_of_polys.cast_to_poly())
    
    print()
    
    print((P)/(Q*P))
    
    print(sum_of_polys * 3)
    print(sum_of_polys * 0)