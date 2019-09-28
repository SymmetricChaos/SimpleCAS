import matplotlib.pyplot as plt
import matplotlib.lines as lines
from Utility.ListManip import tuples_to_lists

def make_canvas(x,y=None,size=None,show_axes=True,title=""):
    # If y is not provided make the y-axis the same as the x
    if not y:
        y = x
    # If only a single value is given for size assume it is a square
    if type(size) == int or type(size) == float:
        size = [size,size]
    # If size is not provided take a guess as a good square size
    elif not size:
        xlim = abs(x[0]-x[1])
        ylim = abs(y[0]-y[1])
        xco = min(xlim,ylim)/xlim
        yco = min(xlim,ylim)/ylim
        size = [xco*9,yco*9]
    fig = plt.figure()
    fig.set_size_inches(size[0], size[1])
    ax = plt.axes(xlim=x, ylim=y)
    if show_axes == False:
        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.title(title)
    return fig, ax


def plot_points(P,**kwargs):
    x,y = tuples_to_lists(P)
    plt.plot(x,y,**kwargs)
    
def scatter_points(P,**kwargs):
    x,y = tuples_to_lists(P)
    plt.scatter(x,y,**kwargs)
    
def connect(A,B,**kwargs):
    ax = plt.gca()
    line = lines.Line2D([A[0],B[0]], [A[1],B[1]], axes=ax,**kwargs)
    ax.add_line(line)