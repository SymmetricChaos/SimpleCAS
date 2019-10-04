from Rational import rational_seq
from Utility import make_canvas, plot_points, connect
from Poly import QPoly, all_roots, critical_points
from random import randint

def poly_plot(poly):
    
    
    r = all_roots(poly)
    c = critical_points(poly)
    
    interesting_points = r + c
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
    
    
    x = rational_seq(xwidth[0],xwidth[1],.05)
    y = [float(i) for i in P.evaluate(x)]
    x = [float(i) for i in x]
    
    
    pts = [i for i in zip(x,y)]
    make_canvas(xwidth,ywidth,size=[5,5],show_axes=True,title=P.pretty_name())
    plot_points(pts,color="black")
    
    connect([xwidth[0],0],[xwidth[1],0],color="gray",zorder=-1)
    

if __name__ == '__main__':
    co = [randint(-9,9) for i in range(7)]
    P = QPoly( co )
    print(f"P = {P}")
    
    r = [round(float(i),3) for i in all_roots(P)]
    c = [round(float(i),3) for i in critical_points(P)]

    poly_plot(P)
    
    print(sorted(r))
    print(sorted(c))