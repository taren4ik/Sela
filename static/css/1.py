import math
a, b = map(int, input().split())
sequence = []
result = []
otvet = 0

xy = a * b
if b % a == 0:
    tt = int(b / a)
    for value in range(1, tt + 1):
        if tt % value == 0:
            sequence.append(value)
    for word in sequence:
        result.append(int(word) * a)

    for element in result:
        y = xy / element
        if float(xy) // math.gcd(element, int(y)) == b:
            otvet += 1

print(otvet)
