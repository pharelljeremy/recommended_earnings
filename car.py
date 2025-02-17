import tkinter as tk
from tkinter import ttk, messagebox
import os

def calculate():
    try:
        monthly_payment = float(payment_entry.get())
        insurance = float(insurance_entry.get())
        gas = float(gas_entry.get())
        maintenance = float(maintenance_entry.get())
        
        total_monthly = monthly_payment + insurance + gas + maintenance
        recommended_income = total_monthly * 10  # Car expenses should be max 10% of income
        
        messagebox.showinfo("Result", f"Recommended Monthly Income: ${recommended_income:.2f}")
        
        # Save result to temp file
        with open("car_result.tmp", "w") as f:
            f.write(str(recommended_income))
            
        root.destroy()
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

root = tk.Tk()
root.title("Car Calculator")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Monthly Car Payment ($):").grid(row=0, column=0, pady=5)
payment_entry = ttk.Entry(frame)
payment_entry.grid(row=0, column=1, padx=10)

ttk.Label(frame, text="Monthly Insurance ($):").grid(row=1, column=0, pady=5)
insurance_entry = ttk.Entry(frame)
insurance_entry.grid(row=1, column=1, padx=10)

ttk.Label(frame, text="Monthly Gas ($):").grid(row=2, column=0, pady=5)
gas_entry = ttk.Entry(frame)
gas_entry.grid(row=2, column=1, padx=10)

ttk.Label(frame, text="Monthly Maintenance ($):").grid(row=3, column=0, pady=5)
maintenance_entry = ttk.Entry(frame)
maintenance_entry.grid(row=3, column=1, padx=10)

ttk.Button(frame, text="Calculate", command=calculate).grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()