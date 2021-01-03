def inds_where(L,val):
    """All indices of list L that equal val"""
    return [i for i in range(len(L)) if L[i] == val]


def first_where(L,val):
    """First index of list L that equals val"""
    for pos,l in enumerate(L):
        if l == val:
            return pos
    return None


def sort_by_nth(L,n,func=None):
    if func == None:
        f = lambda x: x[n]
        return sorted(L,key=f)
    else:
        f = lambda x: func(x[n])
        return sorted(L,key=f)





def poly_normalize(P):
    """Remove trailing zeroes"""
    while P[-1] == 0 and len(P) > 1:
        if len(P) == 1:
            break
        P.pop()


def poly_pad(P,n):
    """Add trailing zeroes"""
    out = P.copy()
    while len(out) < n:
        out.append(0)
    return out


def poly_add(P, Q):
    """Take list of polynomial coefficients and add them"""
        
    pad = max(len(P),len(Q))
    
    P = poly_pad(P,pad)
    Q = poly_pad(Q,pad)
    
    out = []
    
    for x,y in zip(P,Q):
        out.append( x+y )

    poly_normalize(out)

    return out


def poly_mult(P, Q):
    """Take list of polynomial coefficients and multiply them"""
    
    out = [0]*(len(P)+len(Q))
    
    for i in range(len(P)):
        for j in range(len(Q)):
            out[i+j] += P[i]*Q[j]
            out[i+j] = out[i+j]

    
    poly_normalize(out)

    return out



def unit_test(minitests):
    err_ctr = 0
    err_loc = []
    for pos,test in enumerate(minitests):
        if str(test[0]) != test[1]:
            err_ctr += 1
            err_loc.append(pos)
        
        
    if err_ctr == 0:
        print(f"All {len(minitests)} tests passed")
    else:
        print(f"Total Errors: {err_ctr}\n")
        if err_loc:
            for i in err_loc:
                print(f"Error in test {i}")
                print(f"{minitests[i][0]} should be {minitests[i][1]}\n")