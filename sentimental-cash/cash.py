def main():
    # get input for change owed
    c = change_owed()

    # calculate no. of quarters
    quarters = int(c / 25)

    c -= quarters*25

    # calculate no. of dimes
    dimes = int(c / 10)

    c -= dimes*10

    # calculate no. of nickels
    nickels = int(c / 5)

    c -= nickels*5

    # calculate no. of pennies
    pennies = int(c / 1)

    # print sum of coins
    print(quarters + dimes + nickels + pennies)


def change_owed():
    # ensure input is a positive float
    while True:
        try:
            c = float(input("Change owed: "))
        except ValueError:
            continue
        else:
            if c > 0:
                break
    # convert dollars to cents
    return int(c*100)


main()
