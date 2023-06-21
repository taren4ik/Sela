def main():
    a = input()
    mass = list(map(int, input().split()))
    dic = {}
    counter = 0
    for value in mass:

        if value in dic:
            dic[value] += 1
        else:
            dic[value] = 1

    for i in dic.values():
        if i == 1:
            counter += 1
    return counter


if __name__ == '__main__':
    print(main())