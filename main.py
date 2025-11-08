import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import json
from pathlib import Path
import os
import time

class IncomeCalculatorMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Income Calculator Suite")
        
        # Define the base directory and calculator paths
        self.base_dir = "/Users/jeremypharell/Desktop/£/Code/Type_Shi/recommended_earnings"
        
        self.calculator_paths = {
            "Leisure": os.path.join(self.base_dir, "leisure.py"),
            "Housing": os.path.join(self.base_dir, "housing.py"),
            "Car": os.path.join(self.base_dir, "car.py"),
            "Savings": os.path.join(self.base_dir, "savings.py"),
            "Food": os.path.join(self.base_dir, "food.py")
        }
        
        # Store monthly recommendations
        self.recommendations = {
            "Leisure": 0,
            "Housing": 0,
            "Car": 0,
            "Savings": 0,
            "Food": 0
        }
        
        # Create main frame with dark theme
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create calculator buttons
        ttk.Label(self.main_frame, text="Select a calculator to run:", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=10, columnspan=2)
        
        row = 1
        for calculator_name in self.calculator_paths.keys():
            self.create_calculator_button(f"{calculator_name} Calculator", calculator_name, row)
            row += 1
        
        # Create results display
        ttk.Separator(self.main_frame).grid(row=6, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Current Recommendations", padding="10")
        self.results_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.results_labels = {}
        for idx, category in enumerate(self.recommendations.keys()):
            ttk.Label(self.results_frame, text=f"{category}:").grid(row=idx, column=0, padx=5, pady=2, sticky=tk.W)
            self.results_labels[category] = ttk.Label(self.results_frame, text="$0.00")
            self.results_labels[category].grid(row=idx, column=1, padx=5, pady=2, sticky=tk.E)
        
        # Total display
        ttk.Separator(self.results_frame).grid(row=len(self.recommendations), column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.total_monthly_label = ttk.Label(self.results_frame, text="Total Monthly:", font=('Helvetica', 10, 'bold'))
        self.total_monthly_label.grid(row=len(self.recommendations) + 1, column=0, sticky=tk.W)
        
        self.total_monthly_amount = ttk.Label(self.results_frame, text="$0.00", font=('Helvetica', 10, 'bold'))
        self.total_monthly_amount.grid(row=len(self.recommendations) + 1, column=1, sticky=tk.E)
        
        self.total_yearly_label = ttk.Label(self.results_frame, text="Total Yearly:", font=('Helvetica', 10, 'bold'))
        self.total_yearly_label.grid(row=len(self.recommendations) + 2, column=0, sticky=tk.W)
        
        self.total_yearly_amount = ttk.Label(self.results_frame, text="$0.00", font=('Helvetica', 10, 'bold'))
        self.total_yearly_amount.grid(row=len(self.recommendations) + 2, column=1, sticky=tk.E)
        
        # Load previous values if they exist
        self.load_saved_values()
        
        # Clear button
        ttk.Button(self.main_frame, text="Clear All Values", command=self.clear_values).grid(row=8, column=0, columnspan=2, pady=10)

    def create_calculator_button(self, text, calculator_type, row):
        btn = ttk.Button(self.main_frame, text=text, command=lambda: self.run_calculator(calculator_type))
        btn.grid(row=row, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

    def run_calculator(self, calculator_type):
        try:
            # Get the path for the specific calculator
            calculator_path = self.calculator_paths[calculator_type]
            
            # Create a temp file path for this calculator
            temp_file = os.path.join(self.base_dir, f"{calculator_type.lower()}_result.tmp")
            
            # Check if the file exists
            if not os.path.exists(calculator_path):
                messagebox.showerror("Error", f"Calculator file not found: {calculator_path}")
                return
                
            # Run the calculator script
            process = subprocess.Popen([sys.executable, calculator_path])
            
            # Wait for the process to complete
            process.wait()
            
            # Check for the temp file
            start_time = time.time()
            while time.time() - start_time < 5:  # Wait up to 5 seconds
                if os.path.exists(temp_file):
                    try:
                        with open(temp_file, 'r') as f:
                            result = float(f.read().strip())
                        os.remove(temp_file)  # Clean up
                        self.recommendations[calculator_type] = result
                        self.update_display()
                        self.save_values()
                        return
                    except:
                        pass
                time.sleep(0.1)
            
            # If we get here, we didn't get a result
            messagebox.showinfo("No Result", "No result was received from the calculator.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run calculator: {str(e)}")

    def update_display(self):
        # Update individual labels
        for category, amount in self.recommendations.items():
            self.results_labels[category].config(text=f"${amount:,.2f}")
        
        # Calculate and update totals
        monthly_total = sum(self.recommendations.values())
        yearly_total = monthly_total * 12
        
        self.total_monthly_amount.config(text=f"${monthly_total:,.2f}")
        self.total_yearly_amount.config(text=f"${yearly_total:,.2f}")

    def save_values(self):
        try:
            save_path = os.path.join(self.base_dir, 'calculator_values.json')
            with open(save_path, 'w') as f:
                json.dump(self.recommendations, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save values: {str(e)}")

    def load_saved_values(self):
        try:
            save_path = os.path.join(self.base_dir, 'calculator_values.json')
            if os.path.exists(save_path):
                with open(save_path, 'r') as f:
                    self.recommendations.update(json.load(f))
                self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load saved values: {str(e)}")

    def clear_values(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all values?"):
            self.recommendations = dict.fromkeys(self.recommendations, 0)
            self.update_display()
            self.save_values()

def main():
    root = tk.Tk()
    app = IncomeCalculatorMain(root)
    root.mainloop()

if __name__ == "__main__":
    main()


#bruh wadis
