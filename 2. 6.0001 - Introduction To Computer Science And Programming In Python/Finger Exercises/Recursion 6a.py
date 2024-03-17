#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 16:49:38 2024

@author: lucas
"""

def harmonic_sum(n):
    """Assumes n > 0, harmonic sum must be calculated using
    the formula 1 + 1/2 + 1/3 + ... + 1/n
    """
    if n == 2:
        return 1/n
    else:
        return 1/n + harmonic_sum(n - 1)
    
number_harmonic = int(input('Number of Harmonic Sum: '))
print('Harmonic Sum:', round((1 + harmonic_sum(number_harmonic)), 2))