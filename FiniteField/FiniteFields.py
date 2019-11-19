from Poly.ZPoly import ZPoly
import pprint



# work in division, gcd for polynomials

def finite_field_example():
    print("GF(16)")

    
    P = ZPoly( [1,1,0,0,1], 2 )
    S = ZPoly( [0,1], 2 )
    out = ZPoly( [1], 2 )
    
    Fnum = {0:P}
    Fpol = {P:0, ZPoly([0],2):0}
    
    for i in range(1,16):
        Fnum[i] = out
        Fpol[out] = i
        out = (out * S) % P
        
    pprint.pprint(Fnum)
    
    return Fnum,Fpol



    
if __name__ == '__main__':
    import random
    Fnum,Fpol = finite_field_example()
    
    print()
    for i in range(5):
        x,y = random.sample(list(Fnum),2)
        z = Fnum[0]
        a = Fnum[x]
        b = Fnum[y]
        print(f"({a}) * ({b}) = {(a*b)%z}")
        print(f"{Fpol[a]} * {Fpol[b]} = {Fpol[(a*b)%z]}")
        print()
        print()

    for i in range(5):
        x,y = random.sample(list(Fnum),2)
        z = Fnum[0]
        a = Fnum[x]
        b = Fnum[y]
        print(f"({a}) // ({b}) = {(a//b)%z}")
        print(f"{Fpol[a]} // {Fpol[b]} = {Fpol[(a//b)%z]}")
        print()