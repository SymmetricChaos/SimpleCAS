from Rational import rational_seq
from RationalFunc import RFunc, rfunc_roots
from Utility import make_canvas, plot_points, scatter_points
from Poly import QPoly


P = QPoly( [0,1,0,"-1/6",0,"1/120",0,"-1/5040"] )
x = rational_seq(-7,7,.1)
y = P.evaluate(x)
pts = [i for i in zip(x,y)]

make_canvas([-6,6],show_axes=True,title=P.pretty_name)
plot_points(pts)
print(P.pretty_name)

# TODO: decide on a way to draw rational functions without making streaks along
#       the asymptotes
R = RFunc(P,[-.5,2,1])
x = rational_seq(-7,7,.05)
y = R.evaluate(x)
pts = [i for i in zip(x,y)]

make_canvas([-6,6],show_axes=True,title=R.pretty_name)
plot_points(pts)
print(R.pretty_name)
xy = [(i,R(i)) for i in rfunc_roots(R)]
scatter_points(xy)