from RationalFunction import RationalFunc

# TODO find asymptotes of a rational function
def asymptote(rfunc):
    assert type(rfunc) == RationalFunc
    dN = rfunc.N.degree()
    dD = rfunc.D.degree()
    
    if dN > dD:
        pass
    elif dN == dD:
        pass
    elif dN < dD:
        pass
    
if __name__ == '__main__':
    R = RationalFunc( [3,1,6,4] , [7,9,5,3] )