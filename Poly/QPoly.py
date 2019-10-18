# Univariate polynomials with coefficients from the field of rationals


from Rational import Rational, rational_gcd, cast_to_rational
from Utility import poly_add, poly_mult, poly_print, poly_print_pretty


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
    
    
#    def __truediv__(self,poly):
#        """Truedivision of polynomials"""
#        return RFunc(self,poly)


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





if __name__ == '__main__':
    P = QPoly(["3/2",0,1,"11.6"])
    Q = QPoly([-5,1])
    print(f"P      = {P}")
    print(f"Q      = {Q}")
    print(f"P+2    = {P+2}")
    print(f"2+P    = {2+P}")
    print(f"P+Q    = {P+Q}")
    print(f"Q+P    = {Q+P}")
    print(f"P*2    = {P*2}")
    print(f"2*P    = {2*P}")
    print(f"P*Q    = {P*Q}")
    print(f"Q*P    = {Q*P}")
    print(f"P**2   = {P**2}")
    print(f"P//2   = {P//2}")
    print(f"P%2    = {P%2}")
    print(f"P//Q   = {P//Q}")
    print(f"P%Q    = {P%Q}")
    print()
    print(f"P.integral(0)   = {P.integral(0)}")
    print(f"P.derivative()  = {P.derivative()}")
    print()
    print(f"P.content        = {P.content}")
    print(f"P.primitive_part = {P.primitive_part}")
    print()
    print("P.make_primitive()")
    R = P.copy()
    R.make_primitive()
    print(R)
    print()
    print("P.make_monic()")
    S = P.copy()
    S.make_monic()
    print(S)
    