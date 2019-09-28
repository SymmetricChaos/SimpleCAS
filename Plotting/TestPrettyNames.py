from Rational import rational_seq
from Utility import make_canvas, plot_points, show_plot
from Poly import QPoly
from random import sample

R = rational_seq(-2,2,"1/2")

for i in range(3):
    coefs = sample(R,7)
    print("\n\n",coefs)
    P = QPoly( coefs )
    x = rational_seq(-5,5,".01")
    y = P.evaluate(x)
    
    pts = [i for i in zip(x,y)]
    
    make_canvas([-6,6],show_axes=True,title=P.pretty_name(),size=5)
    
    plot_points(pts)
    show_plot()