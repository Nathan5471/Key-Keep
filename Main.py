from Password_Generator import *


def generate_login():
    website = input("What is the website you are creating a login for?: ")
    username = input("What is the username you are using for this login?: ")
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


def get_login():
    website = input("What website do you want your login information from?: ")
    with open("Passwords.txt", "r") as file:
        lines = file.readlines()
        num_lines = len(lines)
        for i in range(num_lines):
            line = lines[i]
            if website in line:
                print(lines[i + 1])
                print(lines[i + 2])
