from Rational import rational_seq
from Utility import make_canvas, plot_points, show_plot
from Poly import QPoly
from random import sample

R = [0,0,0,0,2,10,"1/2","15/7","5/11","9/4"]

for i in range(5):
    coefs = sample(R,5)
    P = QPoly( coefs )
    x = rational_seq(-5,5,".01")
    y = P.evaluate(x)
    
    pts = [i for i in zip(x,y)]
    
    make_canvas([-6,6],show_axes=True,title=P.pretty_name(),size=5)
    
    
    
    print("\n\n",P.coef)
    print("\n",P)
    print("\n",P.pretty_name())
    plot_points(pts)
    show_plot()