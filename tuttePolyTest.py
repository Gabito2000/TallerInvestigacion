# uses sympy to do the calculations (x^6+5x^5+15x^4+12x^3y+23x^3+9x^2y^2+30x^2y+19x^2+xy^4+9xy^3+24xy^2+26xy+6x+y^5+5y^4+11y^3+13y^2+6y - x^6+5x^5+x^4y+14x^4+11x^3y+23x^3+7x^2y^2+30x^2y+21x^2+6xy^3+25xy^2+31xy+8x+y^5+6y^4+15y^3+18y^2+8y)/(x+y-xy)

import sympy as sp

x, y = sp.symbols('x y')

# define
num_1 = sp.Poly(x**6 + 5*x**5 + 15*x**4 + 12*x**3*y + 23*x**3 + 9*x**2*y**2 + 30*x**2*y + 19*x**2 + x*y**4 + 9*x*y**3 + 24*x*y**2 + 26*x*y + 6*x + y**5 + 5*y**4 + 11*y**3 + 13*y**2 + 6*y)
num_2 = sp.Poly(x**6 + 5*x**5 + x**4*y + 14*x**4 + 11*x**3*y + 23*x**3 + 7*x**2*y**2 + 30*x**2*y + 21*x**2 + 6*x*y**3 + 25*x*y**2 + 31*x*y + 8*x + y**5 + 6*y**4 + 15*y**3 + 18*y**2 + 8*y) 

# the denominator of the Tutte polynomial
print(num_1)
print(num_2)


den = sp.Poly(x+y-(x*y))
ret = sp.simplify((num_1-num_2)/den)

print(ret)

R_dict = ret.as_coefficients_dict()

for r_key, r_value in R_dict.items():
    if r_value >= 0:
        print("num_1 is greater than num_2")
        break

for r_key, r_value in R_dict.items():
    if r_value <= 0:
        print("num_2 is greater than num_1")
        break