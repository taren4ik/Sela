import sys
import math
import datetime


def main():
    weekend = (6, 7,)
    read_books = 1
    positiv = 0
    start = datetime.datetime.now()
    k, books_total, day_now = map(int, input().split())

    if books_total > read_books:
        if day_now not in weekend:
            books_total += k
        D = 1 + 4 * books_total * 2
        X = math.floor((D ** 0.5 - 1) / 2)
        books_total -= ((X+1) * X / 2) + (X // 7)*2
        read_books += X
        positiv += X
        day_now += X % 7


    while read_books <= books_total + k:

        if day_now not in weekend:
            books_total += k
        books_total -= read_books
        if books_total >= 0:
            read_books += 1
            positiv += 1
            day_now += 1 % 7
        else:
            return positiv

    duration = datetime.datetime.now() - start
    print(f'time: {duration}')
    return positiv


if __name__ == '__main__':
    print(main())
