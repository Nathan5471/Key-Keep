from Password_Generator import *


logged_in = False


def create_account():
    if not logged_in:
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if "User:" in line:
                    user = lines[i + 1]
        if user == "\n":
            username = input("What do you want your username to be?: ")
            password = input("What do you want your password to be?: ")
            with open("Passwords.txt", "r") as file:
                lines = file.readlines()
                num_lines = len(lines)
                for i in range(num_lines):
                    line = lines[i]
                    if "User:" in line:
                        lines.insert(
                            i + 1, "Username: " + username + "\nPassword: " + password
                        )
                    break
            with open("Passwords.txt", "w") as file:
                file.writelines(lines)
        else:
            print("There is already an account created, please login")
    else:
        print("You are already logged in")


def login():
    global logged_in
    if not logged_in:
        username = input("What is your username?: ")
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if "User:" in line:
                    user = lines[i + 1]
                    user = user.replace("Username: ", "")
                    user = user.replace("\n", "")
        if username == user:
            input_password = input("What is the password for your accout?: ")
            with open("Passwords.txt", "r") as file:
                lines = file.readlines()
                num_lines = len(lines)
                for i in range(num_lines):
                    line = lines[i]
                    if "User:" in line:
                        password = lines[i + 2]
                        password = password.replace("Password: ", "")
                        password = password.replace("\n", "")
            if password == input_password:
                logged_in = True
                print("You have succesfully logged in!")
            else:
                print("The password you inputed is not correct")
                correct = False
                attempts = 1
                while not correct and attempts <= 10:
                    input_password = input("What is the password for your accout?: ")
                    if password == input_password:
                        logged_in = True
                        print("You have succesfully logged in!")
                        correct = True
                    else:
                        attempts += 1
                        print("The password you inputed is not correct")
    else:
        print("You are already logged in")


def get_account():
    if logged_in:
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if "User:" in line:
                    print(lines[i + 1])
                    print(lines[i + 2])
    else:
        print("Please login or create an account to use this function")


def change_username():
    if logged_in:
        new_user = input("What do you want your username to be?")
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if "User:" in line:
                    username = lines[i + 1]
        with open("Passwords.txt", "r") as file:
            txt_file = file.read()

        update_username = txt_file.replace(
            username,
            "Username: " + new_user + "\n",
        )

        with open("Passwords.txt", "w") as file:
            file.write(update_username)


def change_password():
    if logged_in:
        new_password = input("What do you want your password to be?")
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if "User:" in line:
                    password = lines[i + 2]
        with open("Passwords.txt", "r") as file:
            txt_file = file.read()

        update_password = txt_file.replace(
            password,
            "Password: " + new_password + "\n",
        )

        with open("Passwords.txt", "w") as file:
            file.write(update_password)


def generate_login():
    website = input("What is the website you are creating a login for?: ")
    with open("Passwords.txt", "r") as file:
        if website in file.read():
            login_exists = True
        else:
            login_exists = False
    if not login_exists:
        username = input("What is the username you are using for this login?: ")
        password_option = input("Do you want to have a password generated? y or n: ")
        if password_option == "n":
            password = input("What is the password you are using: ")
            with open("Passwords.txt", "a") as file:
                file.write("Website: " + website + "\n")
                file.write("Username: " + username + "\n")
                file.write("Password: " + password + "\n" + "\n")
        else:
            password = generate_password()
            print(password)
            done = True
            while done:
                good_password = input("Is this password okay? y or n: ")
                if good_password == "y":
                    with open("Passwords.txt", "a") as file:
                        file.write("Website: " + website + "\n")
                        file.write("Username: " + username + "\n")
                        file.write("Password: " + password + "\n" + "\n")
                    done = False
                elif good_password == "n":
                    password = generate_password()
                    print(password)
                else:
                    good_password = input("Please input y or n: ")
    else:
        print("A login already exist for the website")


def get_websites():
    with open("Passwords.txt", "r") as file:
        for line in file:
            if "Website: " in line:
                unwanted_text = "Website: "
                print(line.replace(unwanted_text, ""))


def get_login(edit="", website=""):
    if edit == "true":
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if website in line:
                    return lines[i + 1] + lines[i + 2]
    else:
        website = input("What website do you want your login information from?: ")
        with open("Passwords.txt", "r") as file:
            lines = file.readlines()
            num_lines = len(lines)
            for i in range(num_lines):
                line = lines[i]
                if website in line:
                    print(lines[i + 1])
                    print(lines[i + 2])


def get_user(website):
    with open("Passwords.txt", "r") as file:
        lines = file.readlines()
        num_lines = len(lines)
        for i in range(num_lines):
            line = lines[i]
            if website in line:
                return lines[i + 1]


def get_password(website):
    with open("Passwords.txt", "r") as file:
        lines = file.readlines()
        num_lines = len(lines)
        for i in range(num_lines):
            line = lines[i]
            if website in line:
                return lines[i + 2]


def edit_login():
    edit_website = input(
        "What website do you want to change the login information for?: "
    )
    edit_user = input("Do you want to edit your username? y or n: ")
    if edit_user == "y" or edit_user == "n":
        valid_response = True
    else:
        valid_response = False
        while not valid_response:
            edit_user = input("Please input y or n: ")
            if edit_user == "y" or "n":
                valid_response = True
    edit_password = input("Do you want to edit your password? y or n: ")
    if edit_password == "y" or edit_password == "n":
        valid_response = True
    else:
        valid_response = False
        while not valid_response:
            edit_password = input("Please input y or n: ")
            if edit_password == "y" or "n":
                valid_response = True
    if edit_user == "y":
        new_user = input("What do you want your new username to be?: ")
    else:
        new_user = get_user(edit_website).replace("Username: ", "")
        new_user = new_user.replace("\n", "")
    if edit_password == "y":
        new_password = input("what do you want your new password to be?: ")
    else:
        new_password = get_password(edit_website).replace("Password: ", "")
        new_password = new_password.replace("\n", "")
    login_info = get_login("true", edit_website)
    with open("Passwords.txt", "r") as file:
        logins = file.read()

    update_login = logins.replace(
        login_info,
        "Username: " + new_user + "\nPassword: " + new_password + "\n" + "\n",
    )

    with open("Passwords.txt", "w") as file:
        file.write(update_login)
