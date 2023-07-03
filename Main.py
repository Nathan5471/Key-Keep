from Password_Generator import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sqlite3
import os


logged_in = False


def create_account():
    if not logged_in:
        if not os.path.exists("password_manager.db"):
            con = sqlite3.connect("password_manager.db")
            con1 = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur1 = con1.cursor()
            cur.execute("CREATE TABLE login(username, password, account)")
            cur1.execute("CREATE TABLE keys(encryption_key, iv, id)")
            con.commit()
            con1.commit()
            con.close()
            con1.close()
            username = input("What do you want your username to be?: ")
            password = input("What do you want your password to be?: ")
            key = get_random_bytes(32)
            cipher = AES.new(key, AES.MODE_CBC)
            padded_password = pad(password.encode(), AES.block_size)
            encrypted_password = cipher.encrypt(padded_password)
            con = sqlite3.connect("password_manager.db")
            con1 = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur1 = con1.cursor()
            iv = cipher.iv
            login_data = (username, encrypted_password, 1)
            key_data = (key, iv, 0)
            cur.execute(
                "INSERT INTO login (username, password, account) VALUES (?, ?, ?)",
                login_data,
            )
            cur1.execute(
                "INSERT INTO keys (encryption_key, iv, id) VALUES (?, ?, ?)", key_data
            )
            con.commit()
            con1.commit()
            con.close()
            con1.close()
        else:
            print("There is already an account created")
    else:
        print("You are already logged in")


def login():
    global logged_in
    if not logged_in:
        if os.path.exists("password_manager.db"):
            username = input("What is your username?: ")
            con = sqlite3.connect("password_manager.db")
            con1 = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur1 = con1.cursor()
            cur.execute("SELECT * FROM login")
            cur1.execute("SELECT * FROM keys WHERE id = 0")
            rows = cur.fetchall()
            for row in rows:
                user = row[0]
                password = row[1]
            rows = cur1.fetchall()
            for row in rows:
                key = row[0]
                iv = row[1]
            con.close
            con1.close
            if username == user:
                input_password = input("What is the password for your accout?: ")
                decipher = AES.new(key, AES.MODE_CBC, iv=iv)
                password = unpad((decipher.decrypt(password)), AES.block_size).decode()
                if password == input_password:
                    logged_in = True
                    print("You have succesfully logged in!")
                else:
                    print("The password you inputed is not correct")
                    correct = False
                    attempts = 1
                    while not correct and attempts <= 10:
                        input_password = input(
                            "What is the password for your accout?: "
                        )
                        if password == input_password:
                            logged_in = True
                            print("You have succesfully logged in!")
                            correct = True
                        else:
                            attempts += 1
                            print("The password you inputed is not correct")
                    if not correct and attempts <= 10:
                        print("You have attempted entering the password too many times")
        else:
            print("You need to create an account")
    else:
        print("You are already logged in")


def get_account():
    if logged_in:
        con = sqlite3.connect("password_manager.db")
        con1 = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur1 = con1.cursor()
        cur.execute("SELECT * FROM login")
        cur1.execute("SELECT * FROM keys")
        rows = cur.fetchall()
        for row in rows:
            username = row[0]
            password = row[1]
        rows = cur1.fetchall()
        for row in rows:
            key = row[0]
            iv = row[1]
        con.close
        con1.close
        decipher = AES.new(key, AES.MODE_CBC, iv=iv)
        password = unpad((decipher.decrypt(password)), AES.block_size).decode()
        print("Username: " + username + "\nPassword: " + password)
    else:
        print("Please login or create an account to use this function")


def change_username():
    if logged_in:
        new_user = input("What do you want your username to be?")
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute("UPDATE login SET username = ? WHERE account = ?", (new_user, 0))
        con.commit()
        con.close()
    else:
        print("Please login or create an account to use this function")


def change_password():
    if logged_in:
        new_password = input("What do you want your password to be?")
        con = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM keys")
        rows = cur.fetchall()
        for row in rows:
            key = row[0]
            iv = row[1]
        con.close()
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded_password = pad(new_password.encode(), AES.block_size)
        encrypted_password = cipher.encrypt(padded_password)
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE login SET password = ? WHERE account = ?", (encrypted_password, 0)
        )
        con.commit()
        con.close()
    else:
        print("Please login or create an account to use this function")


def generate_login():
    if logged_in:
        website = input("What is the website you are creating a login for?: ")
        con = sqlite3.connect("password_manager.db")
        con1 = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur1 = con1.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS passwords (website, username, password, id)"
        )
        con.commit()
        cur.execute("SELECT * FROM passwords WHERE website = ?", (website,))
        rows = cur.fetchall()
        global login_exists
        login_exists = ""
        for row in rows:
            if rows:
                login_exists = True
            else:
                login_exists = False
        if not login_exists:
            username = input("What is the username you are using for this login?: ")
            password_option = input(
                "Do you want to have a password generated? y or n: "
            )
            con = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur.execute("SELECT id FROM keys")
            ids = cur.fetchall()
            id = 0
            for i in ids:
                id += 1
            con.close()
            if password_option == "n":
                con = sqlite3.connect("password_manager.db")
                con1 = sqlite3.connect("key_manager.db")
                cur = con.cursor()
                cur1 = con1.cursor()
                password = input("What is the password you are using: ")
                key = get_random_bytes(32)
                cipher = AES.new(key, AES.MODE_CBC)
                iv = cipher.iv
                padded_password = pad(password.encode(), AES.block_size)
                encrypted_password = cipher.encrypt(padded_password)
                cur.execute(
                    "INSERT INTO passwords (website, username, password, id) VALUES (?, ?, ?, ?)",
                    (website, username, encrypted_password, id),
                )
                cur1.execute(
                    "INSERT INTO keys (encryption_key, iv, id) VALUES (?, ?, ?)",
                    (key, iv, id),
                )
                con.commit()
                con1.commit()
                con.close()
                con1.close()
            else:
                password = generate_password()
                print(password)
                done = True
                while done:
                    con = sqlite3.connect("key_manager.db")
                    cur = con.cursor()
                    good_password = input("Is this password okay? y or n: ")
                    if good_password == "y":
                        cur.execute("SELECT * FROM keys")
                        rows = cur.fetchall()
                        for row in rows:
                            key = row[0]
                            iv = row[1]
                        con.close()
                        con = sqlite3.connect("password_manager.db")
                        con1 = sqlite3.connect("key_manager.db")
                        cur = con.cursor()
                        cur1 = con1.cursor()
                        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                        padded_password = pad(password.encode(), AES.block_size)
                        encrypted_password = cipher.encrypt(padded_password)
                        cur.execute(
                            "INSERT INTO passwords (website, username, password, id) VALUES (?, ?, ?, ?)",
                            (website, username, encrypted_password, id),
                        )
                        cur1.execute(
                            "INSERT INTO keys (encryption_key, iv, id) VALUES (?, ?, ?)",
                            (key, iv, id),
                        )
                        con.commit()
                        con1.commit()
                        con.close()
                        con1.close()
                        done = False
                    elif good_password == "n":
                        password = generate_password()
                        print(password)
                    else:
                        good_password = input("Please input y or n: ")
        else:
            print("A login already exist for the website")
    else:
        print("Please login or create an account to use this function")


def get_websites():
    if logged_in:
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute("SELECT website FROM passwords")
        websites = cur.fetchall()
        for website in websites:
            print(website)
        con.close()
    else:
        print("Please login or create an account to use this function")


def get_login():
    if logged_in:
        website = input("What website do you want your login information from?: ")
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM passwords WHERE website = ?", (website,))
        rows = cur.fetchall()
        for row in rows:
            username = row[1]
            password = row[2]
            id = row[3]
        con.close()
        con = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM keys WHERE id = ?", (id,))
        rows = cur.fetchall()
        for row in rows:
            key = row[0]
            iv = row[1]
        con.close()
        decipher = AES.new(key, AES.MODE_CBC, iv=iv)
        password = unpad((decipher.decrypt(password)), AES.block_size).decode()
        print("Username: " + username + "\nPassword: " + password)
    else:
        print("Please login or create an account to use this function")


def edit_login():
    if logged_in:
        website = input("What website's login information are you trying to edit?: ")
        edit_username = input("Do you want to edit your username? y or n: ")
        if edit_username == "y" or edit_username == "n":
            valid_response = True
        else:
            edit_username = input("Please input y or n: ")
            while valid_response != True:
                if edit_username == "y" or edit_username == "n":
                    valid_response = True
                else:
                    edit_username = input("Please input y or n: ")
        edit_password = input("Do you want to edit your password? y or n: ")
        if edit_password == "y" or edit_password == "n":
            valid_response = True
        else:
            edit_password = input("Please input y or n: ")
            while valid_response != True:
                if edit_password == "y" or edit_password == "n":
                    valid_response = True
                else:
                    edit_password = input("Please input y or n: ")
        if edit_username == "y":
            new_username = input("What do you want your new username to be?: ")
        else:
            con = sqlite3.connect("password_manager.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM passwords WHERE website = ?", (website,))
            rows = cur.fetchall()
            for row in rows:
                new_username = row[1]
            con.close()
        if edit_password == "y":
            new_password = input("What do you want your new password to be?: ")
            con = sqlite3.connect("password_manager.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM passwords WHERE website = ?", (website,))
            rows = cur.fetchall()
            for row in rows:
                id = row[3]
            con = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM keys WHERE id = ?", (id,))
            rows = cur.fetchall()
            for row in rows:
                key = row[0]
                iv = row[1]
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            padded_password = pad(new_password.encode(), AES.block_size)
            encrypted_password = cipher.encrypt(padded_password)
            con.close()
        else:
            con = sqlite3.connect("password_manager.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM passwords WHERE website = ?", (website,))
            rows = cur.fetchall()
            for row in rows:
                encrypted_password = row[2]
            con.close()
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE passwords SET username = ? WHERE website = ?",
            (new_username, website),
        )
        cur.execute(
            "UPDATE passwords SET password = ? WHERE website = ?",
            (encrypted_password, website),
        )
        con.commit()
        con.close()

    else:
        print("Please login or create an account to use this function")
