from Utility import make_canvas, scatter_points, show_plot
from Poly import ZPoly
 

def zpoly_points(poly):
    x = [n for n in range(F)]
    y = poly.evaluate(x)
    
    return [i for i in zip(x,y)]


def zpoly_plot(poly,size=[5,5]):
    """Automatically make a plot that shows the roots and critical points of the polynomial"""
    
    F = poly.F
    xwidth = [-1,F+1]
    ywidth = [-1,F+1]

    pts = zpoly_points(poly)
    
    make_canvas(xwidth,ywidth,size=size,show_axes=True,title=f"{poly.pretty_name}   (mod {F})")
    scatter_points(pts)
        
    return pts





if __name__ == '__main__':
    from random import randint
    F = 83
    coefs = [randint(0,F-1) for i in range(5)]
    P = ZPoly( coefs, F )
    print(f"P = {P} (mod {P.F})")
    
    zpoly_plot(P)
    show_plot()
