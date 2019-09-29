from Rational import rational_seq
from Utility import make_canvas, plot_points, show_plot
from Poly import QPoly
from random import sample

R = rational_seq(-3,3,"1/4")

for i in range(5):
    coefs = sample(R,7)
    P = QPoly( coefs )
    x = rational_seq(-5,5,".01")
    y = P.evaluate(x)
    
    pts = [i for i in zip(x,y)]
    
    make_canvas([-6,6],show_axes=True,title=P.pretty_name(),size=5)
    
    
    
    print("\n\n",coefs)
    print("\n",P)
    print("\n",P.pretty_name())
    plot_points(pts)
    show_plot()