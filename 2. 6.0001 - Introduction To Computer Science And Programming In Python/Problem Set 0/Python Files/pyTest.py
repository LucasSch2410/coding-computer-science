#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 22:20:40 2024

@author: lucas
"""

import numpy

x = input("Enter number x: ")
y = input("Enter number y: ")

calc = int(x) ** int(y)

print("X**y = ", str(calc))
print("log(x) = ", int(numpy.log2(int(x))))
