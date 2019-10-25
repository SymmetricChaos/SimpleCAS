from Utility import make_canvas, scatter_points, show_plot
from Poly import ZPoly
 

def zpoly_plot(poly,size=[5,5],show_plot=True):
    """Automatically make a plot that shows the roots and critical points of the polynomial"""
    
    F = poly.F
    xwidth = [-1,F+1]
    ywidth = [-1,F+1]

    x = [n for n in range(F)]
    y = [i for i in poly.evaluate(x)]
    
    pts = [i for i in zip(x,y)]
    
    if show_plot:
        make_canvas(xwidth,ywidth,size=size,show_axes=True,title=f"{poly.pretty_name}   (mod {F})")
        scatter_points(pts)
        

    return pts





if __name__ == '__main__':
    from random import randint
    F = 83
    coefs = [randint(0,F-1) for i in range(5)]
    P = ZPoly( coefs, F )
    print(f"P = {P} (mod {P.F})")
    
    pts = zpoly_plot(P)
    show_plot()
#    print()
#    for i in pts:
#        print(i)
    