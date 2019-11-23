def integer_triangle(side_len):

    P = [[0,0],[side_len,0]]
    a = (side_len//2)
    c2 = side_len**2
    b = side_len
    while b**2 + a**2 > c2:
        b -= 1
    P.append([a,b])
    return P

    
def integer_octagon(n):
    """Closest approximations of regular octagon with integer coordinates for vertices"""
    
    a = 5
    b = 7
    a0,a1 = 1,2
    b0,b1 = 1,3
    
    for i in range(n):
        a0, a1 = a1, 2*a0+a1
        b0, b1 = b1, 2*b0+b1
    
    a = a0
    b = b0
    
    P = [ [0,0] ]
    old = [0,0]
    for x,y in [(a*2,0),
              (b,b),
              (0,a*2),
              (-b,b),
              (-a*2,0),
              (-b,-b),
              (0,-2*a)]:
        new = [old[0]+x,old[1]+y]
        P.append(new)
        old = new
    
    return P
    
if __name__ == '__main__':
    from Utility import make_canvas, plot_points,connect


    make_canvas([-10,10],size=6,show_axes=False)
    for xy in range(-10,11):
        connect([-10,xy],[10,xy],color='gray',linewidth=.5)
        connect([xy,-10],[xy,10],color='gray',linewidth=.5)
    
    
    for i in range(3):
        pts = integer_octagon(i)
        
        # Shift to center
        x_mn = sum([i[0] for i in pts])/8
        y_mn = sum([i[1] for i in pts])/8
        pts = [[x-x_mn,y-y_mn] for x,y in pts]
        
        plot_points(pts,color='k')
        connect(pts[0],pts[-1],color='k')