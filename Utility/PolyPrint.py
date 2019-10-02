def poly_print(poly):
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
        val = abs(coe)
        sgn = "-" if coe//val == -1 else "+"
        
        
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
                    s = f" {sgn} x^{pwr}"

            # General case
            else:
                if pwr == 1:
                    s = f" {sgn} {val}x"
                elif pwr == 0:
                    s = f" {sgn} {val}"
                else:
                    s = f" {sgn} {val}x^{pwr}"

        # Handle non-integer coefficients
        else:
            
            if pwr == 1:
                s = f" {sgn} {val.n}/{val.d}x"
            elif pwr == 0:
                s = f" {sgn} {val.n}/{val.d}"
            else:
                s = f" {sgn} {val.n}/{val.d}x^{pwr}"
        
        # Special case of leading coefficient
        if pwr == d:
            s = s.replace(" ","")
            
        out += s
    
    return out



def poly_print_pretty(poly):
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
                    s = f" {sgn} $x$"
                # Special case is term is 1 or -1
                elif pwr == 0:
                    s = f" {sgn} 1"
                # General case
                else:
                    s = f" {sgn} $x^{{{pwr}}}$"

            # General case
            else:
                if pwr == 1:
                    s = f" {sgn} {val}$x$"
                elif pwr == 0:
                    s = f" {sgn} {val}"
                else:
                    s = f" {sgn} {val}$x^{{{pwr}}}$"

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