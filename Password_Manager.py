import secrets
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sqlite3
import os


def generate_password(length):
    if type(length) == int or length.isdigit():
        length = int(length)
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(characters) for _ in range(length))
        password_strength = check_password(password)
        if password_strength[5]:
            return password
        else:
            if password_strength[0]:
                generate_password(length)


def check_password(password):
    min_length = 12
    max_length = 36
    strength = 0
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    numbers = string.digits
    special_characters = string.punctuation
    length_requirements = False
    lowercase_requirements = False
    uppercase_requirements = False
    number_requirements = False
    special_character_requirements = False
    if len(password) >= min_length and len(password) <= max_length:
        strength += 1
        length_requirements = True
    for char in password:
        if char in lowercase_letters:
            lowercase_requirements = True
        if char in uppercase_letters:
            uppercase_requirements = True
        if char in numbers:
            number_requirements = True
        if char in special_characters:
            special_character_requirements = True
    if lowercase_requirements:
        strength += 1
    if uppercase_requirements:
        strength += 1
    if number_requirements:
        strength += 1
    if special_character_requirements:
        strength += 1
    return [
        length_requirements,
        number_requirements,
        lowercase_requirements,
        uppercase_requirements,
        special_character_requirements,
        strength,
    ]


def create_account(username, password):
    if not os.path.exists("key_manager.db"):
        if check_password(password)[5] == 5:
            con = sqlite3.connect("password_manager.db")
            con1 = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur1 = con1.cursor()
            cur.execute("CREATE TABLE login(username, password, id)")
            cur1.execute("CREATE TABLE keys(encryption_key, iv, id)")
            con.commit()
            con1.commit()
            con.close()
            con1.close()
            key = get_random_bytes(32)
            cipher = AES.new(key, AES.MODE_CBC)
            padded_password = pad(password.encode(), AES.block_size)
            encrypted_password = cipher.encrypt(padded_password)
            con = sqlite3.connect("password_manager.db")
            con1 = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur1 = con1.cursor()
            iv = cipher.iv
            login_data = (username, encrypted_password, 0)
            key_data = (key, iv, 0)
            cur.execute(
                "INSERT INTO login (username, password, id) VALUES (?, ?, ?)",
                login_data,
            )
            cur1.execute(
                "INSERT INTO keys (encryption_key, iv, id) VALUES (?, ?, ?)", key_data
            )
            con.commit()
            con1.commit()
            con.close()
            con1.close()
            return "Succes"
        else:
            return "Weak password"
    else:
        return "There is already an account created"


def login(username, input_password):
    if os.path.exists("key_manager.db"):
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
        decipher = AES.new(key, AES.MODE_CBC, iv=iv)
        password = unpad((decipher.decrypt(password)), AES.block_size).decode()
        if password == input_password and username == user:
            logged_in = True
            return "Succes"
        else:
            return "Username or password is incorrect"

    else:
        return "You need to create an account"


def get_account(just_username=""):
    if os.path.exists("key_manager.db"):
        con = sqlite3.connect("password_manager.db")
        con1 = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur1 = con1.cursor()
        cur.execute("SELECT * FROM login")
        cur1.execute("SELECT * FROM keys WHERE id = 0")
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
        if just_username == "":
            return "Username:\n" + username + " \nPassword:\n" + password
        elif just_username == "yes":
            return username
    else:
        return "No Username"


def change_username(new_user):
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("UPDATE login SET username = ? WHERE id = ?", (new_user, 0))
    con.commit()
    con.close()


def change_password(new_password):
    if check_password(new_password)[5] == 5:
        con = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM keys WHERE id = 0")
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
            "UPDATE login SET password = ? WHERE id = ?", (encrypted_password, 0)
        )
        con.commit()
        con.close()
    else:
        return "Weak password"


def generate_login(website, username, password):
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
        if check_password(password)[5] == 5:
            con = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur.execute("SELECT id FROM keys")
            ids = cur.fetchall()
            id = len(ids)
            con.close()
            con = sqlite3.connect("password_manager.db")
            con1 = sqlite3.connect("key_manager.db")
            cur = con.cursor()
            cur1 = con1.cursor()
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
            return "Succes"
        else:
            return "Weak password"
    else:
        return "A login already exist for the website"


def get_websites():
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS passwords (website, username, password, id)"
    )
    cur.execute("SELECT website FROM passwords")
    websites = cur.fetchall()
    con.close()
    if websites:
        return websites
    else:
        return ["No Websites"]


def get_login(website, password=""):
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
    if len(username) > 3 and len(password) > 3:
        return "Username: \n" + username + "\nPassword: \n" + password
    elif len(username) > 3:
        return "Username: \n" + username + "\nPassword: " + password
    elif len(password) > 3:
        return "Username: " + username + "\nPassword: \n" + password
    else:
        return "Username: " + username + "\nPassword: " + password


def edit_login(website, username, password):
    if check_password(password)[5] == 5:
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM passwords WHERE website = ?", (website,))
        rows = cur.fetchall()
        for row in rows:
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
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_password = pad(password.encode(), AES.block_size)
        encrypted_password = cipher.encrypt(padded_password)
        con = sqlite3.connect("password_manager.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE passwords SET username = ? WHERE website = ?",
            (
                username,
                website,
            ),
        )
        cur.execute(
            "UPDATE passwords SET password = ? WHERE website = ?",
            (
                encrypted_password,
                website,
            ),
        ),
        con.commit()
        con.close()
    else:
        return "Weak password"
