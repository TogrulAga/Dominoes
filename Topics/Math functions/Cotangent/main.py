from math import cos, sin, radians


angle = int(input())

print(round(cos(radians(angle)) / sin(radians(angle)), ndigits=10))
