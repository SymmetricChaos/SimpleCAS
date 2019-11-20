from Poly import ZPoly, zpoly_egcd
import pprint


def finite_field_example(P):


    S = ZPoly( [0,1], P.M )
    out = ZPoly( [1], P.M )
    
    Fnum = {0:P}
    Fpol = {P:0, ZPoly([0],2):0}
    
    elems = (P.M)**(len(P)-1)
    
    for i in range(1,elems):
        if out in Fpol:
            raise Exception("Not a finite field")
        Fnum[i] = out
        Fpol[out] = i
        out = (out * S) % P

    
    print(f"GF({elems})")    
    pprint.pprint(Fnum)
    
    return Fnum,Fpol


def ff_inv(a, R):
    """Modular Multiplicative Inverse"""
    
    a = a % R
    
    g, x, _ = zpoly_egcd(a, R)
    if g != ZPoly([1],a.M):
        raise ValueError(f"Multiplicative inverse of {a} mod {R} does not exist")
    else:
        return x % R
    
    
def ff_div(a,b,R):
    if b == R or str(b) == "0":
        raise ZeroDivisionError
    return (a * ff_inv(b,R)) % R




    
    
    

    
if __name__ == '__main__':
    import random
    
    P = ZPoly( [1,1,0,0,1], 2 )
    P = ZPoly( [1,0,0,1,0,1], 2 )
    Fnum,Fpol = finite_field_example(P)
    
    
    print("\n\nIn a field of characteristic two every element is its own additive inverse.")
    for i in range(3):
        x,y = random.sample(list(Fnum),2)
        z = Fnum[0]
        a = Fnum[x]
        b = Fnum[x]
        print(f"({a}) + ({b}) = {(a+b)%z}")
        print(f"{Fpol[a]} + {Fpol[b]} = {Fpol[(a+b)%z]}")
        print()
    
    print("\n\nCalculate multiplicative inverses.")
    for i in range(3):
        x,y = random.sample(list(Fnum),2)
        z = Fnum[0]
        a = Fnum[x]
        if str(a%z) == "0":
            continue
        print(f"({a}) * ({ff_inv(a,z)}) = {a*ff_inv(a,z)%z}")

        print()
        
    print("\n\nExamples of Division over the Finite Field")
    for i in range(3):
        x,y = random.sample(list(Fnum),2)
        z = Fnum[0]
        a = Fnum[x]
        b = Fnum[y]
        if str(b%z) == "0":
            continue
        print(f"({a}) / ({b}) = {ff_div(a,b,z)}")
#        print(f"{Fpol[a]} // {Fpol[b]} = {Fpol[(a//b)%z]}")
        print()

#    print("\n\n")
#    for i in range(3):
#        x,y = random.sample(list(Fnum),2)
#        z = Fnum[0]
#        a = Fnum[x]
#        b = Fnum[y]
#        print(f"({a}) * ({b}) = {(a*b)%z}")
#        print(f"{Fpol[a]} * {Fpol[b]} = {Fpol[(a*b)%z]}")
#        print()
#    
