import tkinter as tk
from tkinter import messagebox
import itertools
import string
import os

PASSWORD_FILE = "password_directory.txt"

root = tk.Tk()
root.title("Security Tester")
root.geometry("550x500")
root.configure(bg="#121212")

USER_DATABASE = {
    "fatma": "welcome",
    "ahmed": "shadow",
    "sara": "ninja",
    "khaled": "mustang",
    "marwa": "abcde"
}

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        messagebox.showerror("Error",
                             f"File '{PASSWORD_FILE}' not found! Please make sure it is in the same directory.")
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
        update_status("No dictionary words found!")
        return None
    for word in dictionary:
        update_status(f"Trying: {word}")
        if word == password:
            return word
    return None

def brute_force_attack(password):
    if len(password) != 5 or not password.isalpha():
        update_status("Brute Force Attack skipped (password not 5 letters).")
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
    update_status(f"Target Username: {username}")
    if username not in USER_DATABASE:
        messagebox.showerror("Error", "Username not found in database!")
        return
    password = USER_DATABASE[username]
    update_status("Starting Dictionary Attack...")
    cracked_password = dictionary_attack(password)
    if cracked_password:
        messagebox.showinfo("Success", f"Password found using Dictionary Attack: {cracked_password}")
        return
    update_status("Dictionary Attack failed. Switching to Brute Force...")
    cracked_password = brute_force_attack(password)
    if cracked_password:
        messagebox.showinfo("Success", f"Password cracked using Brute Force: {cracked_password}")
    else:
        messagebox.showerror("Failure", "Brute Force Attack failed!")

title_label = tk.Label(root, text="Security Tester", font=("Arial", 22, "bold"), fg="#00ADB5", bg="#121212")
title_label.pack(pady=5)

frame = tk.Frame(root, bg="#222831", padx=20, pady=15)
frame.pack(pady=10)

tk.Label(frame, text="Enter Username:", font=("Arial", 14), fg="#EEEEEE", bg="#222831").pack()
username_entry = tk.Entry(frame, font=("Arial", 14), bg="#393E46", fg="white", width=30, relief="flat", insertbackground="white")
username_entry.pack(pady=5)

attack_button = tk.Button(root, text="Start Attack", font=("Arial", 14, "bold"), bg="#00ADB5", fg="black", relief="flat", width=20, height=2, command=start_attack)
attack_button.pack(pady=15)

status_frame = tk.Frame(root, bg="#222831", padx=10, pady=10)
status_frame.pack()

status_text = tk.Text(status_frame, height=12, width=55, bg="#393E46", fg="white", relief="flat", insertbackground="white")
status_text.pack()

root.mainloop()