#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 12:07:20 2024

@author: lucas
"""

semi_annual_raise = .07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
months = 36
steps_bisection = 0

annual_salary = int(input("Enter your starting salary: "))


def calculates_salary(new_salary, percentage_rate):
    current_savings = 0
    
    for month in range(1, 37):
        current_savings += current_savings * r / 12
        current_savings += (new_salary/12) * percentage_rate

        if month % 6 == 0:
            new_salary += new_salary * semi_annual_raise
    
    return current_savings


start = 0
end = 10000
saving_rate = 0
down_payment = total_cost * portion_down_payment

while True:
    middle = (end + start) // 2
    percentage_rate = (middle / 10000)
    new_salary = annual_salary

    current_savings = calculates_salary(new_salary, percentage_rate)
    steps_bisection += 1

    if middle == 10000:
        print("It is not possible to pay the down payment in three years.")
        break
    elif current_savings < (down_payment + 100) and current_savings > (down_payment - 100):
        saving_rate = middle / 10000   
        print("Best savings rate:", saving_rate)
        print("Steps in bisection search:", steps_bisection)
        break
    elif current_savings < down_payment:
        start = middle + 1
    elif current_savings > down_payment:
        end = middle - 1
        
        