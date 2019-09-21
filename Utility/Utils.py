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


def poly_normalize(P):
    while P[-1] == 0 and len(P) > 1:
        if len(P) == 1:
            break
        P.pop()


def poly_pad(P,n):
    out = P.copy()
    while len(out) < n:
        out.append(0)
    return out
	
def poly_add(P, Q):
        
    pad = max(len(P),len(Q))
    
    P = poly_pad(P,pad)
    Q = poly_pad(Q,pad)
    
    out = []
    
    for x,y in zip(P,Q):
        out.append( x+y )

    poly_normalize(out)

    return out


def poly_mult(P, Q):
    
    out = [0]*(len(P)+len(Q))
    
    for i in range(len(P)):
        for j in range(len(Q)):
            out[i+j] += P[i]*Q[j]
            out[i+j] = out[i+j]

    
    poly_normalize(out)

    return out

	
def poly_print(poly,pretty=False):
    """Show the polynomial in descending form as it would be written"""
        
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
                
        # When the coefficient is 1 or -1 don't print it unless it is the
        # coefficient for x^0
        if val == 1 and pwr != 0:
            val = ""
  
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
                if pretty == False:
                    s = f"{sgn}{val}x^{pwr}"
                else:
                    s = f"{sgn}{val}x$^{{{pwr}}}$"
                    
        
        # If the power is 1 just show x rather than x^1
        elif pwr == 1:
            s = f" {sgn} {val}x"
        
        # If the power is 0 only show the sign and value
        elif pwr == 0:
            s = f" {sgn} {val}"
        
        # Otherwise show everything
        else:
            if pretty == False:
                s = f" {sgn} {val}x^{pwr}"
            else:
                s = f" {sgn} {val}x$^{{{pwr}}}$"
        out += s
    return out