![alt text][logo]

[logo]: https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/simpleCASlogo.png "SimpleCAS"


SimpleCAS is a computer algebra library that is meant to be simple enough (and hopefully written clearly enough) that a curious person can take it apart in order to understand how it works. Don't use SimpleCAS for anything important. Its quite slow and, despite my best effort, I can't guarantee it is always accurate.



## Features
Currently three kinds of objects are fully supported by SimpleCAS:

#### Rational
Rational numbers represented in simplest form.

#### QPoly
Univariate polynomials with rational coefficients.

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
