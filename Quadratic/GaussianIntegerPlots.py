from Quadratic.GaussianIntegers import GaussInt, all_with_norm
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



print(f"\n\nAll Gaussian Integer with Norm {example_norm}")
pts = []
for i in all_with_norm(example_norm):
    pts.append([i.re,i.im])
    
scatter_points(pts)