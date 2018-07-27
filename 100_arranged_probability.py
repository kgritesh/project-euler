# -*- coding: utf-8 -*-
"""
If a box contains twenty-one coloured discs, composed of fifteen blue discs and six red discs, and two discs were taken at random, it can be seen that the probability of taking two blue discs, P(BB) = (15/21)×(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box containing eighty-five blue discs and thirty-five red discs.

By finding the first arrangement to contain over 1012 = 1,000,000,000,000 discs in total, determine the number of blue discs that the box would contain.
"""
import math


def recursive_diophantine_equation(x, y):
    return 3 * x + 2 * y - 2, 4 * x + 3 * y - 3


def main():
    x, y = 85, 120
    while y <= math.pow(10, 12):
        x, y = recursive_diophantine_equation(x, y)

    print(x)

if __name__ == '__main__':
    main()
