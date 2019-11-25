#from PowerSeries import PSeries
from itertools import cycle
from Rational import Rational

def sine_series_terms():
    n = cycle([1,0,-1,0])
    d = 1
    ctr = 2
    for num in n:
        yield Rational(num,d)
        d *= ctr
        ctr += 1
    
if __name__ == '__main__':
    for i in enumerate(sine_series_terms()):
        if i[0] > 9:
            break
        print(i[1])