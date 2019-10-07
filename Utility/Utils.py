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
        g,x,y = egcd(a,b)
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
        g,x,y = egcd(a,b)
        return abs(a*b)//g
    
    # if more than two break it up recursively
    a = lcm(*args[0:2])
    b = lcm(*args[2:])
    return lcm(a,b)


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
        raise Exception("n cannot be less than k")
    if k < 0:
        raise Exception("k must be nonnegative")
        
    # Calculate the numerator and denominator seperately in order to avoid loss
    # of precision for large numbers.
    N = 1
    D = 1
    for i in range(1,k+1):
        N *= (n+1-i)
        D *= i
    return N//D
    





def inds_where(L,val):
    return [i for i in range(len(L)) if L[i] == val]


def first_where(L,val):
    for pos,l in enumerate(L):
        if l == val:
            return pos
    return None
     




def poly_normalize(P):
    """Remove trailing zeroes"""
    while P[-1] == 0 and len(P) > 1:
        if len(P) == 1:
            break
        P.pop()


def poly_pad(P,n):
    """Add trailing zeroes"""
    out = P.copy()
    while len(out) < n:
        out.append(0)
    return out
	

def poly_add(P, Q):
    """Take list of polynomial coefficients and add them"""
        
    pad = max(len(P),len(Q))
    
    P = poly_pad(P,pad)
    Q = poly_pad(Q,pad)
    
    out = []
    
    for x,y in zip(P,Q):
        out.append( x+y )

    poly_normalize(out)

    return out


def poly_mult(P, Q):
    """Take list of polynomial coefficients and multiply them"""
    
    out = [0]*(len(P)+len(Q))
    
    for i in range(len(P)):
        for j in range(len(Q)):
            out[i+j] += P[i]*Q[j]
            out[i+j] = out[i+j]

    
    poly_normalize(out)

    return out





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