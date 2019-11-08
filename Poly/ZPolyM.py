# Univariate polynomials with integer coefficients reduced modulo some integer


from Utility import poly_add, poly_mult, mod_inv, mod_div, gcd

class ZPolyM:
    
    def __init__(self,coef,M):
        try:
            iter(coef)
        except:
            raise TypeError("coef must be iterable")
        
        for i in coef:
            if type(i) != int:
                raise TypeError("all coefficients must be integers")
        
        if type(M) != int:
            raise TypeError(f"Modulus must be int not {type(M)}")
        self.coef = coef
        self.M = M
        self.normalize()


    def normalize(self):
        """Remove trailing zeroes and reduce modulo F"""
        if self.coef == []:
            self.coef = [0]

        self.coef = [c % self.M for c in self.coef]
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
        self.coef[n] = val % self.M


    # Not sure about the best method but testing suggests that "co*x**pwr" is
    # faster than "co*x**pwr % self.M" and "co*pow(x,pwr,self.M)" at least when
    # coefficients are potentially much larger than powers
    def __call__(self,x):
        """Evaluate the polynomial at a given point"""
        out = 0
        for pwr,co in enumerate(self.coef):
            out = out + co*x**pwr
        return out % self.M

    
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
        return f"{zpoly_print(self)} (mod {self.M})"
    
    
    def __hash__(self):
        return hash(f"CustomZPolyM{self.full_name}")


    def __len__(self):
        """Number of coefficients"""
        return len(self.coef)


    def __neg__(self):
        """Additive inverse of each coefficient"""
        L = [-c for c in self.coef]
        return ZPolyM(L,self.M)


    def __add__(self,other):
        """Addition"""
        # If we can turn the other into a rational do that
        if type(other) == int:
            other = ZPolyM( [other],self.M )
            L = poly_add(self.coef,other.coef)
            return ZPolyM(L,self.M)
        
        elif type(other) == ZPolyM:
            L = poly_add(self.coef,other.coef)
            return ZPolyM(L,self.M)
        
        else:
            return NotImplemented


    def __radd__(self,other):
        """Addition is commutative"""
        return self + other


    def __sub__(self,other):
        """Subtraction"""
        
        if type(other) not in [int,ZPolyM]:
            return NotImplemented
        
        if type(other) == int:
            other = ZPolyM( [other],self.M )
        
        L = poly_add(self.coef,[-c for c in other.coef])
        return ZPolyM(L,self.M)


    def __rsub__(self,other):
        """Subtraction is NOT commutative"""
        if type(other) == int:
            other = ZPolyM( [other],self.M )

        L = poly_add(self.coef,[-c for c in other.coef])
        return ZPolyM(L,self.M)


    def __mul__(self,other):
        """Multiplication"""
        
        if type(other) not in [int,ZPolyM]:
            return NotImplemented
        
        if type(other) == int:
            other = ZPolyM( [other],self.M )
            
        L = poly_mult(self.coef,other.coef)
        return ZPolyM(L,self.M)


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
            return ZPolyM([1],self.M)
        elif pwr == 1:
            return self
        else:
            out = self.copy()
            for i in range(pwr-1):
                out *= self
        return out


    def __eq__(self,other):
        """Check if two polynomials have the same coefficients"""
        if type(other) != ZPolyM:
            raise TypeError("Cannot compare ZPolyM to {type(other)}")
        
        if self.M != other.F:
            raise ValueError("Can only compare ZPolyM with identical F")

        
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
            other = ZPolyM( [other], self.M )
            
        if type(other) != ZPolyM:
            raise TypeError(f"Could not cast {other} to ZPolyM")

        # Check for division by zero    
        if other.coef == [0]:
            raise ZeroDivisionError

        # We can only divide a longer polynomial by a shorter one
        if len(self) < len(other):
            return ZPolyM([0],self.M), self.copy()

        # Copy inputs
        P = self.coef[:]
        Q = other.coef[:]

        # Case of a single int or rational
        if len(other) == 1:
            return ZPolyM( [mod_div(p,Q[0],self.M) for p in P], self.M), ZPolyM( [0], self.M)
        
        # Use polynomial division algorithm this may not be defined if F is not
        # a prime power.
        else:
            dP = len(P)-1
            dQ = len(Q)-1
            if dP >= dQ:
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
            else:
                qt = [0]
                rm = [i % self.M for i in P]

        return ZPolyM( qt, self.M), ZPolyM( rm, self.M)


    # Using __floordiv__ since there can be a remainder, not because we round down
    def __floordiv__(self,other):
        """Euclidean division of polynomials"""
        if type(other) == int:
            other = ZPolyM([other],self.M)
        elif type(other) == ZPolyM:
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
            other = ZPolyM([other],self.M)
        elif type(other) == ZPolyM:
            pass
        else:
            return NotImplemented
        return divmod(self,other)[1]
    
    
    def __rmod__(self,other):
        """Remainder of Euclidean division of polynomials"""
        other % self
    
    
    def copy(self):
        """Copy the polynomial"""
        return ZPolyM(self.coef[:],self.M)


    def derivative(self):
        """Calculate the formal derivative of the polynomial"""
        co = self.coef.copy()
        for i in range(len(co)):
            co[i] *= i
        return ZPolyM(co[1:],self.M)


    def _content(self):
        return gcd(self.coef)
    
    
    def _primitive_part(self):
        co = [c//self.content for c in self.coef]
        return ZPolyM( co,self.M)
    

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
            self[i] = mod_div(self[i],C,self.M)


    def _pretty_name(self):
        """Formatted for LaTeX"""
        return f"{zpoly_print_pretty(self)} (mod {self.M})"


    # Things that are like attributes can be access as properties
    pretty_name = property(_pretty_name)
    full_name = property(_full_name)
    monic_part = property(_monic_part)
    content = property(_content)
    primitive_part = property(_primitive_part)




if __name__ == '__main__':
    F = 17
    P = ZPolyM( [1,4,7], F = F )
    Q = ZPolyM( [8,1], F = F)
    print(f"P = {P.full_name}")
    print(f"Q = {Q.full_name}")
    print()
    print(f"P//Q = {P//Q}")
    print(f"P%Q  = {P%Q}")
    print("Check the the process reverses")
    print((P//Q)*Q+(P%Q) == P)
    
    print(P.monic_part)
    print(P.full_name)

    
    F = 2
    R = ZPolyM( [1,1,0,0,1], F = F )
    S = ZPolyM( [0,1], F = F )
    out = ZPolyM( [1], F = F )
    print(f"\n\nOne version of of GF(16)")
    print(f"0 = {R}")
    for i in range(15):
        print(out)
        out = (out * S) % R