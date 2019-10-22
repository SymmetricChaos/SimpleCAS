def zpoly_print(poly):
    """Show the polynomial in descending form with commandline formatting"""

        
    # Get the degree of the polynomial in case it is in non-normal form
    d = poly.degree()
    
    if d == -1:
        return "0"
    if d == 0:
        return str(poly.coef[0])

    out = ""
    
    # Step through the ascending list of coefficients backward
    # We do this because polynomials are usually written in descending order
    for pwr in range(d,-1,-1):
        
        
        # Skip the zero coefficients entirely
        if poly[pwr] == 0:
            continue
        
        coe = poly[pwr]            
        
        # Handle integer coefficients

        # Handle the special case of coefficient 1 or -1
        if coe == 1:
            
            # Special case if term is x or -x
            if pwr == 1:
                s = f" + x"
            # Special case is term is 1 or -1
            elif pwr == 0:
                s = f" + 1"
            # General case
            else:
                s = f" + x^{pwr}"

        # General case
        else:
            if pwr == 1:
                s = f" + {coe}x"
            elif pwr == 0:
                s = f" + {coe}"
            else:
                s = f" + {coe}x^{pwr}"
        
        if pwr == d:
            s = s[3:]
        
        out += s
    
    return out# + f" (mod {poly.F})"


def zpoly_print_pretty(poly):
    """Show the polynomial in descending form with LaTeX formatting"""

        
    # Get the degree of the polynomial in case it is in non-normal form
    d = poly.degree()
    
    if d == -1:
        return "0"
    if d == 0:
        return str(poly.coef[0])

    out = ""
    
    # Step through the ascending list of coefficients backward
    # We do this because polynomials are usually written in descending order
    for pwr in range(d,-1,-1):
        
        
        # Skip the zero coefficients entirely
        if poly[pwr] == 0:
            continue
        
        
        # Skip the zero coefficients entirely
        if poly[pwr] == 0:
            continue
        
        coe = poly[pwr]            
        
        # Handle integer coefficients

        # Handle the special case of coefficient 1 or -1
        if coe == 1:
            
            # Special case if term is x or -x
            if pwr == 1:
                s = f" + x"
            # Special case is term is 1 or -1
            elif pwr == 0:
                s = f" + 1"
            # General case
            else:
                s = f" + x^{{{pwr}}}"

        # General case
        else:
            if pwr == 1:
                s = f" + {coe}x"
            elif pwr == 0:
                s = f" + {coe}"
            else:
                s = f" + {coe}x^{{{pwr}}}"
        
        if pwr == d:
            s = s[3:]
        else:
            s = s.replace(" ","\;")
            
        out += s
    
    return f"${out}$"