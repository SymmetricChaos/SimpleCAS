def integer_triangle(side_len):
    """Closest approximations of regular polygons with integer coordinates"""
    
    P = [[0,0],[side_len,0]]
    a = (side_len//2)
    c2 = side_len**2
    b = side_len
    while b**2 + a**2 > c2:
        b -= 1
    P.append([a,b])
    return P

    
def integer_octagon():
    a = 5
    b = 7
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
    
    make_canvas([-1,10],size=6)
    for i in range(1,10):
        pts = integer_triangle(i)
        plot_points(pts,color='k')
        connect(pts[0],pts[-1],color='k')
        
    make_canvas([-10,18],[-4,24],size=6)
    pts = integer_octagon()
    print(pts)
    plot_points(pts,color='k')
    connect(pts[0],pts[-1],color='k')