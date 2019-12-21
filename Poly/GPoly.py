# Univariate polynomials with coefficients from the ring of gaussian integers

from Quadratic import GaussInt
from GPolyPrint import gpoly_print
from Utility import poly_add, poly_mult, mod_inv, mod_div, gcd

class GPoly:
    
    def __init__(self,coef):
        if type(coef) not in [list,tuple]:
            raise TypeError("coef must be list or tuple")
        
        for i in coef:
            if type(i) != GaussInt:
                raise TypeError("all coefficients must be integers")
        

        self.coef = list(coef)
        self.normalize()


    def normalize(self):
        """Remove trailing zeroes and reduce modulo M"""
        if self.coef == []:
            self.coef = [GaussInt(0,0)]
            
        while self.coef[-1] == 0 and len(self.coef) > 1:
            if len(self.coef) == 1:
                break
            self.coef.pop()
        

    def __getitem__(self,n):
        """Make polynomial accessible by indexing"""
        return self.coef[n]


    def __setitem__(self,n,val):
        """Allow valid coefficients to be set"""    
        if type(val) != int:
            raise TypeError("Values must be integers")
        self.coef[n] = val


    # Not sure about the best method but testing suggests that "co*x**pwr" is
    # faster than "co*x**pwr % self.M" and "co*pow(x,pwr)" at least when
    # coefficients are potentially much larger than powers
    def __call__(self,x):
        """Evaluate the polynomial at a given point"""
        out = 0
        if self.M:
            for pwr,co in enumerate(self.coef):
                out = (out + co*x**pwr) % self.M
            return out
        else:
            for pwr,co in enumerate(self.coef):
                out = out + co*x**pwr
            return out


    def evaluate(self,X):
        """Evaluate the polynomial at a given list of points"""
        assert type(X) == list
        return [self(x) for x in X]
 

    def __str__(self):
        """Print nicely in descending written form"""
        return gpoly_print(self)


    def __repr__(self):
        """Print nicely in descending written form"""
        return str(self)
    
    
    def __hash__(self):
        return hash(f"CustomGPoly{self.full_name}")


    def __len__(self):
        """Number of coefficients"""
        return len(self.coef)


    def __neg__(self):
        """Additive inverse of each coefficient"""
        L = [-c for c in self.coef]
        return GPoly(L)


    def __add__(self,other):
        """Addition"""
        # If we can turn the other into a rational do that
        if type(other) == int:
            other = GPoly( [other] )
            L = poly_add(self.coef,other.coef)
            return GPoly(L)
        
        elif type(other) == GPoly:
            L = poly_add(self.coef,other.coef)
            return GPoly(L)
        
        else:
            return NotImplemented


    def __radd__(self,other):
        """Addition is commutative"""
        return self + other


    def __sub__(self,other):
        """Subtraction"""
        
        if type(other) not in [int,GPoly]:
            return NotImplemented
        
        if type(other) == int:
            other = GPoly( [other] )
        
        L = poly_add(self.coef,[-c for c in other.coef])
        return GPoly(L)


    def __rsub__(self,other):
        """Subtraction is NOT commutative"""
        if type(other) == int:
            other = GPoly( [other] )

        L = poly_add(self.coef,[-c for c in other.coef])
        return GPoly(L)


    def __mul__(self,other):
        """Multiplication"""
        
        if type(other) not in [int,GPoly]:
            return NotImplemented
        
        if type(other) == int:
            other = GPoly( [other] )
            
        L = poly_mult(self.coef,other.coef)
        return GPoly(L)


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
            return GPoly([1])
        elif pwr == 1:
            return self
        else:
            out = self.copy()
            for i in range(pwr-1):
                out *= self
        return out


    def __eq__(self,other):
        """Check if two polynomials have the same coefficients"""
        if type(other) != GPoly:
            raise TypeError(f"Cannot compare GPoly to {type(other)}")
        
        if len(self) == len(other):
            if all([x == y for x,y in zip(self.coef,other.coef)]):
                return True

        return False
                

    def degree(self):
        """Degree of the polynomial"""
        return len(self)-1


#    def __divmod__(self,other):
#        """Algorithm for euclidean division of polynomials"""
#    
#        # Cast integer to poly if needed
#        if type(other) == int:
#            other = GPoly( [other] )
#            
#        if type(other) != GPoly:
#            raise TypeError(f"Could not cast {other} to GPoly")
#
#        # Check for division by zero    
#        if other.coef == [0]:
#            raise ZeroDivisionError
#
#        # We can only divide a longer polynomial by a shorter one
#        if len(self) < len(other):
#            return GPoly([0]), self.copy()
#
#        # Copy inputs
#        P = self.coef[:]
#        Q = other.coef[:]
#
#        # Case of division by a single int
#        if len(other) == 1:
#            if self.M:
#                return GPoly( [mod_div(p,Q[0]) for p in P]), GPoly( [0])
#            else:
#                return GPoly( [p//Q[0] for p in P]), GPoly( [p%Q[0] for p in P])
#        
#        # Polynomial division
#
#        dP = len(P)-1
#        dQ = len(Q)-1
#        qt = [0]*dP
#        while dP >= dQ:
#            
#            d = [0]*(dP - dQ) + Q
#            mult = qt[dP - dQ] = P[-1] // d[-1]
#
#            if P[-1] % d[-1] != 0:
#                raise Exception(f"Euclidean division of {self} by {other} is not defined")
#
#            d = [co*mult for co in d]
#            P = [ (coeffP - coeffd)  for coeffP, coeffd in zip(P, d)]
#
#            while P[-1] == 0 and len(P) > 1:
#                if len(P) == 1:
#                    break
#                P.pop()
#            dP = len(P)-1
#
#        rm = [i for i in P]
#
#        return GPoly( qt ), GPoly( rm )
#
#
#    # Using __floordiv__ since there can be a remainder, not because we round down
#    def __floordiv__(self,other):
#        """Euclidean division of polynomials"""
#        if type(other) == int:
#            other = GPoly([other])
#        elif type(other) == GPoly:
#            pass
#        else:
#            return NotImplemented
#        return divmod(self,other)[0]
#    
#    
#    def __rfloordiv__(self,other):
#        """Euclidean division of polynomials"""
#        return other // self
#    
#    
#    def __mod__(self,other):
#        """Remainder of Euclidean division of polynomials"""
#        if type(other) == int:
#            other = GPoly([other])
#        elif type(other) == GPoly:
#            pass
#        else:
#            return NotImplemented
#        return divmod(self,other)[1]
#    
#    
#    def __rmod__(self,other):
#        """Remainder of Euclidean division of polynomials"""
#        other % self
    
    
    def copy(self):
        """Copy the polynomial"""
        return GPoly(self.coef[:])



    def is_monic(self):
        """Check if the polynomial is monic"""
        return self[-1] == 1 or self[-1] == -1


#    def _pretty_name(self):
#        """Formatted for LaTeX"""
#        if self.M:
#            return f"{zpoly_print_pretty(self)} (mod {self.M})"
#        else:
#            return f"{zpoly_print_pretty(self)}"


    # Things that are like attributes can be access as properties
#    pretty_name = property(_pretty_name)
#    content = property(_content)
#    primitive_part = property(_primitive_part)





#def zpoly_gcd(P,Q,part="monic"):
#    """GCD of two polynomials"""
#    assert type(P) == GPoly
#    assert type(Q) == GPoly
#    assert P.M == Q.M
#    
#    if Q.degree() > P.degree():
#        P,Q = Q,P
#    
#    if part == "monic":
#        if Q == GPoly([0],P.M):
#            return P.monic_part
#        if P == GPoly([0],P.M):
#            return Q.monic_part
#        
#        else:
#            g = zpoly_gcd(P % Q, Q)
#            return g.monic_part
#    
#    if part == "primitive":
#        if Q == GPoly([0],P.M):
#            return P.primitive_part
#        if P == GPoly([0],P.M):
#            return Q.primitive_part
#        
#        else:
#            g = zpoly_gcd(P % Q, Q)
#            return g.primitive_part





if __name__ == '__main__':
    
    
    A = GaussInt(1,1)
    B = GaussInt(6,0)
    C = GaussInt(0,2)
    D = GaussInt(3,2)
    
    P = GPoly([A,B,C,D])
    
    
    print(P)
    
    Q = P-P
    print(Q.coef)
    print(Q)
    
    
#    print("Division and Remainder with a modulus")
#    M = 17
#    P = GPoly( [1,4,7], M )
#    Q = GPoly( [8,1], M)
#    print(f"P = {P.full_name}")
#    print(f"Q = {Q.full_name}")
#    print(f"P//Q = {P//Q}")
#    print(f"P%Q  = {P%Q}")
#    print(f"Check the the process reverses: {(P//Q)*Q+(P%Q) == P}")
#    
#    print(f"Monic part of P: {P.monic_part}")
#    
#    
#    print("\n\nDivision and Remainder without a modulus")
#    P = GPoly( [1,4,7] )
#    Q = GPoly( [8,1] )
#
#    print(f"P = {P.full_name}")
#    print(f"Q = {Q.full_name}")
#    print(f"P//Q = {P//Q}")
#    print(f"P%Q  = {P%Q}")
#    print("Check the the process reverses")
#    print((P//Q)*Q+(P%Q) == P)
#
#    print(f"Primitive part of P: {P.primitive_part}")
#    
#    
#    print("\n\nzpoly_gcd")
#    A = GPoly([1,1,0,1,0,1,1],2)
#    B = GPoly([1,1,0,1,1],2)
#    print(A)
#    print(B)
#    print(zpoly_gcd(A,B))

    
