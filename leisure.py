import tkinter as tk
from tkinter import ttk, messagebox
import os

def calculate():
    try:
        monthly_expense = float(expense_entry.get())
        recommended_income = monthly_expense / 0.2
        
        messagebox.showinfo("Result", f"Recommended Monthly Income: ${recommended_income:.2f}")
        
        # Save result to temp file
        with open("leisure_result.tmp", "w") as f:
            f.write(str(recommended_income))
            
        root.destroy()
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")

root = tk.Tk()
root.title("Leisure Calculator")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Monthly Leisure Expense ($):").grid(row=0, column=0, pady=10)
expense_entry = ttk.Entry(frame)
expense_entry.grid(row=0, column=1, padx=10)

ttk.Button(frame, text="Calculate", command=calculate).grid(row=1, column=0, columnspan=2, pady=20)

root.mainloop()