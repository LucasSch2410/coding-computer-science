#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 11:50:00 2024

@author: lucas
"""

portion_down_payment = 0.25
current_savings = 0
r = 0.04

annual_salary = int(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = int(input("Enter the cost of your dream home: "))

months = 0
while current_savings < total_cost * portion_down_payment:
    
    current_savings += current_savings * r / 12
    current_savings += (annual_salary/12) * portion_saved
    months += 1

print(f"Number of months: {months}")