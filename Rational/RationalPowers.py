from Rational import Rational, coerce_to_rational

# Rational numbers raised to the power of rational numbers
class RationalPower:
    
    def __init__(self,base=1,pwr=1):
        self.base = coerce_to_rational(base)
        self.pwr = coerce_to_rational(pwr)
        self.simplify()

    def simplify(self):
        pass
        
    def __str__(self):
        if self.pwr == 1:
            return str(self.base)
        p = f"{self.pwr}" if self.pwr.d == 1 else f"({self.pwr})"
        return f"{self.base}^{p}"
    
    def __mul__(self,other):
        if type(other) == RationalPower:
            if other.base == self.base:
                return RationalPower(self.base,self.pwr+other.pwr)
            
        

#    # Produce decimal expansion
#    def digits():
        

        

# Sums and multiples of rational powers possibly with different bases
#class RationalPowerExpression:
        
    
if __name__ == '__main__':
    r = RationalPower(8,"1/3")
    print(r)
    print(r*r)
    
    
