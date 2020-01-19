from math import sqrt

class QuadInt2:
    
    def __init__(self,a,b=0):
        assert type(a) == int
        assert type(b) == int
        
        # Integer part
        self.a = a
        
        # Quadratic part
        self.b = b


    def __float__(self):
        return self.a + self.b*sqrt(2)


    def __str__(self):
        
        # If the quadratic part is zero return just the whole part
        if self.b == 0:
            return f"{self.a}"
        
        # If the quadratic part is negative
        elif self.b < 0:
            # Unit case
            if self.b == -1:
                if self.a == 0:
                    return f"-√2"
                else:
                    return f"{self.a} - √2"
            # General case
            if self.a == 0:
                return f"-{self.b}√2"
            else:
                return f"{self.a} - {abs(self.b)}√{2}"
        
        # If the quadratic part is positive
        else:
            # Unit case
            if self.b == 1:
                if self.a == 0:
                    return f"√2"
                else:
                    return f"{self.a} + √2"
            # General case
            if self.a == 0:
                return f"{self.b}√2"
            else:
                return f"{self.a} + {self.b}√2"

    
    def __add__(self,other):
        if type(other) == QuadInt2:
            return QuadInt2(self.a+other.a,
                            self.b+other.b)
        elif type(other) == int:
            return QuadInt2(self.a+other,self.b)
        else:
            return NotImplemented
        
        
    def __sub__(self,other):
        return self + -other


    def __mul__(self,other):
        if type(other) == QuadInt2:
            return QuadInt2(self.a*other.a + self.b*other.b*2,
                            self.a*other.b + other.a*self.b
                            )
        elif type(other) == int:
            return QuadInt2(other*self.a,
                            other*self.b)
        else:
            return NotImplemented
        
        
    def __pow__(self,other):
        if type(other) == int:
            if other < 0:
                raise ValueError("Only non-negative powers allowed")
            out = QuadInt2(1)
            for i in range(other):
                out *= self
            return out
            
        else:
            return NotImplemented


    def __neg__(self):
        return QuadInt2(-self.a,-self.b)
        

    def __eq__(self,other):
        if type(other) == QuadInt2:
            if self.a == other.a:
                if self.b == other.b:
                    return True
        return False
    
    
    def norm(self):
        return self.a*self.a - self.b*self.b*2


    def conjugate(self):
        return QuadInt2(self.a,-self.b)





def div_by_root(a):
    return QuadInt2(a.b,a.a//2)



def quad_int2_gcd(a,b,d=QuadInt2(1)):
    """GCD using Stein's method"""

    if a == b or a == -b:
        return d*a
    
    if b.norm() == 1:
        return d
    
    if b == QuadInt2(0):
        return d*a
    
    
    if a.a%2 == b.a%2 == 0:
        return quad_int2_gcd(div_by_root(a),div_by_root(b),d*QuadInt2(0,1))
    
    if a.a%2 == b.a%2 == 1:
        return quad_int2_gcd(div_by_root(a+b),div_by_root(a-b),d)
    
    if a.a%2 == 0 and b.a%2 == 1:
        return quad_int2_gcd(a,div_by_root(b),d)
    
    if a.a%2 == 1 and b.a%2 == 0:
        return quad_int2_gcd(div_by_root(a),b,d)
    
    else:
        raise Exception("IT DIDNT WORK. HELP!")





if __name__ == '__main__':
#    Q = QuadInt2(0,1)
#    R = QuadInt2(3,2)
#    print(Q)
#    print(R)
#    print(Q+R)
#    print(Q*R)
#    print(Q*Q)
#    print(R*R)
#    print(R.conjugate())
#    print(Q+2)
#    print(R*2)
#    print(-R)
#    print(float(R))
#    print(R-Q)
#    print(R**2)
    
    print()
    Q = QuadInt2(9,8)
    R = QuadInt2(5,6)
    one = QuadInt2(1)
    zero = QuadInt2(0)
    sqrt2 = QuadInt2(0,1)
    print(Q)
    print(R)
    print(quad_int2_gcd(Q,R))