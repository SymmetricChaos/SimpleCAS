from Utility.Math import prime_factorization
from Quadratic.GaussianIntegers import GaussInt, str_to_gauss

def is_guass_prime(G):
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


if __name__ == '__main__':
    L = ["5","2+5i","-2-5i"]
    for i in L:
        g = str_to_gauss(i)
        print(g,is_guass_prime(g))