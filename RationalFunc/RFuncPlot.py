from Rational import rational_seq
from Utility import make_canvas, plot_points, connect
from RationalFunc import RFunc, rfunc_roots
from Poly import qpoly_roots


def rfunc_plot(rfunc):
    """Automatically make a plot that shows the rational function well"""

    r = [0] + rfunc_roots(rfunc) + qpoly_roots(rfunc.D)


    # Pick the minimum possible axes for the graph
    xlimit = [ min(r), max(r) ]
    ylimit = [ min(r), max(r) ]
    
    # Choose how much to pad
    xmargin = max(abs(xlimit[0]-xlimit[1])/10,1)
    ymargin = max(abs(ylimit[0]-ylimit[1])/10,1)
    
    # create the actual axes
    xwidth = [float(xlimit[0]-xmargin), float(xlimit[1]+xmargin)]
    ywidth = [float(ylimit[0]-ymargin), float(ylimit[1]+ymargin)]
#    xwidth = [-10,10]
#    ywidth = [-10,10]
    
    
    # Need to identify points outside the plot then change everything except
    # points on the edge of that sequence of float('NaN') so the asymptote
    # isn't drawn.
    
    step_size = abs(xwidth[0]-xwidth[1])/200
    x = rational_seq(xwidth[0],xwidth[1],step_size)
    y = [float(i) for i in rfunc.evaluate(x)]
    x = [float(i) for i in x]
    
    asymptotes = qpoly_roots(rfunc.D)
    
    if asymptotes:
        x += [float(i) for i in asymptotes]
        y += [float('NaN')]*len(asymptotes)
    
    pts = [i for i in zip(x,y)]
    
    pts = sorted(pts, key=lambda tup: tup[0])
    make_canvas(xwidth,ywidth,size=[5,5],show_axes=True,title=rfunc.pretty_name)
    plot_points(pts)
    
    connect([xwidth[0],0],[xwidth[1],0],color="gray",zorder=-1)
    
    return pts





if __name__ == '__main__':
    from random import sample
    coefs = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
    co1 = sample(coefs,4)
    co2 = sample(coefs,4)
    R = RFunc( co1, co2 )
#    R = RFunc( [-4,0,2], [-1,-5] )
    print(f"R = {R}")
    print("Roots:",[r.digits(3) for r in rfunc_roots(R)])
    print("VertA:",qpoly_roots(R.D))
    pts = rfunc_plot(R)
    
    
    