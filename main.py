from io import text_encoding
from re import search
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def pwd_generator():
    if len(pwd_ent.get()) == 0:
        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_list = [random.choice(letters) for _ in range(nr_letters)]
        password_list += [random.choice(symbols) for _ in range(nr_symbols)]
        password_list += [random.choice(numbers) for _ in range(nr_numbers)]
        random.shuffle(password_list)

        password = "".join(password_list)
        pwd_ent.insert(0,password)
        # For copy pwd to clipboard
        pyperclip.copy(password)
    else:
        messagebox.showinfo(title="Warning", message = "Password not empty!!!")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pwd():
    usr_name  = usr_ent.get()
    pwd = pwd_ent.get()
    web = web_ent.get()
    new_data = {
        web:{
            "Username":usr_name,
            "Password":pwd,
        }
    }
    if usr_name and pwd and web:
        is_ok = messagebox.askokcancel(title = web, message = f"Information entered: \nUsername: {usr_name} \nPassword:{pwd} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                usr_ent.delete(0,END)
                pwd_ent.delete(0, END)
                web_ent.delete(0, END)
    else:
        messagebox.showinfo(title = "Warning", message = f"Empty box detected")

def find_pwd():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Warning!!", message="No File Found!!")
    else:
        input_web = web_ent.get()
        if len(input_web) != 0 :
            try:
                usr_name = data[input_web]["Username"]
                pwd = data[input_web]["Password"]
            except KeyError:
                messagebox.showinfo(title="Warning!!",
                                    message=f"Passwords for {input_web} is not saved yet!!! Can't find it!!!")
            else:
                messagebox.showinfo(title="Succeed!!",
                                    message=f"Website: {input_web} \nUsername :{usr_name} \nPasswords: {pwd}")
# ---------------------------- UI SETUP ------------------------------- #

# Setup window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
# Setup canvas
img_name = "logo.png"
img = PhotoImage(file = img_name)
canvas = Canvas(width=200, height=200)
canvas.create_image(100,100,image = img)
canvas.grid(column = 1,row = 0)


# create buttons

gen_button = Button(text="Generate Password", command = pwd_generator)
gen_button.grid(column = 2, row = 3)
add_button = Button(text = "Add", width =36, command = save_pwd)
add_button.grid(column = 1, columnspan = 2, row = 4)

search_button = Button(text = "Search", command = find_pwd)
search_button.grid(column = 3, row = 1)
# Create entries

web_ent = Entry( width = 31)
web_ent.grid(column = 1, row = 1, columnspan = 2)
web_ent.focus()

usr_ent = Entry( width = 31)
usr_ent.grid(column = 1, row = 2, columnspan = 2)

pwd_ent = Entry( width = 21)
pwd_ent.grid(column = 1, row = 3)

# Create Label
web_label = Label(text = " Website:")
web_label.grid(column = 0, row = 1)

usr_label = Label(text = " Email/username:")
usr_label.grid(column = 0, row = 2)

pwd_label = Label(text = " Password:")
pwd_label.grid(column = 0, row = 3)


window.mainloop()