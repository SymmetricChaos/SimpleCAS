from Quadratic.GaussianIntegers import GaussInt, all_with_norm, all_gauss_int
from Quadratic.GaussianIntegerFactoring import is_gauss_prime
from Utility.Drawing import make_canvas, scatter_points, connect
from Utility.Math import int_root


example_norm = 970
sz = int(int_root(example_norm)*1.2)

make_canvas([-sz,sz],[-sz,sz],size=8,show_axes=True,title=f"Gaussian Integers with Norm {example_norm}")


connect([-sz,0],[sz,0],color="gray",zorder=0)
connect([0,-sz],[0,sz],color="gray",zorder=0)

for i in range(-sz,sz):
    connect([-sz,i],[sz,i],color="lightgray",zorder=-1)
    connect([i,-sz],[i,sz],color="lightgray",zorder=-1)

pts = []
for i in all_with_norm(example_norm):
    pts.append([i.re,i.im])
    
scatter_points(pts)





sz = 10
make_canvas([-sz,sz],[-sz,sz],size=8,show_axes=True,title=f"Gaussian Primes")


connect([-sz,0],[sz,0],color="gray",zorder=0)
connect([0,-sz],[0,sz],color="gray",zorder=0)

for i in range(-sz,sz):
    connect([-sz,i],[sz,i],color="lightgray",zorder=-1)
    connect([i,-sz],[i,sz],color="lightgray",zorder=-1)

pts = []
for i in all_gauss_int():
    if i.norm > 200:
        break
    if is_gauss_prime(i):
        pts.append([i.re,i.im])
    
scatter_points(pts)


