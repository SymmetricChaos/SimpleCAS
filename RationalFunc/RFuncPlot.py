from Rational import rational_seq
from Utility import make_canvas, plot_points, connect
from RationalFunc import RFunc, rfunc_roots


def rfunc_plot(rfunc):
    """Automatically make a plot that shows the rational function well"""

    r = rfunc_roots(rfunc)


#    # Pick the minimum possible axes for the graph
    xlimit = [ min(r), max(r) ]
    ylimit = [ min(r), max(r) ]
    
#    # Choose how much to pad
    xmargin = max(abs(xlimit[0]-xlimit[1])/10,1)
    ymargin = max(abs(ylimit[0]-ylimit[1])/10,1)
    
#    # create the actual axes
    xwidth = [float(xlimit[0]-xmargin), float(xlimit[1]+xmargin)]
    ywidth = [float(ylimit[0]-ymargin), float(ylimit[1]+ymargin)]
    
    
    x = rational_seq(xwidth[0],xwidth[1],.01)
    y = [float(i) for i in rfunc.evaluate(x)]
    for pos,val in enumerate(y):
        if val > ywidth[1]:
            y[pos] = float('NaN')
        if val < ywidth[0]:
            y[pos] = float('NaN')
    x = [float(i) for i in x]
    
    
    pts = [i for i in zip(x,y)]
    make_canvas(xwidth,ywidth,size=[5,5],show_axes=True,title=rfunc.pretty_name)
    plot_points(pts,color="black")
    
    connect([xwidth[0],0],[xwidth[1],0],color="gray",zorder=-1)
    

if __name__ == '__main__':
    from random import sample
    coefs = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
    co1 = sample(coefs,6)
    co2 = sample(coefs,6)
    R = RFunc( co1, co2 )
    print(f"R = {R}")
    
    rfunc_plot(R)