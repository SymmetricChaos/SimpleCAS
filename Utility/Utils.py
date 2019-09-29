def egcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

		
def gcd(*args):
    """Greatest Common Denominator"""

    # Handle the case that a list is provided
    if len(args) == 1 and type(args[0]) is list:
        return gcd(*args[0])
    
    # the gcd of a number with itself is iself
    if len(args) == 1:
        return args[0]
    
    # calculate gcd for two numbers
    if len(args) == 2:
        a = args[0]
        b = args[1]
        g,x,y = egcd(a,b)
        return g
    
    # if more than two break it up recursively
    a = gcd(*args[0:2])
    b = gcd(*args[2:])
    return gcd(a,b)

	
def lcm(*args):
    """Least Common Multiple"""
    
    # Handle the case that a list is provided
    if len(args) == 1 and type(args[0]) is list:
        return lcm(*args[0])
    
    # the lcm of a number with itself is iself
    if len(args) == 1:
        return args[0]
    
    # calculate lcm for two numbers
    if len(args) == 2:
        a = args[0]
        b = args[1]
        g,x,y = egcd(a,b)
        return abs(a*b)//g
    
    # if more than two break it up recursively
    a = lcm(*args[0:2])
    b = lcm(*args[2:])
    return lcm(a,b)





def inds_where(L,val):
    return [i for i in range(len(L)) if L[i] == val]


def first_where(L,val):
    for pos,l in enumerate(L):
        if l == val:
            return pos
    return None
     




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

	
def poly_print(poly,pretty=False):
    """Show the polynomial in descending form with commandline formatting"""

        
    # Get the degree of the polynomial in case it is in non-normal form
    d = poly.degree()
    
    if d == -1:
        return f"0"

    out = ""
    
    # Step through the ascending list of coefficients backward
    # We do this because polynomials are usually written in descending order
    for pwr in range(d,-1,-1):
        
        # Skip the zero coefficients entirely
        if poly[pwr] == 0:
            continue
        
        coe = poly[pwr]
        val = abs(coe)
        sgn = "-" if coe//val == -1 else "+"
        
        # Handle sign for leading term
        if pwr == d and sgn == "+":
            sgn = ""
            
                
        # When the coefficient is 1 or -1 don't print it unless it is the
        # coefficient for x^0
        if val == 1 and pwr != 0:

            if pwr == d:
                if sgn == "+":
                    sgn = ""
                
                # Handle powers of 1 or 0 that appear as the first term
                if pwr == 1:
                    s = f"{sgn}x"
                else:
                    s = f" {sgn}x^{pwr}"

                            
            
            # If the power is 1 just show x rather than x^1
            elif pwr == 1:
                s = f" {sgn} x"
            
            # If the power is 0 only show the sign and value
            elif pwr == 0:
                s = f" {sgn} x"
            
            # Otherwise show everything
            else:
                s = f" {sgn} x^{pwr}"
            out += s
    
        else:
    
            # If it is the first term include the sign of the coefficient
            if pwr == d:
                if sgn == "+":
                    sgn = ""
                
                # Handle powers of 1 or 0 that appear as the first term
                if pwr == 1:
                    s = f"{sgn}{val}x"
                elif pwr == 0:
                    s = f"{sgn}{val}"
                else:
                    s = f" {sgn}{val}x^{pwr}"

                            
            
            # If the power is 1 just show x rather than x^1
            elif pwr == 1:
                s = f" {sgn} {val}x"
            
            # If the power is 0 only show the sign and value
            elif pwr == 0:
                s = f" {sgn} {val}"
            
            # Otherwise show everything
            else:
                s = f" {sgn} {val}x^{pwr}"

            out += s
    
    return out



def poly_print_pretty(poly):
    """Show the polynomial in descending form with LaTeX formatting"""

        
    # Get the degree of the polynomial in case it is in non-normal form
    d = poly.degree()
    
    if d == -1:
        return f"0"

    out = ""
    
    # Step through the ascending list of coefficients backward
    # We do this because polynomials are usually written in descending order
    for pwr in range(d,-1,-1):
        
        
        # Skip the zero coefficients entirely
        if poly[pwr] == 0:
            continue
        
        
        coe = poly[pwr]
        val = abs(coe)
        sgn = u"\u2212" if coe//val == -1 else "+" #U+2212 is the large minus
        
        
        # Handle sign for leading term
        if pwr == d and sgn == "+":
            sgn = ""
            
        
        # Handle integer coefficients
        if val.d == 1:
            
            # Handle the special case of coefficient 1 or -1
            if val.n == 1:
                
                # Special case if term is x or -x
                if pwr == 1:
                    s = f" {sgn} x"
                # Special case is term is 1 or -1
                elif pwr == 0:
                    s = f" {sgn} 1"
                # General case
                else:
                    s = f" {sgn} x$^{{{pwr}}}$"

            # General case
            else:
                if pwr == 1:
                    s = f" {sgn} {val}x"
                elif pwr == 0:
                    s = f" {sgn} {val}"
                else:
                    s = f" {sgn} {val}x$^{{{pwr}}}$"

        # Handle non-integer coefficients
        else:
            
            # Handle special case of numerator 1
            if val.n == 1:
                
                # Special case of term x/d
                if pwr == 1:
                    s = f" {sgn} $\dfrac{{x}}{{{val.d}}}$"
                # Special case of term n/d
                elif pwr == 0:
                    s = f" {sgn} $\dfrac{{{val.n}}}{{{val.d}}}$"
                # General case
                else:
                    s = f" {sgn} $\dfrac{{x^{{{pwr}}}}}{{{val.d}}}$"
                
            # General case
            else:
                if pwr == 1:
                    s = f" {sgn} $\dfrac{{{val.n}x}}{{{val.d}}}$"
                elif pwr == 0:
                    s = f" {sgn} $\dfrac{{{val.n}}}{{{val.d}}}$"
                else:
                    s = f" {sgn} $\dfrac{{{val.n}x^{{{pwr}}}}}{{{val.d}}}$"
        
        # Special case of leading coefficient
        if pwr == d:
            s = s.replace(" ","")
            
        out += s
    
    return out


def estimate_root(x):
    """Crude Estimate for Square Root"""
    return x // (10**(len(str(x))//2))


def int_root(x):
    """Integer Square Root"""
    
    a = estimate_root(x)
    
    if a == 0:
        return 0
    
    b = (a+(x//a))//2
    
    t = [(a,b)]
    
    while True:
        if b == 0:
            break
        a, b = b, (b+(x//b))//2
        if (a,b) in t:
            break
        t.append((a,b))
    
    # Sometimes b is too large when we reach a stopping point, this fixes that
    if b**2 > x:
        return b-1
    return b


def factorization(n,negatives=False):
    """All Unique Factors"""
    if type(n) != int:
        raise Exception("n must be an integer") 
    
    if n == 0:
        return [0]
    
    lim = int_root(n)+1
    
    if negatives == True:
        L = [1,-1,n,-n]
    else:
        L = [1,n]
    
    for i in range(2,lim):
        f,r = divmod(n,i)
        if f == 0 or i == 0:
            print(n)
        if r == 0:
            if negatives == True:
                L += [i,-i,f,-f]
            else:
                L += [i,f]
            
    L = list(set(L))
    L.sort()
    
    return L