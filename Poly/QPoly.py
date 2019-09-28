# Univariate polynomials with coefficients from the field of rationals


## TODO: Polynomial GCD

from Rational import Rational, rational_gcd, coerce_to_rational
from Utility import poly_add, poly_mult, poly_print, poly_print_pretty

class QPoly:
    
    def __init__(self,coef):
        assert type(coef) == list
        self.coef = []
        for c in coef:
            self.coef.append(coerce_to_rational(c))
        self.normalize()


    def __getitem__(self,n):
        """Make polynomial accessible by indexing"""
        return self.coef[n]


    def __setitem__(self,n,val):
        """Allow valid coefficients to be set"""    
        self.coef[n] = coerce_to_rational(val)


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


    def __len__(self):
        """Number of coefficients"""
        return len(self.coef)


    def __neg__(self):
        """Additive inverse of each coefficient"""
        L = [-c for c in self.coef]
        return QPoly(L)


    def __add__(self,poly):
        """Add a polynomial to a polynomial"""
        if type(poly)  == int or type(poly) == Rational:
            poly = QPoly([poly])

        L = poly_add(self.coef,poly.coef)
        return QPoly(L)


    def __radd__(self,poly):
        """Polynomial addition is commutative"""
        return self + poly


    def __sub__(self,poly):
        """Subtract a polynomial from a polynomial"""
        if type(poly)  == int or type(poly) == Rational:
            poly = QPoly([poly])

        L = poly_add(self.coef,[-c for c in poly.coef])
        return QPoly(L,self)


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
        if pwr == 0:
            return QPoly([1])
        if pwr == 1:
            return self
        else:
            assert type(pwr) == int, f"{pwr} is not an integer"
            assert type(pwr) > 0, f"{pwr} is negative"
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
        assert type(poly) == QPoly, f"Could not cast {poly} to rational polynomial"

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


    # Still using floor division since there can be a remainder
    def __floordiv__(self,poly):
        """Integer division of polynomials"""
        a,b = divmod(self,poly)
        return a


    def __mod__(self,poly):
        """Remainder of integer division of polynomials"""
        a,b = divmod(self,poly)
        return b
    
    
#    def __truediv__(self,poly):
#        """Truedivision of polynomials"""
#        return RationalFunc(self,poly)


    def normalize(self):
        """Remove trailing zeroes"""
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
        co.insert(C,0)
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
    
    
    def content(self):
        """Rational GCD of the coefficients, negative if leading coef is negative,
        makes the polynomial have integer coefs"""
        return abs(rational_gcd(self.coef)) * (-1 if self.coef[-1] < 0 else 1)
    

    def primitive(self):
        """Smallest rational multiple of the polynomial with integer coefficients
        that have no common factors"""
        return self//self.content()
    
    
    def is_primitive(self):
        """Convenience function to check if a polynomial is primitive"""
        return self.content == 1


    def pretty_name(self):
        """Formatted for LaTeX"""
        return poly_print_pretty(self)






if __name__ == '__main__':
    P = QPoly([0,2,0,-6,-2,0,0])
    P[1] /= 3
    print(f"P    = {P}")
    print(f"P(2) = {P(2)}")
    print(f"P//3 = {P//3}")
    print(P//QPoly([0,1,2]))
    print(P)
    
    Q = QPoly([-5,1,-3])
    print(f"\nQ          = {Q}")
    print(f"integral   = {Q.integral(0)}")
    print(f"derivative = {Q.derivative()}")
    
    R = QPoly([0,2,0,-6,-2])
    R //= 3
    R[1] = Rational(3,5)
    print(f"\nR            = {R}")
    print(f"content(R)   = {R.content()}")
    print(f"primitive(R) = {R.primitive()}")
    
    S = QPoly([0,"3/2",0,"4/3","11.76"])
    print(S)