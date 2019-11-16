# Generalized continued fractions

from Rational.RationalType import Rational

class CFracG:
    
    def __init__(self,nums,dens):
        
        if len(nums) != len(dens):
            raise ValueError(f"Same number of numerators and denominators must be supplied")

    
        if type(nums) not in [list,tuple]:
            raise TypeError(f"Numerators must be given as a list or tuple, not {type(nums)}")
        else:
            for i in nums:
                if type(i) != int:
                    raise TypeError(f"All numerators must be given as int not {type(i)}")
        self.nums = nums
        
        
        if type(dens) not in [list,tuple]:
            raise TypeError(f"Denominators must be given as a list or tuple, not {type(nums)}")
        else:
            for i in dens:
                if type(i) != int:
                    raise TypeError(f"All denominators must be given as int not {type(i)}")
        self.dens = dens

    
    def __len__(self):
        return len(self.nums)
    
    
    def __str__(self):
        if len(self) == 1:
            return str(self[0])
        
        else:
            prm = "#+##/(*)" #primitive element
            out = "*"
            for n,d in zip(self.nums[:-1],self.dens[:-1]):
                out = out.replace("*",prm)
                out = out.replace("##",str(n))
                out = out.replace("#",str(d))
            out = out.replace("*",str(self.dens[-1]))
            out = out.replace(f"({self.dens[-1]})",f"{self.dens[-1]}")
            if self.dens[0] == 0:
                return out[2:]
            else:
                return out


    def as_rational(self):
        """Convert a generalized continued fraction to a Rational"""
    
        A1 = self.dens[0]
        A2 = self.dens[1]*self.dens[0]+self.nums[0]
        
        B1 = 1
        B2 = self.dens[1]
                
        for d,n in zip(self.dens[2:],self.nums[1:]):
            
            A1, A2 = A2, d*A2+n*A1
            B1, B2 = B2, d*B2+n*B1
            
        return Rational(A2,B2) 


    def convergents(self):
        """Rational convergents"""

        A1 = self.dens[0]
        A2 = self.dens[1]*self.dens[0]+self.nums[0]
        
        B1 = 1
        B2 = self.dens[1]
        
        
        yield Rational(A1,B1)
        
        for d,n in zip(self.dens[2:],self.nums[1:]):
            
            A1, A2 = A2, d*A2+n*A1
            B1, B2 = B2, d*B2+n*B1
        
            yield Rational(A1,B1)
            
        yield Rational(A2,B2)


#    def semiconvergents(self):
#        """Rational semiconvergents"""
#  
#        a = self.terms
#        Q = self.as_rational()
#        
#        prev = Rational(a[0])
#        for pos,val in enumerate(a):
#            # Try appending the floor of half the next convergent
#            semi = a[:pos]+[(val-1)//2+1]
#            semi = CFrac(semi)
#            
#            # If it is worse than the last semiconvergent add 1
#            if abs(semi.as_rational() - Q)  >  abs(prev - Q):
#                semi.terms[pos] += 1
#                
#            while semi.terms[pos] <= val:
#                yield prev
#                prev = semi.as_rational()
#                semi.terms[pos] += 1
#        yield Q


    # There are multiple pretty conventions for CFracG so at least one other
    # should be supported
    def _pretty_name(self):
        """Name formatted for LaTeX, requires amsmath"""

        if len(self) == 1:
            return str(self[0])
        
        else:
            prm = "#+\cfrac{##}{*}" #primitive element
            out = "*"
            for n,d in zip(self.nums[:-1],self.dens[:-1]):
                out = out.replace("*",prm)
                out = out.replace("##",str(n))
                out = out.replace("#",str(d))
            out = out.replace("*",str(self.dens[-1]))
            if self.dens[0] == 0:
                return f"${out[2:]}$"
            else:
                return f"${out}$"
        

    pretty_name = property(_pretty_name)





if __name__ == '__main__':

        
    print()
    C = CFracG([1,1,1,1],[2,3,1,4])
    print(C.pretty_name)
    print(C)
    
    for i in C.convergents():
        print(i)
        
    print("\nAbove should be:\n2\n7/3\n9/4\n43/19")
        
        
    print()
    C = CFracG([4,1,4,9,16,25,36,49,64],[0,1,3,5,7,9,11,13,15])
    print(C.pretty_name)

    
    for i in C.convergents():
        s = str(i)
        print(f"{s:<12} = {i.digits(6)}")