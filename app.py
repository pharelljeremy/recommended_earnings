from flask import Flask, render_template, request, redirect, url_for
import subprocess
import sys
import os
import time
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Define the base directory and calculator paths
base_dir = "/Users/jeremypharell/Desktop/£/Code/Type_Shi/recommended_earnings"
calculator_paths = {
    "Leisure": os.path.join(base_dir, "leisure.py"),
    "Housing": os.path.join(base_dir, "housing.py"),
    "Car": os.path.join(base_dir, "car.py"),
    "Savings": os.path.join(base_dir, "savings.py"),
    "Food": os.path.join(base_dir, "food.py")
}

def run_calculator(calculator_type):
    try:
        calculator_path = calculator_paths[calculator_type]
        temp_file = os.path.join(base_dir, f"{calculator_type.lower()}_result.tmp")

        if not os.path.exists(calculator_path):
            return f"Calculator file not found: {calculator_path}"

        process = subprocess.Popen([sys.executable, calculator_path])
        process.wait()

        start_time = time.time()
        while time.time() - start_time < 5:  # Wait up to 5 seconds
            if os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    result = float(f.read().strip())
                os.remove(temp_file)  # Clean up
                return result
            time.sleep(0.1)

        return "No result received from the calculator."
    except Exception as e:
        return f"Failed to run calculator: {str(e)}"

@app.route('/')
def index():
    conn = get_db_connection()
    recommendations = conn.execute('SELECT * FROM recommendations').fetchall()
    conn.close()

    # Calculate totals
    monthly_total = sum(rec['amount'] for rec in recommendations)
    yearly_total = monthly_total * 12

    return render_template('index.html', recommendations=recommendations, monthly_total=monthly_total, yearly_total=yearly_total)

@app.route('/run_calculator/<category>')
def run_calculator_route(category):
    result = run_calculator(category)
    if isinstance(result, float):
        conn = get_db_connection()
        conn.execute('INSERT INTO recommendations (category, amount) VALUES (?, ?)', (category, result))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_recommendation(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recommendations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/clear')
def clear_recommendations():
    conn = get_db_connection()
    conn.execute('DELETE FROM recommendations')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)