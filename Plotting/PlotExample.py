from Rational import Rational, rational_seq
from Utility import make_canvas, plot_points
from Poly import QPoly


c3 = Rational(-1,6)
c5 = Rational(1,120)
c7 = Rational(-1,5040)

P = QPoly( [0,1,0,c3,0,c5,0,c7] )
x = rational_seq(-5,5,".01")
y = P.evaluate(x)

pts = [i for i in zip(x,y)]

make_canvas([-6,6],show_axes=True,title=P.pretty_name())

plot_points(pts)