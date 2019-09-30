from Rational import rational_seq
from Utility import make_canvas, plot_points
from Poly import QPoly, bound_of_roots
from random import randint

co = [randint(-9,9) for i in range(4)]
P = QPoly( co )
b = (bound_of_roots(P)+1)//1
x = rational_seq(-b,b,.05)
y = [float(i) for i in P.evaluate(x)]

pts = [i for i in zip(x,y)]

#b = max(b,max(y))

make_canvas([-b,b],show_axes=True,title=P.pretty_name())

plot_points(pts)
plot_points( [ [-10,0], [10,0] ]  )