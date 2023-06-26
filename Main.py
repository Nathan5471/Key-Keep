from Password_Generator import *


def generate_login():
    website = input("What is the website you are creating a login for?: ")
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
        first_user = get_user(edit_website).replace("Username: ", "")
        new_user = first_user.replace("\n", "")
    if edit_password == "y":
        new_password = input("what do you want your new password to be?: ")
    else:
        first_password = get_password(edit_website).replace("Password: ", "")
        new_password = first_password.replace("\n", "")
    login_info = get_login("true", edit_website)
    with open("Passwords.txt", "r") as file:
        logins = file.read()

    update_login = logins.replace(
        login_info,
        "Username: " + new_user + "\nPassword: " + new_password + "\n" + "\n",
    )

    with open("Passwords.txt", "w") as file:
        file.write(update_login)
