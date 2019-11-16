![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/simpleCASlogo.png "SimpleCAS")


SimpleCAS is a computer algebra library that works with rational numbers and univariate polynomials which is meant to be simple enough (and hopefully written clearly enough) that a curious person can take it apart in order to understand how it works. It is written almost entirely in base Python so that even the most basic parts can be seen. In particular the standard library modules `math`, `fractions`, and `decimal` are not used.

For the love of common sense don't use SimpleCAS for anything remotely important. Its quite slow and, despite my best efforts, I can't guarantee it is always accurate. Also it does not currently provide symbolic calculation of roots for any polynomials.



# Features
Currently four basic kinds of objects are supported by SimpleCAS: Rational (rational numbers), CFrac (simple continued fractions), QPoly (polynomials with rational coefficients), and ZPoly (polynomials with integer coefficients).

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
print(frac_to_cfrac(R))
[3; 2, 1, 3]
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

# Ratio notation
print(cast_to_rational("45/12"))
15/4

# Terminating decimal notation
print(cast_to_rational("12.95"))
259/20

# Repeating decimal notation
print(cast_to_rational("-.71(010)"))
-70939/999

# Scientific notation
print(cast_to_rational("1.24e-5"))
31/2500000
```

While giving floats to `cast_to_rational` is allowed it is not recommended. Floating point numbers are finite length binary approximations of some real number so the results may not be the same as expected. The method used also relies on how Python converts floating point numbers to strings so it is dependent on any settings that influence that.

```
print(cast_to_rational(45.13))
4513/100

print(cast_to_rational(1/3))
3333333333333333/10000000000000000
```

## CFrac

[Continued fractions](https://en.wikipedia.org/wiki/Continued_fraction) are an alternative way to represent rational numbers that encodes a lot of useful information. The CFrac type specifically represents simple continued fractions, those that have numerator one for all terms.

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/continued_fraction_example.png "8+\cfrac{1}{11+\cfrac{1}{4+\cfrac{1}{2+\cfrac{1}{7}}}}")

A more portable way to describe this is simply as a list. Because the numerators are always equal to one just storing the denominators as a list is sufficient to describe it and also much easier to write. The integer part of the continued fraction is marked by a semicolon.

```
C = CFrac([8, 11, 4, 2, 7])
print(C)
[8; 11, 4, 2, 7]
```

SimpleCAS can also produce the nice LaTeX formatting with the `.pretty_name` attribute.

```
print(C.pretty_name)
8+\cfrac{1}{11+\cfrac{1}{4+\cfrac{1}{2+\cfrac{1}{7}}}}
```

Generalized continued fractions are also supported as CFracG with somehwat different inputs. The list of numerators must be given along with the list of denominators. The inline printing for generalized continued fractions isn't quite as nice, though the `.pretty_name` attribute still gives the LaTeX formatting.

```
D = CFracG([4,1,4,9,16,25],[0,1,3,5,7,9,11])
print(D)
4/(1+1/(3+4/(5+9/(7+16/(9+25/11)))))
```

The convergents of this particular continued fraction approach pi.

```
for i in D.convergents():
   s = str(i)
   print(f"{s:<8} = {i.digits(5)}")
   
0        = 0.00000
4        = 4.00000
3        = 3.00000
19/6     = 3.16666
160/51   = 3.13725
1744/555 = 3.14234
644/205  = 3.14146
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

```
print(P.derivative())
-4x^3 + 18/5x + 3
print(P.integral(C=0))
-1/5x^5 + 3/5x^3 + 3/2x^2 - 13/10x
```

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
Polynomials with integer coefficients.

```
P = ZPoly( [18,0,-8,121,9] )
print(P)
9x^4 + 121x^3 + -8x^2 + 18
```

Optionally a modulus can be provided in order to make the coefficients obey [modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic) for all operations. When the modulus is provided and the coefficients are not positive and less than the modulus then they are reduced by the modulus.

```
P = ZPoly( [18,0,-8,121,9], 27 )
print(P)
9x^4 + 13x^3 + 19x^2 + 18
```

Note that when printed ZPoly does *not* include an indication that it is different from QPoly such as `(mod n)` since this is often inconvenient when several need to be printed for some reason. Instead use the `.full_name` attribute. Similarly the `.pretty_name` attribute which created a LaTeX formatted version of the polynomial does include the modulus. The `zpoly_plot` function will draw the entire polynomial and use `.pretty_name` to write the title.

![alt text](https://github.com/SymmetricChaos/SimpleCAS/blob/master/ImageFiles/ZPolyExample.png "polynomial over GF(83)")

Using `zpoly_plot` on polynomials with a very large number of points is not recommended.

It is often useful for the order of the group to be a prime or prime power so that the group can also be treated as a finite field but this isn't required. For example Shamir's Secret Sharing Scheme must be done over a finite field. The basics of the algorithm are provided by the functions `make_shamir_secret` and `get_shamir_secret`. Say that our secret is the word HELP which we can represent as the number 72697680 in the ASCII encoding. To split the secret so that it can be given to six people and any four of them can recontruct it we need a polynomial of degree 4 with 72697680 as the zeroth order term. We can pick the prime number 104395301 as the order of the field.

```
secret = 72697680
min_parts = 4
total_parts = 6
F = 104395301
pts = make_shamir_secret(secret,min_parts,total_parts,F)
```

This gives us the following points.

```
(21346801, 23023971)
(62283306, 1693724)
(91943746, 96294104)
(5317738, 41135555)
(97064895, 93506030)
(83272536, 75940346)
```

Now four of people can come together and interpolate the polynomial that passes through the points they've been given to reveal the secret that was given to the group.

```
p = [(21346801, 23023971),
     (62283306, 1693724),
     (91943746, 96294104),
     (5317738, 41135555)]
print(get_shamir_secret(p,F))
72697680
```

Because there are only finitely many polynomials of each degree for any given modulus it is possible to list all of them with `all_zpolys` or just the ones with leading coefficient 1 with `all_monic_zpolys`.

```
for poly in all_monic_polys(3):
   if len(poly) > 3:
       break
   print(poly)
1
x
x + 1
x + 2
x^2
x^2 + 1
x^2 + 2
x^2 + x
x^2 + x + 1
x^2 + x + 2
x^2 + 2x
x^2 + 2x + 1
x^2 + 2x + 2
```

# Planned Expansions
Currently there are plans for a few additions to the system. Power series already have a tiny bit of support as the PSeries object. Combiner objects for QPoly have some support so that sums and products of QPoly can be represented. Similar objects for ZPoly are being worked on.

# Not Planned
## Multivariate Polynomials
Multivariate polynomials would, to my knowledge, require fundamentally redesigning the logic of how the system treats polynomials to be vastly more complex. Because the simplicity of the QPoly object is central to making SimpleCAS easy to understand there are no plans to include multivariate polynomials in SimpleCAS.

## Radicals and Logarithms
Can't figure out a good way to generally handle these.
