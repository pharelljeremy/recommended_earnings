import tkinter as tk
from tkinter import ttk, messagebox
import os

def calculate():
    try:
        if payment_type.get() == "rent":
            monthly_payment = float(rent_entry.get())
        else:
            mortgage = float(mortgage_entry.get())
            monthly_payment = mortgage
            
        utilities = float(utilities_entry.get())
        total_monthly = monthly_payment + utilities
        recommended_income = total_monthly / 0.3
        
        messagebox.showinfo("Result", f"Recommended Monthly Income: ${recommended_income:.2f}")
        
        # Save result to temp file
        with open("housing_result.tmp", "w") as f:
            f.write(str(recommended_income))
            
        root.destroy()
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

def toggle_payment():
    if payment_type.get() == "rent":
        mortgage_entry.grid_remove()
        mortgage_label.grid_remove()
        rent_entry.grid(row=1, column=1, padx=10)
        rent_label.grid(row=1, column=0)
    else:
        rent_entry.grid_remove()
        rent_label.grid_remove()
        mortgage_entry.grid(row=1, column=1, padx=10)
        mortgage_label.grid(row=1, column=0)

root = tk.Tk()
root.title("Housing Calculator")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

payment_type = tk.StringVar(value="rent")
ttk.Radiobutton(frame, text="Rent", variable=payment_type, value="rent", command=toggle_payment).grid(row=0, column=0)
ttk.Radiobutton(frame, text="Mortgage", variable=payment_type, value="mortgage", command=toggle_payment).grid(row=0, column=1)

rent_label = ttk.Label(frame, text="Monthly Rent ($):")
rent_label.grid(row=1, column=0)
rent_entry = ttk.Entry(frame)
rent_entry.grid(row=1, column=1, padx=10)

mortgage_label = ttk.Label(frame, text="Monthly Mortgage ($):")
mortgage_entry = ttk.Entry(frame)

ttk.Label(frame, text="Monthly Utilities ($):").grid(row=2, column=0)
utilities_entry = ttk.Entry(frame)
utilities_entry.grid(row=2, column=1, padx=10)

ttk.Button(frame, text="Calculate", command=calculate).grid(row=3, column=0, columnspan=2, pady=20)

toggle_payment()
root.mainloop()