# Univariate polynomials with coefficients from the field of rationals

from Utility import poly_add, poly_mult, mod_inv, mod_div, gcd
from Poly.ZPolyPrint import zpoly_print, zpoly_print_pretty

class ZPoly:
    
    def __init__(self,coef,M=None):
        if type(coef) not in [list,tuple]:
            raise TypeError("coef must be list or tuple")
        
        for i in coef:
            if type(i) != int:
                raise TypeError("all coefficients must be integers")
        
        if M == None:
            pass
        else:
            if type(M) != int:
                raise TypeError(f"Modulus must be int or None not {type(M)}")
        
        self.coef = list(coef)
        self.M = M
        self.normalize()


    def normalize(self):
        """Remove trailing zeroes and reduce modulo M"""
        if self.coef == []:
            self.coef = [0]

        if self.M:    
            self.coef = [c % self.M for c in self.coef]
        else:
            pass
            
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
        if self.M:
            self.coef[n] = val % self.M
        else:
            self.coef[n] = val


    # Not sure about the best method but testing suggests that "co*x**pwr" is
    # faster than "co*x**pwr % self.M" and "co*pow(x,pwr,self.M)" at least when
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
        return zpoly_print(self)


    def __repr__(self):
        """Print nicely in descending written form"""
        return zpoly_print(self)
    
    
    def _full_name(self):
        """Print nicely in descending written form with modulus"""
        if self.M:
            return f"{zpoly_print(self)} (mod {self.M})"
        else:
            return f"{zpoly_print(self)}"
    
    
    def __hash__(self):
        return hash(f"CustomZPoly{self.full_name}")


    def __len__(self):
        """Number of coefficients"""
        return len(self.coef)


    def __neg__(self):
        """Additive inverse of each coefficient"""
        L = [-c for c in self.coef]
        return ZPoly(L,self.M)


    def __add__(self,other):
        """Addition"""
        # If we can turn the other into a rational do that
        if type(other) == int:
            other = ZPoly( [other],self.M )
            L = poly_add(self.coef,other.coef)
            return ZPoly(L,self.M)
        
        elif type(other) == ZPoly:
            L = poly_add(self.coef,other.coef)
            return ZPoly(L,self.M)
        
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
            other = ZPoly( [other],self.M )
        
        L = poly_add(self.coef,[-c for c in other.coef])
        return ZPoly(L,self.M)


    def __rsub__(self,other):
        """Subtraction is NOT commutative"""
        if type(other) == int:
            other = ZPoly( [other],self.M )

        L = poly_add(self.coef,[-c for c in other.coef])
        return ZPoly(L,self.M)


    def __mul__(self,other):
        """Multiplication"""
        
        if type(other) not in [int,ZPoly]:
            return NotImplemented
        
        if type(other) == int:
            other = ZPoly( [other],self.M )
            
        L = poly_mult(self.coef,other.coef)
        return ZPoly(L,self.M)


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
            return ZPoly([1],self.M)
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
            raise TypeError("Cannot compare ZPoly to {type(other)}")
        
        if self.M != other.M:
            raise ValueError("Can only compare ZPoly with identical modulus")

        if len(self) == len(other):
            if all([x == y for x,y in zip(self.coef,other.coef)]):
                return True

        return False
    
    
    def __lt__(self,other):
        """Strict less than relation"""
        # See if the inputs are identical.
        # Since __eq__ does error checking we don't need to repeat it
        if self == other:
            return False


        if len(self) < len(other):
            return True
        
        elif len(self) > len(other):
            return False
            
        else:
            X = reversed(self.coef)
            Y = reversed(other.coef)
            for x,y in zip(X,Y):
                if x < y:
                    return True
                if x > y:
                    return False
            

    def degree(self):
        """Degree of the polynomial"""
        return len(self)-1


    def __divmod__(self,other):
        """Algorithm for euclidean division of polynomials"""
    
        # Cast integer to poly if needed
        if type(other) == int:
            other = ZPoly( [other], self.M )
            
        if type(other) != ZPoly:
            raise TypeError(f"Could not cast {other} to ZPoly")

        # Check for division by zero    
        if other.coef == [0]:
            raise ZeroDivisionError

        # We can only divide a longer polynomial by a shorter one
        if len(self) < len(other):
            return ZPoly([0],self.M), self.copy()

        # Copy inputs
        P = self.coef[:]
        Q = other.coef[:]

        # Case of division by a single int
        if len(other) == 1:
            if self.M:
                return ZPoly( [mod_div(p,Q[0],self.M) for p in P], self.M), ZPoly( [0], self.M)
            else:
                return ZPoly( [p//Q[0] for p in P], self.M), ZPoly( [p%Q[0] for p in P], self.M)
        
        if self.M:
            # Polynomial division if a modulus is given
            dP = len(P)-1
            dQ = len(Q)-1
            qt = [0]*dP
            while dP >= dQ:
                
                d = [0]*(dP - dQ) + Q
                mult = qt[dP - dQ] = P[-1] * mod_inv(d[-1],self.M)
                
                d = [co*mult for co in d]
                P = [ (coeffP - coeffd) % self.M for coeffP, coeffd in zip(P, d)]
                
                while P[-1] == 0 and len(P) > 1:
                    if len(P) == 1:
                        break
                    P.pop()
                    
                dP = len(P)-1
                rm = [i % self.M for i in P]

            return ZPoly( qt, self.M), ZPoly( rm, self.M)
        
        else:
            # Polynomial division if a modulus is NOT given

            dP = len(P)-1
            dQ = len(Q)-1
            qt = [0]*dP
            while dP >= dQ:
                
                d = [0]*(dP - dQ) + Q
                mult = qt[dP - dQ] = P[-1] // d[-1]

                if P[-1] % d[-1] != 0:
                    raise Exception(f"Euclidean division of {self} by {other} is not defined")

                d = [co*mult for co in d]
                P = [ (coeffP - coeffd)  for coeffP, coeffd in zip(P, d)]

                while P[-1] == 0 and len(P) > 1:
                    if len(P) == 1:
                        break
                    P.pop()
                dP = len(P)-1

            rm = [i for i in P]

            return ZPoly( qt ), ZPoly( rm )


    # Using __floordiv__ since there can be a remainder, not because we round down
    def __floordiv__(self,other):
        """Euclidean division of polynomials"""
        if type(other) == int:
            other = ZPoly([other],self.M)
        elif type(other) == ZPoly:
            pass
        else:
            return NotImplemented
        return divmod(self,other)[0]
    
    
    def __rfloordiv__(self,other):
        """Euclidean division of polynomials"""
        return other // self
    
    
    def __mod__(self,other):
        """Remainder of Euclidean division of polynomials"""
        if type(other) == int:
            other = ZPoly([other],self.M)
        elif type(other) == ZPoly:
            pass
        else:
            return NotImplemented
        return divmod(self,other)[1]
    
    
    def __rmod__(self,other):
        """Remainder of Euclidean division of polynomials"""
        other % self
    
    
    def copy(self):
        """Copy the polynomial"""
        return ZPoly(self.coef[:],self.M)


    def derivative(self):
        """Calculate the formal derivative of the polynomial"""
        co = self.coef.copy()
        for i in range(len(co)):
            co[i] *= i
        return ZPoly(co[1:],self.M)


    def _content(self):
        return gcd(self.coef)
    
    
    def _primitive_part(self):
        co = [c//self.content for c in self.coef]
        return ZPoly( co,self.M)
    

    def is_monic(self):
        """Check if the polynomial is monic"""
        return self[-1] == 1 or self[-1] == -1
    
    
    def _monic_part(self):
        C = self.copy()
        C.make_monic()
        return C

    
    def make_monic(self):
        if self.M == None:
            raise ValueError("Cannot produce a monic polynomial without modulus, try .primitive_part instead")
        C = self[-1]
        for i in range(len(self)):
            self[i] = mod_div(self[i],C,self.M)


    def _pretty_name(self):
        """Formatted for LaTeX"""
        if self.M:
            return f"{zpoly_print_pretty(self)} (mod {self.M})"
        else:
            return f"{zpoly_print_pretty(self)}"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    full_name = property(_full_name)
    monic_part = property(_monic_part)
    content = property(_content)
    primitive_part = property(_primitive_part)


def zpoly_gcd(P,Q):
    """GCD of two polynomials"""
    assert type(P) == ZPoly
    assert type(Q) == ZPoly
    assert P.M == Q.M
    
    if Q.degree() > P.degree():
        P,Q = Q,P
        
    # Check if we reached the end
    if Q == ZPoly([0],P.M):
        return P.monic_part
    if P == ZPoly([0],P.M):
        return Q.monic_part
    
    else:
        g = zpoly_gcd(P % Q, Q)
        return g.monic_part





if __name__ == '__main__':
    
    print("Division and Remainder with a modulus")
    M = 17
    P = ZPoly( [1,4,7], M )
    Q = ZPoly( [8,1], M)
    print(f"P = {P.full_name}")
    print(f"Q = {Q.full_name}")
    print(f"P//Q = {P//Q}")
    print(f"P%Q  = {P%Q}")
    print(f"Check the the process reverses: {(P//Q)*Q+(P%Q) == P}")
    
    print(f"Monic part of P: {P.monic_part}")
    
    
    print("\n\nDivision and Remainder without a modulus")
    P = ZPoly( [1,4,7] )
    Q = ZPoly( [8,1] )

    print(f"P = {P.full_name}")
    print(f"Q = {Q.full_name}")
    print(f"P//Q = {P//Q}")
    print(f"P%Q  = {P%Q}")
    print("Check the the process reverses")
    print((P//Q)*Q+(P%Q) == P)

    print(f"Primitive part of P: {P.primitive_part}")
    
    
    print("\n\nzpoly_gcd")
    A = ZPoly([1,1,0,1,0,1,1],2)
    B = ZPoly([1,1,0,1,1],2)
    print(A)
    print(B)
    print(zpoly_gcd(A,B))

    
