#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:39:52 2024

@author: lucas
"""

def get_min(d):
    """d a dict mapping letters to ints
    returns the value in d with the key that occurs first
    in the
    alphabet. E.g., if d = {x = 11, b = 12}, get_min
    returns 12."""
    
    return_value = 'z'
    for key, val in d.items():
        if key <= return_value:
            return_value = key
            
    return d[return_value]