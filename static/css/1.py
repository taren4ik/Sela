def main():
	weekend = (6, 7,)
	read_books = 1
	positiv = 0
	k, books_total, day_now = map(int, input().split())
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
	return positiv


if __name__ == '__main__':
	print(main())
