![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/simpleCASlogo.png "SimpleCAS")


SimpleCAS is a computer algebra library that works with rational numbers and univariate polynomials which is meant to be simple enough (and hopefully written clearly enough) that a curious person can take it apart in order to understand how it works. It is written almost entirely in base Python so that even the most basic parts can be seen. In particular the standard library modules `math`, `fractions`, and `decimal` are not used.

For the love of common sense don't use SimpleCAS for anything remotely important. Its quite slow and, despite my best efforts, I can't guarantee it is always accurate. Also it does not currently provide symbolic calculation of roots for any polynomials.



# Features
Currently four kinds of objects are supported by SimpleCAS:

## Rational
Rational numbers represented in simplest form. They are essentially just a pair of numbers with a bunch of methods defined to make sure they interact with other Rational objects as well as Python's integers.

```
R = Rational(34,18)
S = Rational(8,1)
print(R)
17/9
print(S)
8
print(R+S)
89/9
```

Rationals can be expanded into several forms.

```
R = Rational(137,126)

# String showing the first n digits after the decimal
print(R.digits(5)) 
1.08730

# String showing the complete decimal expansion with the repeating part parenthesized
print(R.decimal_expansion)  
1.0(873015)

# List with the canonical simple continued fraction
print(R.cfrac())
[3, 2, 1, 3]
```

The continued fraction representation is useful for "rounding" rational numbers by finding the best rational approximation with a denominator no greater than a certain value. Note that this method uses semi-convergents and so it will actually *the* best approximation rather than simply *a* best approximation.

```
R = Rational(392699,125000)
print(rational_round(R,100))
311/99
```

Since writing out a `Rational(Numerator,Denominator)` can be inconvenient every time the `cast_to_rational` function is provided which accepts integers and properly formatted strings as well as floating point numbers.

```
print(cast_to_rational(12))
12

print(cast_to_rational("45/12"))
15/4

print(cast_to_rational("12.95"))
259/20

print(cast_to_rational("-.71(010)"))
-70939/999

print(cast_to_rational(45.13))
4513/100
```

While giving floats to `cast_to_rational` is allowed it is not recommended. Floating point numbers are finite length binary approximations of some real number so the results may not be the same as expected. The method used also relies on how Python converts floating point numbers to strings so it is dependent on any settings that influence that.

```
print(cast_to_rational(1/3))
3333333333333333/10000000000000000
```

## QPoly
Univariate polynomials with rational coefficients. Internally these are simple to represent as a list with the term of degree 0 in position 0, the term of degree 1 in position 1, and so on. This makes indexing the polynomial when working with it in Python intuitive but its not how we generally write polynomials in order to read them. When a QPoly object is printed it will show the standard written form with terms in descending order.

```
P = QPoly( [2,3,1,0,-11] )
print(P)
-11x^4 + x^2 + 3x + 2
```

Because the coefficients are automatically passed through `cast_to_rational` it is easy to create polynomials with non-integer coefficients, though keep in mind the warnings about using floating point numbers from above.

```
P = QPoly( ["-1.3",3,"9/5",0,-1] )
print(P)
-x^4 + 9/5x^2 + 3x - 13/10
```

Naturally QPoly will interact with most mathematical operations. Addition, subtraction, and multiplication are defined with any QPoly, Rational, or Integer. Exponentiation is defined for non-negative integers. Since polynomials form a ring but not a field true division does not produce a QPoly, instead it returns an RFunc object. Euclidean division of polynomials takes the place of the floored division operation (in many cases this is preferred since it always returns a polynomial). The modulus operator returns the remainder.

The derivative and integral of the polynomials are avaible through the `.derivative()` and `.integral()` methods.

But wait, there's more! The standard written form is fine for text but it looks ugly in places where more complex formatting is expected. To that end the `pretty_name` property gives a LaTeX formated version of the polynomial.

```
print(P.pretty_name)
$−x^{4}\;+\;\dfrac{9x^{2}}{5}\;+\;3x\;−\;\dfrac{13}{10}$
```

It looks pretty horrendous just written out like that but lets try it with the `poly_plot` function which attempts to find the "interesting" part of the polynomial based on where the roots and stationary points are.

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/poly_example_1.png "polynomial")

Rational approximations of the locations of where certain special points are given by the `qpoly_roots`, `stationary_points`, and `inflection_points` functions. Fineness of the approximation is adjustable.


## RFunc
Rational functions are quotients of polynomials represented in simplest form. Unfortunately rational functions are not generally as well behaved as polynomials are so there isn't quite as much support for them.

An RFunc object can be created in must the same way QPoly except that there are two lists rather than just one. These lists are automatically concerted to QPoly objects and then their common factors are divided out.

```
R = RFunc( [-28,16,-16,16,12], [-2,5,-6,6,-4,1] )
print(R)
(12x + 28) / (x^2 - 3x + 2)
```

Making a picture of the "interesting" part of rational function is rather difficult. Given that Wolfram Alpha struggles to do this don't expect anything particularly pretty here. The LaTeX formatted names look nice, though.

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/rfunc_example.png "rational function")


## ZPoly
Polynomials with integer coefficients that obey [modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic) for all operations. Equivalently the coefficients are drawn from some cyclic group Z/nZ. A ZPoly object can be created in the same ways as as QPoly except that the coefficients must be integers and the order of the cyclic group must also be specified. If the coefficients provided are not members of the cyclic group specified then they are reduced modulo the order of the group so that they will fit.

```
P = ZPoly( [18,0,-8,121,9], 27 )
print(P)
9x^4 + 13x^3 + 19x^2 + 18
```

Note that when printed ZPoly does *not* include an indication that it is different from QPoly such as `(mod n)` since this is often inconvenient. The `zpoly_plot` function will draw the entire polynomial and include a nicely formatted name with the modulus included.

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/ZPolyExample.png "polynomial over GF(83)")

It is often useful for the order of the group to be a prime or prime power so that the group can also be treated as a finite field but this isn't required.


# Planned Expansions
Currently there are plans for a few additions to the system. Power series already have a tiny bit of support as the PSeries object. Combiner objects for QPoly have some support so that sums and products of QPoly can be represented.

# Not Planned
## Multivariate Polynomials
Multivariate polynomials would, to my knowledge, require fundamentally redesigning the logic of how the system treats polynomials to be vastly more complex. Because the simplicity of the QPoly object is central to making SimpleCAS easy to understand there are no plans to include multivariate polynomials in SimpleCAS.

## Radicals and Logarithms
Can't figure out a good way to generally handle these.
