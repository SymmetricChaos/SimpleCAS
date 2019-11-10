from Utility import make_canvas, scatter_points
 

def zpoly_points(poly):
    x = [n for n in range(poly.M)]
    y = poly.evaluate(x)
    
    return [i for i in zip(x,y)]


def zpoly_plot(poly,size=[5,5]):
    """Automatically make a plot that shows the roots and critical points of the polynomial"""
        
    M = poly.M
    xwidth = [-1,M+1]
    ywidth = [-1,M+1]

    pts = zpoly_points(poly)
    
    make_canvas(xwidth,ywidth,size=size,show_axes=True,title=poly.pretty_name)
    scatter_points(pts)
        
    return pts