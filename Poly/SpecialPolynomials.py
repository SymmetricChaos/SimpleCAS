from QPoly import QPoly

## TODO: generators for abel
## TODO: bernoulli, legendre
## TODO: examples of using these sequences

def abel_poly(n,a):
    """Abel polynomial"""
    if n == 0:
        return QPoly([1])
        
    x = QPoly([0,1])
    
    return x*(x-a*n)**(n-1)


def chebyshev_poly(n,kind=1):
    """Chebyshev polynomial"""
    if kind == 1:
        
        if n == 0:
            return QPoly([1])
        elif n == 1:
            return QPoly([0,1])
        else:
            return QPoly([0,2])*chebyshev_poly(n-1,1) - chebyshev_poly(n-2,1)
    
    elif kind == 2:
        
        if n == 0:
            return QPoly([1])
        elif n == 1:
            return QPoly([0,2])
        else:
            return QPoly([0,2])*chebyshev_poly(n-1,2) - chebyshev_poly(n-2,2)

    else:
        raise Exception(f"There are only Chebyshev polynomials of the 1st and 2nd kind")


def chebyshev_poly_gen(n,kind=1):
    """Chebyshev polynomial"""
    if kind == 1:
        
        K0 = QPoly([1])
        K1 = QPoly([0,1])
        for i in range(n):
            yield K0
            K0, K1 = K1, QPoly([0,2])*K1 - K0
    
    elif kind == 2:
        
        K0 = QPoly([1])
        K1 = QPoly([0,2])
        for i in range(n):
            yield K0
            K0, K1 = K1, QPoly([0,2])*K1 - K0

    else:
        raise Exception(f"There are only Chebyshev polynomials of the 1st and 2nd kind")


def falling_factorial(n):
    """Polynomial representation of the falling factorial"""
    x = QPoly([0,1])
    out = 1
    for k in range(n):
        out *= (x-k)
    return out


def falling_factorial_gen(n):
    """Generator polynomial representations of the falling factorial"""
    x = QPoly([0,1])
    out = 1
    for k in range(n):
        yield out
        out *= (x-k)


def rising_factorial(n):
    """Polynomial representation of the rising factorial"""
    x = QPoly([0,1])
    out = 1
    for k in range(n):
        out *= (x+k)
    return out


def rising_factorial_gen(n):
    """Generator polynomial representations of the rising factorial"""
    x = QPoly([0,1])
    out = 1
    for k in range(n):
        yield out
        out *= (x+k)


def fibonacci_poly(n):
    x = QPoly([0,1])
    if n == 0:
        return QPoly([0])
    elif n == 1:
        return QPoly([1])
    else:
        return x*fibonacci_poly(n-1) + fibonacci_poly(n-2)


def fibonacci_poly_gen(n):
    x = QPoly([0,1])
    F0 = QPoly([0])
    F1 = QPoly([1])
    for i in range(n):
        yield F0
        F0, F1 = F1, x*F1 + F0
        
        
def lucas_poly(n):
    x = QPoly([0,1])
    if n == 0:
        return QPoly([0])
    elif n == 1:
        return QPoly([1])
    else:
        return x*fibonacci_poly(n-1) + fibonacci_poly(n-2)


def lucas_poly_gen(n):
    x = QPoly([0,1])
    F0 = QPoly([2])
    F1 = QPoly([0,1])
    for i in range(n):
        yield F0
        F0, F1 = F1, x*F1 + F0
        

    





if __name__ == '__main__':
    
    print("Abel Polynomials for a = 1")
    for n in range(7):
        print(abel_poly(n,1))
        
    print("\n\nChebyshev Polynomials of the 1st Kind")
    for i in chebyshev_poly_gen(7,1):
        print(i)
        
    print("\n\nChebyshev Polynomials of the 2nd Kind")
    for i in chebyshev_poly_gen(7,2):
        print(i)
        
    print("\n\nFalling Factorial Polynomials")
    for i in falling_factorial_gen(7):
        print(i)
        
    print("\n\nRising Factorial Polynomials")
    for i in rising_factorial_gen(7):
        print(i)
        
    print("\n\nFibonacci Polynomials")
    for i in fibonacci_poly_gen(7):
        print(i)
        
    print("\n\nLucas Polynomials")
    for i in lucas_poly_gen(7):
        print(i)