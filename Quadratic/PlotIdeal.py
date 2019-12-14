from Quadratic.GaussianIntegers import GaussInt, ideal
from Utils.Drawing import make_canvas, scatter_points, connect



make_canvas([-6,6],[-6,6],show_axes = True)

G = GaussInt(1,2)

pts = []

for i,val in enumerate(ideal(G)):
    if i > 50:
        break
    pts.append((val.re,val.im))

scatter_points(pts)
scatter_points([[G.re,G.im]],color='red',s=100)
connect([-10,0],[10,0],color="gray",zorder=0)
connect([0,-10],[0,10],color="gray",zorder=0)

for i in range(-10,10):
    connect([-10,i],[10,i],color="lightgray",zorder=-1)
    connect([i,-10],[i,10],color="lightgray",zorder=-1)