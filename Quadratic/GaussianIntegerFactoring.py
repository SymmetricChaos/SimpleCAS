from Utility.Math import prime_factorization
from Quadratic.GaussianIntegers import GaussInt, str_to_gauss, all_with_norm, associates
from itertools import product

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
    """Return a prime factorization up to unit multiplication"""
    a = associates(G)
    F = prime_factorization(G.norm)
    L = []
    for f in F:
        L.append([i for i in all_with_norm(f)])
    
    for i in product(*L):
        pr = GaussInt(1)
        for fs in i:
            pr *= fs
        if pr in a:
            return i
    

if __name__ == '__main__':
    L = ["5","2+5i","-2-5i","-11+7i","88-23i","15+22i"]
    for i in L:
        g = str_to_gauss(i)
        p = "is prime" if is_gauss_prime(g) else "is not prime"
        print(f"{i:<7}{p}")
    
    print("\n\nPrime Factorization")
    g = GaussInt(-11,7)
    print(g)
    
    print(f"The norm of {g} is {g.norm}")
    print(f"The prime factorization of {g.norm} is {prime_factorization(g.norm)}")
    print(f"By searching gaussian integers with these norms we find a prime factorization of:\n{gauss_factorization(g)}")
