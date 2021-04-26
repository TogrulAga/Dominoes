from math import log

number_1 = int(input())
number_2 = int(input())

print(round(log(number_1, number_2) if number_2 > 0 and number_2 != 1 else log(number_1), 2))
