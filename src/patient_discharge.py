import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

PATIENT_FILE = 'data/patients.json'
DISCHARGED_STACK = []

def load_patients():
    if not os.path.exists(PATIENT_FILE):
        return []
    with open(PATIENT_FILE, 'r') as f:
        return json.load(f)

def save_patients(data):
    with open(PATIENT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def search_patient(patients, key):
    results = []
    for p in patients:
        if str(p.get("id")) == key or p.get("name", "").lower() == key.lower():
            results.append(p)
    return results

def discharge_patient(patients, patient_key):
    for i, p in enumerate(patients):
        if str(p["id"]) == str(patient_key) or p["name"].lower() == str(patient_key).lower():
            DISCHARGED_STACK.append(p)
            del patients[i]
            save_patients(patients)
            return p
    return None

def launch_discharge_module():
    window = tk.Toplevel()
    window.title("Patient Discharge Module")
    window.geometry("640x550")
    window.resizable(False, False)

    # Background image
    try:
        bg_image = Image.open("data/hospital_background.jpg")
        bg_image = bg_image.resize((800, 600))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        print("✅ Background image loaded")
    except Exception as e:
        print("❌ Background image not found or failed to load:", e)

    label_font = ("Segoe UI", 12, "bold")
    entry_font = ("Segoe UI", 11)
    button_font = ("Segoe UI", 10, "bold")
    text_font = ("Consolas", 10)

    tk.Label(window, text="Enter Patient Name or ID:",
             font=label_font, bg="#e6f2ff", fg="#003366").pack(pady=(20, 8))

    entry_container = tk.Frame(window, bg="#e6f2ff")
    entry_container.pack()
    entry_search = tk.Entry(entry_container, font=entry_font, width=40,
                            bd=2, relief="solid", bg="#ffffff", highlightthickness=1,
                            highlightbackground="#cccccc")
    entry_search.pack(pady=5, ipady=5, ipadx=5)

    def create_button(text, command):
        return tk.Button(window, text=text, command=command,
                         font=button_font, bg="#007acc", fg="white",
                         activebackground="#005f99", activeforeground="white",
                         width=30, relief="flat", bd=3, cursor="hand2")

    def handle_search():
        key = entry_search.get().strip()
        fresh_patients = load_patients()
        results = search_patient(fresh_patients, key)
        result_box.config(state="normal")
        result_box.delete('1.0', tk.END)
        if results:
            for p in results:
                result_box.insert(tk.END, f"🩺 ID: {p['id']}\n👤 Name: {p['name']}\n🎂 Age: {p['age']}\n\n")
        else:
            result_box.insert(tk.END, "⚠️ No matching patient found.")
        result_box.config(state="disabled")

    def handle_discharge():
        key = entry_search.get().strip()
        updated_patients = load_patients()
        result = discharge_patient(updated_patients, key)
        result_box.config(state="normal")
        result_box.delete('1.0', tk.END)
        if result:
            result_box.insert(tk.END, f"✅ Patient {result['name']} (ID: {result['id']}) discharged.\n")
        else:
            result_box.insert(tk.END, "⚠️ Patient not found or already discharged.")
        result_box.config(state="disabled")

    def show_recent_discharges():
        result_box.config(state="normal")
        result_box.delete('1.0', tk.END)
        if DISCHARGED_STACK:
            result_box.insert(tk.END, "🕓 Recent Discharges:\n\n")
            for p in reversed(DISCHARGED_STACK[-10:]):
                result_box.insert(tk.END, f"🩺 ID: {p['id']}, 👤 Name: {p['name']}\n")
        else:
            result_box.insert(tk.END, "⚠️ No discharges yet.")
        result_box.config(state="disabled")

    create_button("Search", handle_search).pack(pady=3)
    create_button("Discharge", handle_discharge).pack(pady=3)
    create_button("Show Recent Discharges", show_recent_discharges).pack(pady=3)

    text_frame = tk.Frame(window, bg="#e6f2ff")
    text_frame.pack(pady=(10, 15))

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_box = tk.Text(text_frame, height=12, width=70,
                         font=text_font, bd=2, relief="sunken", bg="#ffffff",
                         yscrollcommand=scrollbar.set, wrap="word")
    result_box.pack(side=tk.LEFT)
    scrollbar.config(command=result_box.yview)

    result_box.config(state="disabled")

    window.mainloop()
