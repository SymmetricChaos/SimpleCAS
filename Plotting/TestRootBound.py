from Rational import rational_seq
from Utility import make_canvas, plot_points, scatter_points, connect
from Poly import QPoly, all_roots, critical_points, sturm_root_isolation
from random import randint

co = [randint(-9,9) for i in range(5)]
co = [3,-1,3,-7,-5]
P = QPoly( co )
print(f"P = {P}")
r = all_roots(P)
print(f"roots = {r}")
c = critical_points(P)
print(f"critical = {c}")
print(f"root_intervals = {sturm_root_isolation(P)}")

interesting_points = r + c
interesting_values = P.evaluate(interesting_points)




xwidth = [ float(min(interesting_points)-1), float(max(interesting_points)+1) ]
ywidth = [ float(min(interesting_values)-1), float(max(interesting_values)+1) ]

x = rational_seq(xwidth[0],xwidth[1],.05)
y = [float(i) for i in P.evaluate(x)]
x = [float(i) for i in x]


pts = [i for i in zip(x,y)]
make_canvas(xwidth,ywidth,size=[5,5],show_axes=True,title=P.pretty_name())
plot_points(pts,color="black")

connect([xwidth[0],0],[xwidth[1],0],color="gray",zorder=-1)

pts2 = [i for i in zip(interesting_points,interesting_values)]
scatter_points(pts2,zorder=5)
