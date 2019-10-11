![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/simpleCASlogo.png "SimpleCAS")


SimpleCAS is a computer algebra library that is meant to be simple enough (and hopefully written clearly enough) that a curious person can take it apart in order to understand how it works. Don't use SimpleCAS for anything important. Its quite slow and, despite my best effort, I can't guarantee it is always accurate.



## Features
Currently three kinds of objects are supported by SimpleCAS:

#### Rational
Rational numbers represented in simplest form.

#### QPoly
Univariate polynomials with rational coefficients. Internally these are simply to represent as a list with the term of degree 0 in position 0, the term of degree 1 in position 1, and so on. This makes indexing the polynomial when working with it in Python intuitive but its now how we generally write polynomials. When a QPoly object is printed it will show the standard written form with terms in descending order.

```
P = QPoly( [2,3,1,0,-11] )
print(P)
-11x^4 + x^2 + 3x + 2
```

But wait, there's more! The standard written form is fine for text but it looks ugly in places where more complex formatting is expected. To that end the `pretty_name` property gives a LaTeX formated version of the polynomial.

```
print(P.pretty_name)
$−11x^{4}\;+\;x^{2}\;+\;3x\;+\;2$
```

It looks pretty horrendous just written out like that but lets try it with the `poly_plot()` function

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/poly_example.png "polynomial")



#### RFunc
Quotients of polynomials represented in simplest form.



## In Progress
One object is partially supported:

#### PSeries
Power series with finite or infinite terms.


## Planned
One object is planned:

#### ZPoly
Polynomials with integer coefficients reduced modulo some integer.

## Not Planned
#### Multivariate Polynomials
Multivariate polynomials would, to my knowledge, require fundamentally redesigning the logic of how the system treats polynomials to be vastly more complex. Because the simplicity of the QPoly object is central to making SimpleCAS easy to understand there are no plans to include multivariate polynomials in SimpleCAS.

### Radicals and Logarithms
Can't figure out a good way to handle these right now.
