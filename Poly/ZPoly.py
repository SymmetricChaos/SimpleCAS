# Univariate polynomials with coefficients from the field of rationals

from Utility import poly_add, poly_mult, poly_print, poly_print_pretty


class ZPoly:
    
    def __init__(self,coef,F):
        assert type(coef) == list
        if type(F) != int:
            raise TypeError(f"Modulus must be int not {type(F)}")
        self.coef = coef
        self.normalize()


    def normalize(self):
        """Remove trailing zeroes"""
        if self.coef == []:
            self.coef = [0]
        while self.coef[-1] == 0 and len(self.coef) > 1:
            if len(self.coef) == 1:
                break
            self.coef.pop()
            
        for i in range(len(self)):
            self.coef[i] = self.coef[i] % self.F


    def __getitem__(self,n):
        """Make polynomial accessible by indexing"""
        return self.coef[n]


    def __setitem__(self,n,val):
        """Allow valid coefficients to be set"""    
        if type(val) != int:
            raise TypeError("Values must be integers")
        self.coef[n] = val


    # Need to check that this isn't too slow
    def __call__(self,x):
        """Evaluate the polynomial at a given point"""
        out = 0
        for pwr,co in enumerate(self.coef):
            out = out + co*(x**pwr)
        return out % self.F
    
    
    def evaluate(self,X):
        """Evaluate the polynomial at a given list of points"""
        assert type(X) == list
        return [self(x) for x in X]
 

    def __str__(self):
        """Print nicely in descending written form"""
        return poly_print(self)


    def __repr__(self):
        """Print nicely in descending written form"""
        return poly_print(self)
    
    
    def __hash__(self):
        return hash("CustomZPoly"+str(self))


    def __len__(self):
        """Number of coefficients"""
        return len(self.coef)


    def __neg__(self):
        """Additive inverse of each coefficient"""
        L = [-c for c in self.coef]
        return ZPoly(L)


    def __add__(self,other):
        """Addition"""
        # If we can turn the other into a rational do that
        if type(other) == int:
            other = ZPoly( [other] )
            L = poly_add(self.coef,other.coef)
            return ZPoly(L)
        
        elif type(other) == ZPoly:
            L = poly_add(self.coef,other.coef)
            return ZPoly(L)
        
        else:
            return NotImplemented


    def __radd__(self,other):
        """Addition is commutative"""
        return self + other


    def __sub__(self,other):
        """Subtraction"""
        
        if type(other) not in [int,ZPoly]:
            return NotImplemented
        
        if type(other) == int:
            other = ZPoly( [other] )
        
        L = poly_add(self.coef,[-c for c in other.coef])
        return ZPoly(L)


    def __rsub__(self,other):
        """Subtraction is NOT commutative"""
        if type(other) == int:
            other = ZPoly( [other] )

        L = poly_add(self.coef,[-c for c in other.coef])
        return ZPoly(L)


    def __mul__(self,other):
        """Multiplication"""
        
        if type(other) not in [int,ZPoly]:
            return NotImplemented
        
        if type(other) == int:
            other = ZPoly( [other] )
            
        L = poly_mult(self.coef,other.coef)
        return ZPoly(L)


    def __rmul__(self,other):
        """Multiplication is commutative"""
        return self*other


    def __pow__(self,pwr):
        """Raise to an positive integer power"""
        if type(pwr) != int:
            raise TypeError(f"pwr must be an integer not {type(pwr)}")
        if pwr < 0:
            raise TypeError(f"pwr must be non-negative")

        if pwr == 0:
            return ZPoly([1])
        elif pwr == 1:
            return self
        else:
            out = self.copy()
            for i in range(pwr-1):
                out *= self
        return out


    def __eq__(self,other):
        """Check if two polynomials have the same coefficients"""
        if type(other) != ZPoly:
            return False
        
        if self.F != other.F:
            return False
        
        if len(self) == len(other):
            if all([x == y for x,y in zip(self.coef,other.coef)]):
                return True

        return False


    def degree(self):
        """Degree of the polynomial"""
        return len(self)-1

#    def __divmod__(self,poly):
#        """Algorithm for euclidean division of polynomials"""
#
#        # Cast integer to poly if needed
#        if type(poly) in [int,Rational]:
#            poly = QPoly([poly])
#            
#        if type(poly) != QPoly:
#            raise TypeError(f"Could not cast {poly} to QPoly")
#
#        # Check for division by zero    
#        if poly.coef == [0]:
#            raise ZeroDivisionError
#
#        # We can only divide a longer polynomial by a shorter one
#        if len(self) < len(poly):
#            return QPoly([0]), self.copy()
#
#        # Copy inputs
#        P = self.coef[:]
#        Q = poly.coef[:]
#
#        # Case of a single int or rational
#        if len(poly) == 1:
#            return QPoly([p/Q[0] for p in P]), QPoly([0])
#        # Use polynomial division algorithm, rationals are a field so this is
#        # always defined
#        else:
#            dP = len(P)-1
#            dQ = len(Q)-1
#            if dP >= dQ:
#                qt = [0] * dP
#                while dP >= dQ:
#                    d = [0]*(dP - dQ) + Q
#                    mult = qt[dP - dQ] = P[-1] / d[-1]
#                    d = [coeff*mult for coeff in d]
#                    P = [ coeffN - coeffd for coeffN, coeffd in zip(P, d)]
#                    while P[-1] == 0 and len(P) > 1:
#                        if len(P) == 1:
#                            break
#                        P.pop()
#                    dP = len(P)-1
#            return QPoly(qt), QPoly(P)
#
#
#    # Using __floordiv__ since there can be a remainder, not because we round down
#    def __floordiv__(self,other):
#        """Euclidean division of polynomials"""
#        if type(other) in [int,Rational]:
#            other = QPoly([other])
#        elif type(other) == QPoly:
#            pass
#        else:
#            return NotImplemented
#        return divmod(self,other)[0]
#    
#    
#    def __rfloordiv__(self,other):
#        """Euclidean division of polynomials"""
#        if type(other) in [int,Rational]:
#            other = QPoly([other])
#        elif type(other) == QPoly:
#            pass
#        else:
#            return NotImplemented
#        return divmod(other,self)[0]
#
#
#    def __mod__(self,other):
#        """Remainder of Euclidean division of polynomials"""
#        return divmod(self,other)[1]
#    
#    
#    def __rmod__(self,other):
#        """Remainder of Euclidean division of polynomials"""
#        if type(other) in [int,Rational]:
#            other = QPoly([other])
#        return divmod(self,other)[1]
#    
#    
#    # __truediv__ isn't a closed operation so we get a QPolyQou object
#    def __truediv__(self,other):
#        """Truedivision of polynomials"""
#        if type(other) in [int,Rational]:
#            other = QPoly([other])
#        elif type(other) == QPoly:
#            pass
#        else:
#            return NotImplemented
#        return RFunc(self,other)
#    
#    
#    def __rtruediv__(self,other):
#        """Truedivision of polynomials"""
#        if type(other) in [int,Rational]:
#            other = QPoly([other])
#        elif type(other) == QPoly:
#            pass
#        else:
#            return NotImplemented
#        return RFunc(other,other)



    def copy(self):
        """Copy the polynomial"""
        return ZPoly(self.coef[:])


#    def derivative(self):
#        """Calculate the derivative of the polynomial"""
#        co = self.coef.copy()
#        for i in range(len(co)):
#            co[i] *= i
#        return ZPoly(co[1:])
#
#
#    def integral(self,C):
#        """Calculate the integral of the polynomial"""
#        co = self.coef.copy()
#        co.insert(0,C)
#        for pos,val in enumerate(co[1:],start=1):
#            co[pos] = val/(pos)
#        return ZPoly(co)
#
#
#
#    def is_monic(self):
#        """Check if the polynomial is monic"""
#        return self[-1] == 1 or self[-1] == -1
#    
#    
#    def _monic_part(self):
#        C = self.copy()
#        C.make_monic()
#        return C
#
#    
#    def make_monic(self):
#        C = self[-1]
#        for i in range(len(self)):
#            self[i] /= C
#
#
#    def _content(self):
#        """Rational GCD of the coefficients, negative if leading coef is negative,
#        makes the polynomial have integer coefs"""
#        return abs(rational_gcd(self.coef)) * (-1 if self.coef[-1] < 0 else 1)
#    
#
#    def _primitive_part(self):
#        """Smallest rational multiple of the polynomial with integer coefficients
#        that have no common factors"""
#        return self//self.content
#    
#    
#    def is_primitive(self):
#        """Convenience function to check if a polynomial is primitive"""
#        return self.content == 1
#
#
#    def make_primitive(self):
#        C = self.content
#        for i in range(len(self)):
#            self[i] /= C



    # Things that are like attributes can be access as properties
#    pretty_name = property(_pretty_name)
#    content = property(_content)
#    primitive_part = property(_primitive_part)
#    monic_part = property(_monic_part)





############################
## Fundamental Operations ##
############################
    
# GCD is defined as primitive part
# It could also be defined as the monic part but primitive works even when one
# wishes to work with integer polynomials
#def poly_gcd(P,Q):
#    """GCD of two polynomials"""
#    assert type(P) == QPoly
#    assert type(Q) == QPoly
#    
#    if Q.degree() > P.degree():
#        P,Q = Q,P
#        
#    # Check if we reached the end
#    if Q == QPoly([0]):
#        return P.primitive_part
#    if P == QPoly([0]):
#        return Q.primitive_part
#    
#    else:
#        g = poly_gcd(P % Q, Q)
#        return g.primitive_part

