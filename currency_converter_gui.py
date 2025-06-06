import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime

# Language dictionary (only English shown here for brevity, add others as needed)
LANGUAGES = {
    "English": {
        "title": "Currency Converter",
        "from": "From Currency:",
        "to": "To Currency:",
        "amount": "Amount:",
        "convert": "Convert",
        "result": "Result:",
        "error": "Error",
        "conversion_error": "Conversion Error",
        "filename": "Save filename:",
        "save_success": "Saved to file successfully!",
        "save_fail": "Failed to save file.",
    }
}

FLAG_EMOJIS = {
    "USD": "🇺🇸",
    "INR": "🇮🇳",
    "EUR": "🇪🇺",
    # Add more flags as needed
}

def get_currency_codes():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        codes = list(data["rates"].keys())
        codes.sort()
        return codes
    except:
        return list(FLAG_EMOJIS.keys())

def format_currency_with_flag(code):
    flag = FLAG_EMOJIS.get(code, "")
    return f"{flag} {code}"

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if "rates" in data and target_currency in data["rates"]:
        return data["rates"][target_currency]
    else:
        raise ValueError("Invalid currency code or API error")

def convert():
    base = base_combo.get().split()[-1]
    target = target_combo.get().split()[-1]
    try:
        amount = float(amount_entry.get())
        rate = get_exchange_rate(base, target)
        converted = amount * rate
        result_text = f"{amount:.2f} {base} = {converted:.2f} {target}"
        result_label.config(text=labels["result"] + " " + result_text)
        save_to_file(result_text)
    except ValueError as ve:
        messagebox.showerror(labels["conversion_error"], str(ve))
    except Exception as e:
        messagebox.showerror(labels["error"], "Something went wrong.\n" + str(e))

def save_to_file(text):
    filename = filename_entry.get().strip()
    if not filename:
        filename = "conversion_history.txt"
    if not filename.endswith(".txt"):
        filename += ".txt"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()} - {text}\n")
        messagebox.showinfo(labels["title"], labels["save_success"])
    except Exception:
        messagebox.showerror(labels["error"], labels["save_fail"])

def update_language(event):
    global labels
    selected_language = language_combo.get()
    labels = LANGUAGES[selected_language]
    root.title(labels["title"])
    title_label.config(text=labels["title"])
    from_label.config(text=labels["from"])
    to_label.config(text=labels["to"])
    amount_label.config(text=labels["amount"])
    convert_btn.config(text=labels["convert"])
    result_label.config(text=labels["result"])
    filename_label.config(text=labels["filename"])

root = tk.Tk()
root.geometry("480x420")
root.resizable(False, False)

labels = LANGUAGES["English"]
root.title(labels["title"])

title_label = ttk.Label(root, text=labels["title"], font=("Segoe UI", 16, "bold"))
title_label.pack(pady=10)

language_combo = ttk.Combobox(root, values=list(LANGUAGES.keys()), state="readonly")
language_combo.set("English")
language_combo.bind("<<ComboboxSelected>>", update_language)
language_combo.pack(pady=5)

test_label = ttk.Label(root, text="🇺🇸 🇮🇳 🇫🇷", font=("Segoe UI Emoji", 20))
test_label.pack(pady=5)

frame = ttk.Frame(root, padding=10)
frame.pack()

from_label = ttk.Label(frame, text=labels["from"])
from_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

base_combo = ttk.Combobox(frame, state="readonly", width=20, font=("Segoe UI Emoji", 11))
base_combo.grid(row=0, column=1, padx=5, pady=5)

to_label = ttk.Label(frame, text=labels["to"])
to_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

target_combo = ttk.Combobox(frame, state="readonly", width=20, font=("Segoe UI Emoji", 11))
target_combo.grid(row=1, column=1, padx=5, pady=5)

amount_label = ttk.Label(frame, text=labels["amount"])
amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

amount_entry = ttk.Entry(frame, width=22)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

filename_label = ttk.Label(frame, text=labels["filename"])
filename_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

filename_entry = ttk.Entry(frame, width=22)
filename_entry.grid(row=3, column=1, padx=5, pady=5)
filename_entry.insert(0, "conversion_history.txt")

convert_btn = ttk.Button(root, text=labels["convert"], command=convert)
convert_btn.pack(pady=15)

result_label = ttk.Label(root, text=labels["result"], font=("Segoe UI", 12))
result_label.pack(pady=5)

codes = get_currency_codes()
codes_with_flags = [format_currency_with_flag(code) for code in codes]

base_combo["values"] = codes_with_flags
target_combo["values"] = codes_with_flags
base_combo.set(format_currency_with_flag("USD"))
target_combo.set(format_currency_with_flag("INR"))

root.mainloop()
