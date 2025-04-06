import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", 
                background="#fdf6e3", 
                foreground="#000000", 
                rowheight=25, 
                fieldbackground="#fdf6e3")
style.map('Treeview', background=[('selected', '#d1e7dd')])
entry_name = tk.Entry(frame, width=40, bg="#ffffff", fg="#000000")
entry_ingredients = tk.Text(frame, width=30, height=4, bg="#fff8dc", fg="#222")
entry_instructions = tk.Text(frame, width=30, height=4, bg="#fff8dc", fg="#222")
entry_category = tk.Entry(frame, width=40, bg="#ffffff", fg="#000000")


try:
    import mysql.connector
except ModuleNotFoundError:
    messagebox.showerror("Error", "MySQL Connector module is not installed. Install it using 'pip install mysql-connector-python'")
    exit()

# Database Connection
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Change if needed
            password="123Joel...",  # Change if needed
            database="recipe_manager"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Function to add a recipe
def add_recipe():
    name = entry_name.get()
    ingredients = entry_ingredients.get("1.0", tk.END).strip()
    instructions = entry_instructions.get("1.0", tk.END).strip()
    category = entry_category.get()
    
    if not (name and ingredients and instructions and category):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    sql = "INSERT INTO recipes (name, ingredients, instructions, category) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, ingredients, instructions, category))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Recipe added successfully!")
    clear_fields()

# Function to clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_ingredients.delete("1.0", tk.END)
    entry_instructions.delete("1.0", tk.END)
    entry_category.delete(0, tk.END)

# Function to view recipes
def view_recipes():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM recipes")
    rows = cursor.fetchall()
    conn.close()
    
    view_window = tk.Toplevel(root)
    view_window.title("All Recipes")
    
    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Category"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.pack(fill=tk.BOTH, expand=True)
    
    for row in rows:
        tree.insert("", tk.END, values=row)

# Function to search recipes by category
def search_by_category():
    category = entry_search.get().strip()
    if not category:
        messagebox.showerror("Error", "Please enter a category!")
        return
    
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM recipes WHERE category=%s", (category,))
    rows = cursor.fetchall()
    conn.close()
    
    result_window = tk.Toplevel(root)
    result_window.title(f"Recipes in {category}")
    
    tree = ttk.Treeview(result_window, columns=("ID", "Name"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.pack(fill=tk.BOTH, expand=True)
    
    for row in rows:
        tree.insert("", tk.END, values=row)

# GUI Setup
root = tk.Tk()
root.title("Recipe Manager")

# Recipe Entry Form
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Recipe Name:").grid(row=0, column=0)
entry_name = tk.Entry(frame, width=40)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Ingredients:").grid(row=1, column=0)
entry_ingredients = tk.Text(frame, width=30, height=4)
entry_ingredients.grid(row=1, column=1)

tk.Label(frame, text="Instructions:").grid(row=2, column=0)
entry_instructions = tk.Text(frame, width=30, height=4)
entry_instructions.grid(row=2, column=1)

tk.Label(frame, text="Category:").grid(row=3, column=0)
entry_category = tk.Entry(frame, width=40)
entry_category.grid(row=3, column=1)

tk.Button(frame, text="Add Recipe", command=add_recipe).grid(row=4, column=0, columnspan=2, pady=5)

# View Recipes Button
tk.Button(root, text="View All Recipes", command=view_recipes).pack(pady=5)

# Search by Category
frame_search = tk.Frame(root)
frame_search.pack(pady=5)

tk.Label(frame_search, text="Search by Category:").grid(row=0, column=0)
entry_search = tk.Entry(frame_search, width=30)
entry_search.grid(row=0, column=1)
tk.Button(frame_search, text="Search", command=search_by_category).grid(row=0, column=2)

root.mainloop()
