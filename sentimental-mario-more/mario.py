def main():
    # get height input
    h = get_height()
    i = int(1)

    # print bricks
    while i <= h:
        print(" "*(h-i) + "#"*i + "  " + "#"*i)
        i += 1


def get_height():
    # ensure height is a digit between 0 and 9 exclusive
    while True:
        h = input("Height: ")
        if h.isdigit() and int(h) > 0 and int(h) < 9:
            break
    return int(h)


main()
