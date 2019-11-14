# Generalized continued fractions

from Rational.RationalType import Rational

class CFracG:
    
    def __init__(self,nums,dens):
        
        if len(nums) != len(dens):
            raise ValueError(f"Same number of numerators and denominators must be provided")
    
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


#    def __str__(self):
#        out = str(self.terms)
#        out = out.replace(",",";",1)
#        return out
    
    
    def __len__(self):
        return len(self.nums)
    
#    def as_rational(self):
#        """Convert a generalized continued fraction to a Rational"""
#    
#        L = self.terms
#        
#        N = [1,L[0]]
#        D = [0,1]
#        con = 2
#        
#        while con < len(self)+1:
#            N.append( L[con-1] * N[con-1] + N[con-2] )
#            D.append( L[con-1] * D[con-1] + D[con-2] )
#            con += 1
#            
#        return Rational(N[-1],D[-1])  
#    
#            
#    def convergents(self):
#        """Rational convergents"""
#        T = self.terms
#        N = [1,T[0]]
#        D = [0,1]
#        con = 2
#        
#        yield Rational(N[-1],D[-1])
#        
#        while con < len(self)+1:
#            N.append( T[con-1] * N[con-1] + N[con-2] )
#            D.append( T[con-1] * D[con-1] + D[con-2] )
#        
#            yield Rational(N[-1],D[-1])
#            
#            con += 1
#            
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
#

    # There are multiple pretty conventions for CFracG so at least one other
    # should be supported
    def _pretty_name(self):
        """Name formatted for LaTeX, requires amsmath"""

        if len(self) == 1:
            return str(self[0])
        
        else:
        
            prm = "#+\cfrac{##}{*}"
            out = "*"
            for n,d in zip(self.nums[:-1],self.dens[:-1]):
                out = out.replace("*",prm)
                out = out.replace("##",str(n))
                out = out.replace("#",str(d))
            out = out.replace("*",str(self.nums[-1]))
            return f"${out}$"
        

    pretty_name = property(_pretty_name)







if __name__ == '__main__':

    C = CFracG([1,2,3,4],[2,2,2,2])
    print(C)
    print(C.pretty_name)