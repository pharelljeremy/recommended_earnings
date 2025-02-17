import tkinter as tk
from tkinter import ttk, messagebox
import os

def calculate():
    try:
        groceries = float(groceries_entry.get())
        dining = float(dining_entry.get())
        
        total_monthly = groceries + dining
        recommended_income = total_monthly / 0.2  # Food should be 20% of income
        
        messagebox.showinfo("Result", f"Recommended Monthly Income: ${recommended_income:.2f}")
        
        # Save result to temp file
        with open("food_result.tmp", "w") as f:
            f.write(str(recommended_income))
            
        root.destroy()
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

root = tk.Tk()
root.title("Food Calculator")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Monthly Groceries ($):").grid(row=0, column=0, pady=5)
groceries_entry = ttk.Entry(frame)
groceries_entry.grid(row=0, column=1, padx=10)

ttk.Label(frame, text="Monthly Dining Out ($):").grid(row=1, column=0, pady=5)
dining_entry = ttk.Entry(frame)
dining_entry.grid(row=1, column=1, padx=10)

ttk.Button(frame, text="Calculate", command=calculate).grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()