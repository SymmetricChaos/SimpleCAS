from Rational import rational_seq
from Utility import make_canvas, plot_points
from Poly import QPoly, all_roots
from random import randint

co = [randint(-9,9) for i in range(4)]
P = QPoly( co )
r = all_roots(P)
xwidth = [ float(r[0]-1), float(r[-1]+1) ]
x = rational_seq(r[0]-1,r[-1]+1,.1)
y = [float(i) for i in P.evaluate(x)]
x = [float(i) for i in x]
ywidth = (min(y),max(y))

pts = [i for i in zip(x,y)]
make_canvas(xwidth,ywidth,size=[5,5],show_axes=True,title=P.pretty_name())

plot_points(pts)