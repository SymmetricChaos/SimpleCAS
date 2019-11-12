from Rational.RationalType import Rational
from Rational.RationalUtils import mediant
from Rational.CastToRational import cast_to_rational
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


def harmonic_progression(a=1,d=1):

    a = cast_to_rational(a)
    d = cast_to_rational(d)
    
    den = a
    one = Rational(1)
    while True:
        yield one/den
        den += d
        
def harmonic_series():
    out = Rational(1)
    ctr = 2
    while True:
        yield out
        out += Rational(1,ctr)
        ctr += 1

    
    

if __name__ == '__main__':
    from Utility import make_canvas, scatter_points, show_plot

    print("Farey Sequence F_12")
    F12 = [i for i in farey_sequence(12)]
    print(F12)
    
    print()
    xy = question_mark_func(40)
    make_canvas([-.02,1.02],size=6,title="Minkowski's Question-mark Function\nAt Rational Arguments")
    scatter_points(xy,s=1)
    show_plot()

    
    print("\n\nHarmonic Progressions")
    S1 = harmonic_progression(a=1,d=1)
    for pos,val in enumerate(S1):
        if pos > 10:
            break
        print(val)
            
    print()
    S2 = harmonic_progression(a="1/3",d="2/9")
    for pos,val in enumerate(S2):
        if pos > 10:
            break
        print(val)
    
    print()
    H = harmonic_series()
    for pos,val in enumerate(H):
        if pos > 5:
            break
        print(val)
