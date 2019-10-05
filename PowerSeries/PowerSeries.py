from Rational import coerce_to_rational


class PSeries:
    
    def __init__(self,a,c=0):
        try: 
            iter(a)
        except:
            raise Exception(f"{a} is not iterable")
        self.a = a
        self.c = coerce_to_rational(c)
        
if __name__ == '__main__':
    P = PSeries([5,6,5,5,6],4)
    print(P.a)
    print(P.c)