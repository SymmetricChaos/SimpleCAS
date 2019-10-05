from QPoly import QPoly

def abel_poly(n,a):
    if n == 0:
        return QPoly([1])
        
    x = QPoly([0,1])
    
    return x*(x-a*n)**(n-1)
    
    
if __name__ == '__main__':
    
    print("Abel Polynomials for a = 1")
    for n in range(6):
        print(f"p_{n} =",abel_poly(n,1))