from random import *


def generate_password():
    lowercase_letter = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    uppercase_letter = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    special_character = ["!", "@", "#", "$", "&", "?"]

    def get_length():
        # Used in generate_password() to get password length that user wants

        global length
        length = input("How many characters do you want your password to be?: ")
        if length.isdigit():
            length = int(length)
            return length
        else:
            print("Please input a number")
            get_length()

    def password_strength():
        # Use in generate_password() to get password strength that user want

        global strength
        strength = input("On a scale of 1-4 how strong do you want your password?: ")
        """  Requirements
        1. Numbers or Letters
        2. Numbers and Letters
        3. Uppercase Letters, Lowercase Letters, and Numbers
        4. Special Characters, Uppercase Letters, Lowercase Letters, and Numbers
        """
        if strength.isdigit():
            if int(strength) >= 1 and int(strength) <= 4:
                strength = int(strength)
            else:
                print("Please input a number between 1-4")
                password_strength()
        else:
            print("Please input a number")
            password_strength()

    get_length()  # Password length
    password_strength()  # Password strength

    def strength_1():
        random = randrange(1, 3)
        if random == 1:
            digits = 1
            password = ""
            while digits <= length:
                password += str(randrange(0, 10))
                digits += 1
            return password
        else:
            digits = 1
            password = ""
            while digits <= length:
                lowernum = randrange(0, 26)
                password += lowercase_letter[lowernum]
                digits += 1
            return password

    def strength_2():
        digits = 1
        password = ""
        while digits <= length:
            num = randrange(1, 3)
            if num == 1:
                password += str(randrange(0, 10))
                digits += 1
            else:
                lowernum = randrange(0, 26)
                password += lowercase_letter[lowernum]
                digits += 1
        return password

    def strength_3():
        digits = 1
        password = ""
        while digits <= length:
            num = randrange(1, 4)
            if num == 1:
                password += str(randrange(0, 10))
                digits += 1
            elif num == 2:
                lowernum = randrange(0, 26)
                password += lowercase_letter[lowernum]
                digits += 1
            else:
                uppernum = randrange(0, 26)
                password += uppercase_letter[uppernum]
                digits += 1
        return password

    def strength_4():
        digits = 1
        password = ""
        while digits <= length:
            num = randrange(1, 5)
            if num == 1:
                password += str(randrange(0, 10))
                digits += 1
            elif num == 2:
                lowernum = randrange(0, 26)
                password += lowercase_letter[lowernum]
                digits += 1
            elif num == 3:
                uppernum = randrange(0, 26)
                password += uppercase_letter[uppernum]
                digits += 1
            else:
                special_num = randrange(0, 6)
                password += special_character[special_num]
                digits += 1
        return password

    if strength == 1:
        password = strength_1()
        return password
    elif strength == 2:
        password = strength_2()
        return password
    elif strength == 3:
        password = strength_3()
        return password
    else:
        password = strength_4()
        return password
