from QPoly import QPoly

def abel_poly(n,a):
    if n == 0:
        return QPoly([1])
        
    x = QPoly([0,1])
    
    return x*(x-a*n)**(n-1)


def chebyshev_poly(n):
    if n == 0:
        return QPoly([1])
    elif n == 1:
        return QPoly([0,1])
    else:
        return 2*QPoly([0,1])*chebyshev_poly(n-1) - chebyshev_poly(n-2)
    

if __name__ == '__main__':
    
    print("Abel Polynomials for a = 1")
    for n in range(6):
        print(f"p_{n} =",abel_poly(n,1))
        
    print("\n\nChebyshev Polynomials")
    for n in range(6):
        print(f"T_{n} =",chebyshev_poly(n))