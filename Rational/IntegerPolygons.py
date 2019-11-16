def integer_polygon(N,side_len):
    """Closest approximations of regular polygons with integer coordinates"""
    
    if N == 3:
        P = [[0,0],[side_len,0]]
        a = (side_len//2)
        c2 = side_len**2
        b = side_len
        while b**2 + a**2 > c2:
            b -= 1
        P.append([a,b])
        return P
    elif N == 4:
        P = [[0,0],
             [side_len,0],
             [side_len,side_len],
             [0,side_len]]
        return P
    elif N == 5:
        P = [[0,0]]
        
    else:
        return None
    
    
if __name__ == '__main__':
    from Utility import make_canvas, plot_points,connect
    
    make_canvas([-1,10],size=6)
    for i in range(1,10):
        pts = integer_polygon(3,i)
        plot_points(pts,color='k')
        connect(pts[0],pts[-1],color='k')