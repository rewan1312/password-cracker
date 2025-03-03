import tkinter as tk
from tkinter import messagebox
import itertools
import string
import os


PASSWORD_FILE = "password.txt"


root = tk.Tk()
root.title("Password Cracker")
root.geometry("500x450")
root.configure(bg="#0A2647")


USER_DATABASE = {
    "elwardany": "password",
    "rewan": "trustno1",
    "charlie": "sunshine",
    "david": "master",
    "eve": "dragon"
}

def load_passwords():
  
    if not os.path.exists(PASSWORD_FILE):
        messagebox.showerror("Error", f"File '{PASSWORD_FILE}' not found! Please make sure it is in the same directory.")
        return []
    
    try:
        with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file '{PASSWORD_FILE}': {e}")
        return []

def update_status(message):
  
    status_text.insert(tk.END, message + "\n")
    status_text.see(tk.END)
    root.update_idletasks()

def dictionary_attack(password):

    dictionary = load_passwords()
    
    if not dictionary:
        update_status("⚠️ No dictionary words found!")
        return None

    for word in dictionary:
        update_status(f"Trying: {word}")
        if word == password:
            return word
    return None

def brute_force_attack(password):
   
    if len(password) != 5 or not password.isalpha():
        update_status("⚠️ Brute Force Attack skipped (password not 5 letters).")
        return None

    chars = string.ascii_letters  
    length = 5  
    for attempt in itertools.product(chars, repeat=length):
        attempt_str = "".join(attempt)
        update_status(f"Trying: {attempt_str}")

        if attempt_str == password:
            return attempt_str
    return None

def start_attack():
    username = username_entry.get().strip()

    if not username:
        messagebox.showerror("Error", "Username field cannot be empty!")
        return

    update_status(f"🔎 Target Username: {username}")

    if username not in USER_DATABASE:
        messagebox.showerror("Error", "❌ Username not found in database!")
        return  #
    password = USER_DATABASE[username]

    update_status("🚀 Starting Dictionary Attack...")

    cracked_password = dictionary_attack(password)
    if cracked_password:
        messagebox.showinfo("Success", f"✅ Password found using Dictionary Attack: {cracked_password}")
        return

    update_status("❌ Dictionary Attack failed. Switching to Brute Force...")

  
    cracked_password = brute_force_attack(password)
    if cracked_password:
        messagebox.showinfo("Success", f"✅ Password cracked using Brute Force: {cracked_password}")
    else:
        messagebox.showerror("Failure", "❌ Brute Force Attack failed!")


tk.Label(root, text="🔐", font=("Arial", 40), bg="#0A2647", fg="#A0D2EB").pack(pady=5)
tk.Label(root, text="Password Cracker", font=("Arial", 20, "bold"), fg="#A0D2EB", bg="#0A2647").pack(pady=5)

tk.Label(root, text="Enter Username:", font=("Arial", 14), fg="#A0D2EB", bg="#0A2647").pack()
username_entry = tk.Entry(root, font=("Arial", 14), bg="#E0E0E0", fg="black", width=30, relief="flat")
username_entry.pack(pady=5)

attack_button = tk.Button(root, text="Start Attack", font=("Arial", 14, "bold"), bg="#007BFF", fg="white", relief="flat", width=20, height=2, command=start_attack)
attack_button.pack(pady=10)

status_text = tk.Text(root, height=12, width=55, bg="#E0E0E0", fg="black", relief="flat")
status_text.pack(pady=5)


root.mainloop()
