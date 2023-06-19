from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

SAVED_EMAIL = "email@example.com"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    ws = website_entry.get().title()
    id = email_entry.get()
    pwd = password_entry.get()
    new_data = {ws:{"Email":id, "Password":pwd}}

    if len(ws) == 0 or len(id) == 0 or len(pwd) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        no_flag = messagebox.askokcancel(title=ws, message=f"These are the details entered:\n\nID: {id}\nPassword: {pwd}\n\nIs it okay to save?")
        if no_flag:
            try:
                with open("data.json", mode="r") as file:
                    # read old data
                    data = json.load(file)
            except FileNotFoundError:
                # runs if file does not exist
                with open("data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # update old data
                data.update(new_data)
                # upload updated data
                with open("data.json", mode="w") as file:
                    json.dump(data, file, indent=4)
            finally:
                password_entry.delete(0,END)
                website_entry.delete(0,END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    ws = website_entry.get().title()
    try:
        with open("Password Manager\data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="File Error", message="No data file found.")
    else:
        if ws in data:
            em = data[ws]["Email"]
            pwd = data[ws]["Password"]
            messagebox.showinfo(title=ws, message=f"Email: {em}\n\nPassword: {pwd}")
        else:
            messagebox.showinfo(title="Website Error", message=f'No details for "{ws}" exist.\n\nCheck spelling!')

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file=r"Password Manager\logo.png")
canvas.create_image(100,100, image=img)
canvas.grid(row=0,column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1,column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2,column=0)
password_label = Label(text="Password:")
password_label.grid(row=3,column=0)

# Entries
website_entry = Entry(width=34)
website_entry.grid(row=1,column=1)
website_entry.focus()
email_entry = Entry(width=53)
email_entry.insert(0,SAVED_EMAIL)
email_entry.grid(row=2,column=1,columnspan=2)
password_entry = Entry(width=34)
password_entry.grid(row=3, column=1)

# Button
password_gen_button = Button(text="Generate Password", command=gen_password)
password_gen_button.grid(row=3, column=2)
add_button = Button(text="Add", width=45, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()