from Rational import rational_seq
from Utility import make_canvas, plot_points, scatter_points, connect
from Poly.QPoly import QPoly, RFunc
from Poly.RootApproximation import qpoly_roots, stationary_points, \
                                   inflection_points, rfunc_roots, \
                                   rfunc_asymptotes
from Poly.ZPoly import ZPoly
from Poly.ZPolyPlot import zpoly_plot



def poly_plot(poly,size=[5,5],show_plot=True):
    """Automatically make a plot that shows the roots and critical points of the polynomial"""
    
    
    if type(poly) == ZPoly:
        if poly.M:
            pts = zpoly_plot(poly)
            return pts
        else:
            poly = QPoly(poly.coef)
    
    if type(poly) == QPoly:
        r = qpoly_roots(poly)
        s = stationary_points(poly)
        c = inflection_points(poly)
        
        interesting_points = r + s + c

    elif type(poly) == RFunc:
        r = rfunc_roots(poly)
        a = rfunc_asymptotes(poly)
        
        interesting_points = r + a
    
    else:
        raise TypeError("Input must be QPoly, RFunc, or ZPoly")
        
    
    interesting_values = poly.evaluate(interesting_points)
    
        
    # Pick the minimum possible axes for the graph
    xlimit = [ min(interesting_points), max(interesting_points) ]
    ylimit = [ min(interesting_values), max(interesting_values) ]
    
    # Choose how much to pad
    xmargin = max(abs(xlimit[0]-xlimit[1])/10,1)
    ymargin = max(abs(ylimit[0]-ylimit[1])/10,1)
    
    # create the actual axes
    xwidth = [float(xlimit[0]-xmargin), float(xlimit[1]+xmargin)]
    ywidth = [float(ylimit[0]-ymargin), float(ylimit[1]+ymargin)]
    
    step_size = abs(xwidth[0]-xwidth[1])/100
    x = rational_seq(xwidth[0],xwidth[1],step_size)
    y = [float(i) for i in poly.evaluate(x)]
    x = [float(i) for i in x]
    
    pts = [i for i in zip(x,y)]
    
    if show_plot:
        make_canvas(xwidth,ywidth,size=size,show_axes=True,title=poly.pretty_name)
        plot_points(pts)
        connect([xwidth[0],0],[xwidth[1],0],color="gray",zorder=-1)
        
    return [(a,b) for a,b in zip(x,y)]





if __name__ == '__main__':
    from random import sample, randint
    coefs = [f"{i}/6" for i in range(30)] + [f"-{i}/6" for i in range(30)] + [i for i in range(20)] + [-i for i in range(20)]
    co = sample(coefs,randint(3,7))
    P = QPoly( co )
    print(f"P = {P}")
    
    r = [i for i in qpoly_roots(P)]
    s = [i for i in stationary_points(P)]
    c = [i for i in inflection_points(P)]

    poly_plot(P)
    

    if len(r) > 0:
        rpts = [(i,P(i)) for i in r]
        scatter_points(rpts,zorder=5,color='black')
    
    if len(s) > 0:
        spts = [(i,P(i)) for i in s]
        scatter_points(spts,zorder=5,color='blue')
    
    if len(c) > 0:
        cpts = [(i,P(i)) for i in c]
        scatter_points(cpts,zorder=5,color='red')


    M = 83
    coefs = [randint(0,M-1) for i in range(5)]
    P = ZPoly( coefs, M )
    print(f"P = {P} (mod {P.M})")
    
    poly_plot(P)


    