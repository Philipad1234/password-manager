from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_value = website_entry.get()
    email_value = email_entry.get()
    password_value = password_entry.get()
    new_data = {
        website_value: {
            "email": email_value,
            "password": password_value,
        }
    }

    if len(website_value) == 0 or len(password_value) == 0:
        messagebox.showinfo(title='Oops!', message='Please do not leave any fields empty!')
    else:
        try:
            with open('data.json', 'r') as datafile:
                data = json.load(datafile)
        except FileNotFoundError:
            with open('data.json', 'w') as datafile:
                json.dump(new_data, datafile, indent=4)
        else:
            data.update(new_data)
            with open('data.json', 'w') as datafile:
                json.dump(data, datafile, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_value = website_entry.get()
    try:
        with open('data.json') as datafile:
            data = json.load(datafile)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No data file found.')
    else:
        if website_value in data:
            email_value = data[website_value]['email']
            password_value = data[website_value]['password']
            messagebox.showinfo(title='Success', message=f'Website: {email_value}\nPassword: {password_value}')
        else:
            messagebox.showinfo(title='Error', message=f'No details for {website_value} found.')


# ---------------------------- UI SETUP ------------------------------- #
# window setup
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# canvas setup
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# labels setup
website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

email_label = Label(text='Email/Username:')
email_label.grid(column=0, row=2)

password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

# inputs setup
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=36)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, 'name@mail.com')

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# buttons setup
password_button = Button(text='Generate Password', command=generate_password)
password_button.grid(column=2, row=3)

search_button = Button(text='Search', width=15, command=find_password)
search_button.grid(column=2, row=1)

add_button = Button(text='Add', width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
