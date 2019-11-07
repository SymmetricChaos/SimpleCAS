from Rational.RationalType import Rational

def farey_sequence(n):
    """All unique fractions between 0 and 1 with denominator less than or equal to n"""
    a, b, c, d = 0, 1, 1, n
    yield Rational(a,b)
    
    while c <= (10):
        k = (n+b)//d
        a, b, c, d = c, d, k*c-a, k*d-b
        yield Rational(a,b)


if __name__ == '__main__':
    
    print("Farey Sequence F_15")
    F5 = [i for i in farey_sequence(15)]
    print(F5)