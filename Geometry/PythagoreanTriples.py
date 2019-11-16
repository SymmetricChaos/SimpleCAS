from Utility import gcd

def prim_pythag_triples(N):

    
    for m in range(1,N):
        for n in range(m+1,N):
            if gcd(n,m) == 1: # must be coprime
                if not (n%2 == 1 and m%2 == 1): # can't both be odd
                    a = n*n-m*m
                    b = 2*m*n
                    c = m*m+n*n
                    
                    yield sorted([a,b,c])
            



            
if __name__ == '__main__':
    
    for i in prim_pythag_triples(7):
        print(i)