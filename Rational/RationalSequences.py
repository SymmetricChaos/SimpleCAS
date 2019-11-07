from Rational.RationalType import Rational
from Rational.RationalUtils import mediant
from Utility import sort_by_nth

def farey_sequence(n):
    """All unique fractions between 0 and 1 with denominator less than or equal to n"""
    a, b, c, d = 0, 1, 1, n
    yield Rational(0)
    
    while c <= n:
        k = (n+b)//d
        a, b, c, d = c, d, k*c-a, k*d-b
        yield Rational(a,b)


def question_mark_func(n):
    """Use the Farey sequences to calculate the question mark function"""
    
    known_val = {Rational(0) : Rational(0),
                 Rational(1) : Rational(1)}

    out = [(Rational(0),Rational(0))]
    for i in range(1,n):

        S = farey_sequence(i)
    
    
        a = next(S)
        b = next(S)
        while True:
            new = mediant(a,b)
            val = (known_val[a]+known_val[b])/2
            
            
            if new not in known_val:  
                known_val[new] = val
                out.append((new,val))
            
            a = b
            try:
                b = next(S)
            except StopIteration:
                break
    
    out += [(Rational(1),Rational(1))]
    out = sort_by_nth(out,0)
    return out


    
    

if __name__ == '__main__':
    from Utility import make_canvas, scatter_points

    print("Farey Sequence F_15")
    F15 = [i for i in farey_sequence(12)]
    print(F15)
    
    print("\n\n")
    xy = question_mark_func(30)
    make_canvas([0,1],size=5,title="Minkowski's Question-mark Function\nAt Rational Arguments")
    scatter_points(xy,s=1)
    
    print("Minkowski's Question-mark Function at some rational arguments")
    xy = question_mark_func(5)
    print(xy)