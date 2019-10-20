![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/simpleCASlogo.png "SimpleCAS")


SimpleCAS is a computer algebra library that works with rational numbers and univariate polynomials which is meant to be simple enough (and hopefully written clearly enough) that a curious person can take it apart in order to understand how it works. It is written almost entirely in base Python so that even the most basic parts can be seen. In particular the standard library modules `math`, `fractions`, and `decimal` are not used.

For the love of common sense don't use SimpleCAS for anything remotely important. Its quite slow and, despite my best efforts, I can't guarantee it is always accurate. Also it does not currently provide symbolic calculation of roots for any polynomials.



# Features
Currently three kinds of objects are supported by SimpleCAS:

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

For most purposes creating Rational objects directly is rather cumbersome but also unnecessary. For convenience there is a `cast_to_rational` function provided that will try to create a Rational object from integers, floats, and properly formatted strings. This is used automatically by every function that accepts Rationals as an argument.

Rationals can be expanded into several forms.

```
R = Rational(137,126)

#String showing the first n digits after the decimals
print(R.digits(5)) 
1.08730

# String showing the complete decimal expansion with the repeating part parenthesized
print(R.decimal_expansion)  
1.0(873015)

# List with the canonical simple continued fraction
print(R.cfrac())
[3, 2, 1, 3]
```

The continued fraction representation is useful for "rounding" rational numbers by finding the best rational approximation with a denominator no greater than a certain value.

```
R = Rational(392699,125000)
print(rational_round(R,100))
311/99
```

## QPoly
Univariate polynomials with rational coefficients. Internally these are simple to represent as a list with the term of degree 0 in position 0, the term of degree 1 in position 1, and so on. This makes indexing the polynomial when working with it in Python intuitive but its not how we generally write polynomials in order to read them. When a QPoly object is printed it will show the standard written form with terms in descending order.

```
P = QPoly( [2,3,1,0,-11] )
print(P)
-11x^4 + x^2 + 3x + 2
```

Because the coefficients are automatically passed through `cast_to_rational` it is easy to create polynomials with non-integer coefficients.

```
P = QPoly( ["-1.3",3,"9/5",0,-1] )
print(P)
-x^4 + 9/5x^2 + 3x - 13/10
```

Naturally QPoly will interact with most mathematical operations. Addition, subtraction, and multiplication are defined with any QPoly, Rational, or Integer. Exponentiation is defined for non-negative integers. Since polynomials form a ring but not a field true division does not produce a QPoly, instead it returns an RFunc object. Euclidean division of polynomials takes the place of the floored division operation (in many cases this is preferred since it always returns a polynomial).

But wait, there's more! The standard written form is fine for text but it looks ugly in places where more complex formatting is expected. To that end the `pretty_name` property gives a LaTeX formated version of the polynomial.

```
print(P.pretty_name)
$−x^{4}\;+\;\dfrac{9x^{2}}{5}\;+\;3x\;−\;\dfrac{13}{10}$
```

It looks pretty horrendous just written out like that but lets try it with the `poly_plot()` function which attempts to find the "interesting" part of the polynomial based on where the roots and stationary points are.

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/poly_example_1.png "polynomial")

Rational approximations of the locations of where certain special points are given by `qpoly_roots()`, `stationary_points()`, and `inflection_points()`. Fineness of the approximation is adjustable.


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


# Planned Expansions
Currently there are plans for a few additions to the system. Power series already have a tiny bit of support as the PSeries object. Polynomials with integer coefficient reduced modulo some integer used to be included as ZPoly but were removed to focus on the correctness of QPoly, they will be reintroduced at some point.



# Not Planned
## Multivariate Polynomials
Multivariate polynomials would, to my knowledge, require fundamentally redesigning the logic of how the system treats polynomials to be vastly more complex. Because the simplicity of the QPoly object is central to making SimpleCAS easy to understand there are no plans to include multivariate polynomials in SimpleCAS.

## Radicals and Logarithms
Can't figure out a good way to generally handle these.
