from Password_Generator import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from tkinter import *
import sqlite3
import os


def create_account(username, password):
    if not os.path.exists("key_manager.db"):
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


def get_account():
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
    return "Username: " + username + " \nPassword: " + password


def change_username(new_user):
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("UPDATE login SET username = ? WHERE id = ?", (new_user, 0))
    con.commit()
    con.close()


def change_password(new_password):
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
    cur.execute("UPDATE login SET password = ? WHERE id = ?", (encrypted_password, 0))
    con.commit()
    con.close()


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
        con = sqlite3.connect("key_manager.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM keys")
        ids = cur.fetchall()
        id = 0
        for i in ids:
            id += 1
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
        return "A login already exist for the website"


def get_websites():
    con = sqlite3.connect("password_manager.db")
    cur = con.cursor()
    cur.execute("SELECT website FROM passwords")
    websites = cur.fetchall()
    if websites:
        return websites
    else:
        return ["No Websites"]
    con.close()


def get_login(website):
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
    return "Username: " + username + "\nPassword: " + password


def edit_login(website, username, password):
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


window = Tk()
window.title("Password Manager")
window.geometry("200x275")


def go_to_create():
    account_page.pack_forget()
    login_page.pack_forget()
    create_page.pack()


def go_to_login():
    account_page.pack_forget()
    create_page.pack_forget()
    login_page.pack()


def go_to_main():
    account_management_page.pack_forget()
    get_account_page.pack_forget()
    change_username_page.pack_forget()
    change_password_page.pack_forget()
    add_password_page.pack_forget()
    get_login_page.pack_forget()
    edit_login_page.pack_forget()
    main_page.pack()


def go_to_account_managment():
    main_page.pack_forget()
    account_management_page.pack()


def go_to_change_username():
    account_management_page.pack_forget()
    change_username_page.pack()


def go_to_change_password():
    account_management_page.pack_forget()
    change_password_page.pack()


def go_to_add():
    main_page.pack_forget()
    add_password_page.pack()


def go_to_get_login():
    main_page.pack_forget()
    websites = get_websites()
    selected_option = websites[0]
    website_dropdown["menu"].delete(0, "end")
    for website in websites:
        website_dropdown["menu"].add_command(
            label=website, command=lambda value=website: selected_option.set(value)
        )
    get_login_page.pack()


def go_to_edit_login():
    main_page.pack_forget()
    websites = get_websites()
    selected_option = websites[0]
    website_dropdown_1["menu"].delete(0, "end")
    for website in websites:
        website_dropdown_1["menu"].add_command(
            label=website, command=lambda value=website: selected_option.set(value)
        )
    edit_login_page.pack()


def create_account_1():
    result = create_account(username_box_create.get(), password_box_create.get())
    if result == "Succes":
        create_page.pack_forget()
        main_page.pack()
    elif result == "There is already an account created":
        error_label = Label(
            create_page,
            text="There is already an account \n created, please login.",
            fg="red",
        )
        error_label.pack(pady=(15, 0))
        login_button = Button(create_page, text="Login", width=15, command=go_to_login)
        login_button.pack()


def login_1():
    result = login(username_box_login.get(), password_box_login.get())
    if result == "Succes":
        login_page.pack_forget()
        main_page.pack()
    elif result == "You need to create an account":
        error_label = Label(login_page, text="You need to create an account", fg="red")
        error_label.pack(pady=(15, 0))
        create_account_button = Button(
            login_page, text="Create Account", width=15, command=go_to_create
        )
        create_account_button.pack()
    elif result == "Username or password is incorrect":
        error_label = Label(
            login_page,
            text="The username or password \n you entered is incorrect",
            fg="red",
        )
        error_label.pack(pady=(15, 0))


def change_username_1():
    change_username(change_username_entry.get())
    go_to_main()


def change_password_1():
    change_password(change_password_entry.get())
    go_to_main()


def add_password_1():
    result = generate_login(
        website_box_add.get(), username_box_add.get(), password_box_add.get()
    )
    if result == "Succes":
        add_password_page.pack_forget()
        main_page.pack()
    elif result == "A login already exist for the website":
        error_label = Label(
            add_password_page,
            text="A password already exist for this website",
            fg="red",
        )
        error_label.pack()


def get_account_1():
    result = get_account()
    account_management_page.pack_forget()
    details_label.config(text=result)
    details_label.pack(pady=(70, 0))
    ok_button.pack(pady=(20, 0))
    get_account_page.pack()


def get_login_1():
    website = selected_option.get().replace("('", "")
    website = website.replace("',)", "")
    login = get_login(website)
    login_label.config(text=login)


def edit_login_1():
    website = selected_option_1.get().replace("('", "")
    website = website.replace("',)", "")
    edit_login(website, username_box_edit.get(), password_box_edit.get())
    go_to_main()


account_page = Frame(window)
create_account_button = Button(
    account_page, text="Create Account", width=15, command=go_to_create
)
create_account_button.pack(pady=(90, 10))
login_button = Button(account_page, text="Login", width=15, command=go_to_login)
login_button.pack(pady=(10, 0))
account_page.pack()

create_page = Frame(window)
username_label = Label(create_page, text="Username")
username_label.pack(pady=(70, 0))
username_box_create = Entry(create_page)
username_box_create.pack()
password_label = Label(create_page, text="Password")
password_label.pack(pady=(10, 0))
password_box_create = Entry(create_page)
password_box_create.pack()
create_account_subit = Button(
    create_page, text="Create Account", width=15, command=create_account_1
)
create_account_subit.pack(pady=(10, 0))

login_page = Frame(window)
username_label = Label(login_page, text="Username")
username_label.pack(pady=(70, 0))
username_box_login = Entry(login_page)
username_box_login.pack()
password_label = Label(login_page, text="Password")
password_label.pack(pady=(10, 0))
password_box_login = Entry(login_page)
password_box_login.pack()
login_subit = Button(login_page, text="Login", width=15, command=login_1)
login_subit.pack(pady=(10, 0))

main_page = Frame(window)
account_management_button = Button(
    main_page, text="Account Management", width=17, command=go_to_account_managment
)
account_management_button.pack(pady=(45, 0))
add_password_button = Button(
    main_page, text="Add Password", width=17, command=go_to_add
)
add_password_button.pack(pady=(20, 0))
get_login_button = Button(
    main_page, text="Get Password", width=17, command=go_to_get_login
)
get_login_button.pack(pady=(20, 0))
edit_login_button = Button(
    main_page, text="Edit Password", width=17, command=go_to_edit_login
)
edit_login_button.pack(pady=(20, 0))

account_management_page = Frame(window)
account_details_button = Button(
    account_management_page, text="Account Details", width=17, command=get_account_1
)
account_details_button.pack(pady=(45, 0))
change_username_button = Button(
    account_management_page,
    text="Change Username",
    width=17,
    command=go_to_change_username,
)
change_username_button.pack(pady=(20, 0))
change_password_button = Button(
    account_management_page,
    text="Change Password",
    width=17,
    command=go_to_change_password,
)
change_password_button.pack(pady=(20, 0))
back_button = Button(account_management_page, text="Back", width=17, command=go_to_main)
back_button.pack(pady=(20, 0))

get_account_page = Frame(window)
details_label = Label(get_account_page, text="")
ok_button = Button(get_account_page, text="Ok", width=10, command=go_to_main)

change_username_page = Frame(window)
change_username_label = Label(change_username_page, text="Username")
change_username_label.pack(pady=(60, 0))
change_username_entry = Entry(change_username_page)
change_username_entry.pack()
change_username_submit = Button(
    change_username_page, text="Change Username", command=change_username_1
)
change_username_submit.pack(pady=(15, 0))
cancel_button = Button(change_username_page, text="Cancel", command=go_to_main)
cancel_button.pack(pady=(15, 0))

change_password_page = Frame(window)
change_password_label = Label(change_password_page, text="Password")
change_password_label.pack(pady=(60, 0))
change_password_entry = Entry(change_password_page)
change_password_entry.pack()
change_password_submit = Button(
    change_password_page, text="Change Password", command=change_password_1
)
change_password_submit.pack(pady=(15, 0))
cancel_button = Button(change_password_page, text="Cancel", command=go_to_main)
cancel_button.pack(pady=(15, 0))

add_password_page = Frame(window)
website_label = Label(add_password_page, text="Website")
website_label.pack(pady=(20, 0))
website_box_add = Entry(add_password_page)
website_box_add.pack()
username_label = Label(add_password_page, text="Username")
username_label.pack(pady=(10, 0))
username_box_add = Entry(add_password_page)
username_box_add.pack()
password_label = Label(add_password_page, text="Password")
password_label.pack(pady=(10, 0))
password_box_add = Entry(add_password_page)
password_box_add.pack()
add_button = Button(
    add_password_page, text="Add Password", width=15, command=add_password_1
)
add_button.pack(pady=(10, 0))
back_button = Button(add_password_page, text="Back", width=15, command=go_to_main)
back_button.pack(pady=(10, 0))

con = sqlite3.connect("password_manager.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS passwords (website, username, password, id)")
con.commit()

websites = get_websites()

get_login_page = Frame(window)
selected_option = StringVar(window)
selected_option.set(websites[0])
website_dropdown = OptionMenu(get_login_page, selected_option, *websites)
website_dropdown.pack(pady=(60, 0))
get_login_button_1 = Button(
    get_login_page, text="Get Login", command=get_login_1, width=15
)
get_login_button_1.pack(pady=(10, 0))
login_label = Label(get_login_page, text="")
login_label.pack(pady=(10, 0))
back_button = Button(get_login_page, text="Back", command=go_to_main, width=15)
back_button.pack(pady=(10, 0))

edit_login_page = Frame(window)
selected_option_1 = StringVar(window)
selected_option_1.set(websites[0])
website_dropdown_1 = OptionMenu(edit_login_page, selected_option, *websites)
website_dropdown_1.pack(pady=(30, 0))
new_username_label = Label(edit_login_page, text="New Username")
new_username_label.pack(pady=(10, 0))
username_box_edit = Entry(edit_login_page)
username_box_edit.pack()
new_password_label = Label(edit_login_page, text="New Password")
new_password_label.pack(pady=(10, 0))
password_box_edit = Entry(edit_login_page)
password_box_edit.pack()
submit_button = Button(edit_login_page, text="Submit", command=edit_login_1, width=15)
submit_button.pack(pady=(10, 0))
back_button = Button(edit_login_page, text="Back", command=go_to_main, width=15)
back_button.pack(pady=(10, 0))

window.mainloop()
