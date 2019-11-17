def egcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

		
def gcd(*args):
    """Greatest Common Denominator"""

    # Handle the case that a list is provided
    if len(args) == 1 and type(args[0]) is list:
        return gcd(*args[0])
    
    # the gcd of a single number is itself
    if len(args) == 1:
        return args[0]
    
    # calculate gcd for two numbers
    if len(args) == 2:
        a = args[0]
        b = args[1]
        g,_,_ = egcd(a,b)
        return g
    
    # if more than two break it up recursively
    a = gcd(*args[0:2])
    b = gcd(*args[2:])
    return gcd(a,b)

	
def lcm(*args):
    """Least Common Multiple"""
    
    # Handle the case that a list is provided
    if len(args) == 1 and type(args[0]) is list:
        return lcm(*args[0])
    
    # the lcm of a single number is itself
    if len(args) == 1:
        return args[0]
    
    # calculate lcm for two numbers
    if len(args) == 2:
        a = args[0]
        b = args[1]
        g,_,_ = egcd(a,b)
        return abs(a*b)//g
    
    # if more than two break it up recursively
    a = lcm(*args[0:2])
    b = lcm(*args[2:])
    return lcm(a,b)


def mod_inv(a, m):
    """Modular Multiplicative Inverse"""
    
    a = a % m
    
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"Multiplicative inverse of {a} mod {m} does not exist")
    else:
        return x % m
    
    
def mod_div(a,b,m):
    """a divided by b modulo m"""
    return (a * mod_inv(b,m)) % m


def factorial(n):
    """Factorial of n"""
    if type(n) != int:
        raise TypeError(f"n must be an integer not {type(n)}")
    out = 1
    for i in range(1,n+1):
        out *= i
    return out


def choose(n,k):
    """Binomial coefficient"""
    if type(n) != int:
        raise TypeError(f"n must be an integer not {type(n)}")
    if type(k) != int:
        raise TypeError(f"k must be an integer not {type(k)}")
    if n < k:
        raise ValueError("n cannot be less than k")
    if k < 0:
        raise ValueError("k must be nonnegative")
        
    # Calculate the numerator and denominator seperately in order to avoid loss
    # of precision for large numbers.
    N = 1
    D = 1
    for i in range(1,k+1):
        N *= (n+1-i)
        D *= i
    return N//D


def kronecker_delta(i,j):
    """The Kronecker delta"""
    if i == j:
        return 1
    return 0


def estimate_root(x):
    """Crude Estimate for Square Root"""
    return x // (10**(len(str(x))//2))


def int_root(x):
    """Integer Square Root"""
    
    a = estimate_root(x)
    
    if a == 0:
        return 0
    
    b = (a+(x//a))//2
    
    t = [(a,b)]
    
    while True:
        if b == 0:
            break
        a, b = b, (b+(x//b))//2
        if (a,b) in t:
            break
        t.append((a,b))
    
    # Sometimes b is too large when we reach a stopping point, this fixes that
    if b**2 > x:
        return b-1
    return b


def factorization(n,negatives=False):
    """All Unique Factors"""
    if type(n) != int:
        raise TypeError("n must be an integer") 
    
    if n == 0:
        return [0]
    
    lim = int_root(n)+1
    
    if negatives == True:
        L = [1,-1,n,-n]
    else:
        L = [1,n]
    
    for i in range(2,lim):
        f,r = divmod(n,i)
        if f == 0 or i == 0:
            print(n)
        if r == 0:
            if negatives == True:
                L += [i,-i,f,-f]
            else:
                L += [i,f]
            
    L = list(set(L))
    L.sort()
    
    return L


def primes():
    """Prime Numbers"""
    D = {}
    q = 2
    
    while True:
        if q not in D:
            
            yield q
                
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1


def prime_factorization(n):
    """Prime Factors with Multiplicity"""
    if type(n) != int:
        raise TypeError("n must be an integer") 
    
    lim = int_root(n)+1
    L = []
    
    for p in primes():
        while n % p == 0:
            L.append(p)
            n = n // p
            
        if n == 1:
            break
        
        if p > lim:
            L.append(n)
            break
    return L


def cantor_pair(x,y):
    """A unique positive integer that represents the order pair (x,y), x and y positive"""
    if type(x) != int or type(y) != int:
        raise TypeError("arguments must be integers")
    if x < 0 or y < 0:
        raise ValueError("arguments must be positive")
    return ((x+y)*(x+y+1))//2+y


def cantor_tuple(*ks):
    """A unique integer that represents the given tuple"""
    if len(ks) == 2:
        return cantor_pair(ks[0],ks[1])
    else:
        return cantor_tuple(cantor_tuple(*ks[:-1]),ks[-1])


def cantor_pair_inv(n):
    """Inverse of the cantor pairing function"""
    if type(n) != int :
        raise TypeError("n must be an integer")
    if n < 0 :
        raise ValueError("n must be positive")

    w = (int_root(8*n+1)-1)//2
    t = (w*w+w)//2
    y = n - t
    x = w - y
    return x,y