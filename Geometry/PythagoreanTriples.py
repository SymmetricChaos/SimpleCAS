from Utility import gcd

def prim_pythag_triples(N):
    """N is the limit of m and n in Euclid's formula"""
    
    for m in range(1,N):
        for n in range(m+1,N):
            if gcd(n,m) == 1: # must be coprime
                if not (n%2 == 1 and m%2 == 1): # can't both be odd
                    a = n*n-m*m
                    b = 2*m*n
                    c = m*m+n*n
                    
                    yield sorted([a,b,c])

            


            
if __name__ == '__main__':
    from Utility import make_canvas, scatter_points
        
    for i in prim_pythag_triples(10):
        print(i)
        
    make_canvas([-1.2,1.2],size=6,title="Rational Points on a Circle")
    pts = []
    for i in prim_pythag_triples(10):
        pts += [[i[0]/i[2],i[1]/i[2]]]
        pts += [[-i[0]/i[2],i[1]/i[2]]]
        pts += [[i[0]/i[2],-i[1]/i[2]]]
        pts += [[-i[0]/i[2],-i[1]/i[2]]]

    scatter_points(pts,s=2)
    