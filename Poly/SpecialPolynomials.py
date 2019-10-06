from QPoly import QPoly

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





if __name__ == '__main__':
    
    print("Abel Polynomials for a = 1")
    for n in range(6):
        print(abel_poly(n,1))
        
    print("\n\nChebyshev Polynomials of the 1st Kind")
    for i in range(6):
        print(chebyshev_poly(i,1))
        
    print("\n\nChebyshev Polynomials of the 2nd Kind")
    for i in range(6):
        print(chebyshev_poly(i,2))
        
    print("\n\nFalling Factorial Polynomials")
    for i in falling_factorial_gen(6):
        print(i)
        
    print("\n\nRising Factorial Polynomials")
    for i in rising_factorial_gen(6):
        print(i)
        