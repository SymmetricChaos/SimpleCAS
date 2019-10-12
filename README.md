![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/simpleCASlogo.png "SimpleCAS")


SimpleCAS is a computer algebra library that is meant to be simple enough (and hopefully written clearly enough) that a curious person can take it apart in order to understand how it works. It is written almost entirely in base Python so that even the most basic parts can be seen. In particular the standard library modules `math`, `fractions`, and `decimal` are not used.

For the love of common sense don't use SimpleCAS for anything remotely important. Its quite slow and, despite my best efforts, I can't guarantee it is always accurate.



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



## QPoly
Univariate polynomials with rational coefficients. Internally these are simple to represent as a list with the term of degree 0 in position 0, the term of degree 1 in position 1, and so on. This makes indexing the polynomial when working with it in Python intuitive but its now how we generally write polynomials. When a QPoly object is printed it will show the standard written form with terms in descending order.

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

Naturally QPoly will interact with most mathematical operations. Addition, subtraction, and multiplication are defined with for all inputs. Exponentiation is defined for non-negative integers. True division is not defined because not every polynomial has an inverse which is also a polynomials, instead Euclidean divison is used.

But wait, there's more! The standard written form is fine for text but it looks ugly in places where more complex formatting is expected. To that end the `pretty_name` property gives a LaTeX formated version of the polynomial.

```
print(P.pretty_name)
$−11x^{4}\;+\;x^{2}\;+\;3x\;+\;2$
```

It looks pretty horrendous just written out like that but lets try it with the `poly_plot()` function

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/poly_example.png "polynomial")



## RFunc
Quotients of polynomials represented in simplest form.



# In Progress
One object is partially supported:

## PSeries
Power series with finite or infinite terms.


# Planned
One object is planned:

## ZPoly
Polynomials with integer coefficients reduced modulo some integer.

# Not Planned
## Multivariate Polynomials
Multivariate polynomials would, to my knowledge, require fundamentally redesigning the logic of how the system treats polynomials to be vastly more complex. Because the simplicity of the QPoly object is central to making SimpleCAS easy to understand there are no plans to include multivariate polynomials in SimpleCAS.

## Radicals and Logarithms
Can't figure out a good way to handle these right now.
