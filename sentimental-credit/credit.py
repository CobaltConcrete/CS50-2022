import math


def main():

    n = get_number()

    if Luhn(n):

        # check if AMEX
        if (n >= 34*pow(10, 13) and n < 35*pow(10, 13)) or (n >= 37*pow(10, 13) and n < 38*pow(10, 13)):
            print("AMEX")

        # check if MASTERCARD
        elif n >= 51*pow(10, 14) and n < 56*pow(10, 14):
            print("MASTERCARD")

        # check if VISA
        elif (n >= 4*pow(10, 12) and n < 5*pow(10, 12)) or (n >= 4*pow(10, 15) and n < 5*pow(10, 15)):
            print("VISA")

        # no match
        else:
            print("INVALID")

    # failed Lun's Algorithm
    else:
        print("INVALID")


def get_number():
    while True:
        try:
            n = int(input("Number: "))
        except ValueError:
            continue
        if n > 0:
            return n

# first sum in Luhn
def sum1(n):
    if n < 10:
        return 0
    else:
        d1 = int(2 * (int(n / 10) % 10))
        return int(int(d1/10) + d1 % 10 + sum1(n / 100))

# second sum in Luhn
def sum2(n):
    if n == 0:
        return 0
    else:
        d2 = int(n % 10)
        return int(d2 + sum2(n / 100))

# check if Luhn's algorithm returns True
def Luhn(n):
    if (sum1(n) + sum2(n)) % 10 == 0:
        return True

    return False


main()
