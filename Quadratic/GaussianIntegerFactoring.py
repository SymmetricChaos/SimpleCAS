from Utility.Math import prime_factorization
from Quadratic.GaussianIntegers import GaussInt, str_to_gauss

def is_gauss_prime(G):
    assert type(G) == GaussInt
    
    if G.re == 0:
        if abs(G.im) % 4 == 3:
            if len(prime_factorization(abs(G.im))) == 1:
                return True
    elif G.im == 0:
        if abs(G.re) % 4 == 3:
            if len(prime_factorization(abs(G.re))) == 1:
                return True
    
    if len(prime_factorization(G.norm)) == 1:
        return True
    
    return False

# The norm is a multiplcative function
# Thus if we can factor the norm we known the norms of the factors
def gauss_factorization(G):
    F = prime_factorization(G.norm)
    print(F)


if __name__ == '__main__':
    L = ["5","2+5i","-2-5i","-11+7i","88-23i","15+22i"]
    for i in L:
        g = str_to_gauss(i)
        print(g,is_gauss_prime(g))
    
    g = GaussInt(-11,7)
    print(gauss_factorization(g))