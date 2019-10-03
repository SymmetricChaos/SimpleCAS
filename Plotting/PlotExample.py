from Rational import rational_seq
from RationalFunc import RationalFunc
from Utility import make_canvas, plot_points
from Poly import QPoly


P = QPoly( [0,1,0,"-1/6",0,"1/120",0,"-1/5040"] )
x = rational_seq(-7,7,.1)
y = P.evaluate(x)
pts = [i for i in zip(x,y)]

make_canvas([-6,6],show_axes=True,title=P.pretty_name())
plot_points(pts)

print(P.pretty_name())


R = RationalFunc(P,[-1,1])
x = rational_seq(-7,7,.1)
y = R.evaluate(x)
pts = [i for i in zip(x,y)]

make_canvas([-6,6],show_axes=True,title=R.pretty_name())
plot_points(pts)