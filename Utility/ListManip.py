def lists_to_tuples(*args):
    """Convert lists to a list of tuples"""
    L = []
    for i in zip(*args):
        L.append(i)
    return L


def tuples_to_lists(L):
    """Convert a list of tuples to lists"""
    out = []
    W = len(L[0])
    for w in range(W):
        out.append( [i[w] for i in L] )
    return out

