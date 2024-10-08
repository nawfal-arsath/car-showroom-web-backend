import sqlite3
import tkinter as tk
from tkinter import ttk
import mysql.connector
# Create a SQLite database and connect to it
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*****",
    database="bike",
    port='3306'
)

# Create tables if they don't exist
'''cursor.execute()
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT
    )
)'''
cursor = conn.cursor()
cursor.execute("CREATE TABLE Bike (id int PRIMARY KEY AUTOINCREMENT,brand varchar(30),model varchar(30),year int,price numeric(7,2),available int)")

 '''cursor.execute(
    CREATE TABLE IF NOT EXISTS Transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        bike_id INTEGER,
        sale_date DATE,
        FOREIGN KEY (customer_id) REFERENCES Customers(id),
        FOREIGN KEY (bike_id) REFERENCES Bike(id)
    )
)'''

conn.commit()

# Function to insert a new customer into the database
def add_customer():
    name = customer_name_entry.get()
    phone = customer_phone_entry.get()
    email = customer_email_entry.get()

    cursor.execute('''
        INSERT INTO Customers (name, phone, email)
        VALUES (?, ?, ?)
    ''', (name, phone, email))

    conn.commit()
    update_customer_list()

# Function to update the customer list
def update_customer_list():
    customer_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    for customer in customers:
        customer_list.insert(tk.END, f"{customer[1]} - {customer[2]}, {customer[3]}")

# Function to insert a new bike into the database
def add_bike():
    brand = bike_brand_entry.get()
    model = bike_model_entry.get()
    year = int(bike_year_entry.get())
    price = float(bike_price_entry.get())
    available = True  # Assume all newly added bike are available

    cursor.execute('''
        INSERT INTO Bike (brand, model, year, price, available)
        VALUES (?, ?, ?, ?, ?)
    ''', (brand, model, year, price, available))

    conn.commit()
    update_bike_list()

# Function to update the bike list
def update_bike_list():
    bike_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM Bike")
    bike = cursor.fetchall()
    for bike in bike:
        status = "Available" if bike[5] else "Not Available"
        bike_list.insert(tk.END, f"{bike[1]} {bike[2]} ({bike[3]}), Price: ${bike[4]:,.2f}, {status}")

# Function to handle the sale of a bike
def sell_bike():
    selected_customer = customer_list.curselection()
    selected_bike = bike_list.curselection()

    if selected_customer and selected_bike:
        customer_id = cursor.execute("SELECT id FROM Customers").fetchall()[selected_customer[0]][0]
        bike_id = cursor.execute("SELECT id FROM Bike").fetchall()[selected_bike[0]][0]

        cursor.execute('''
            INSERT INTO Transactions (customer_id, bike_id, sale_date)
            VALUES (?, ?, CURRENT_DATE)
        ''', (customer_id, bike_id))

        cursor.execute("UPDATE Bike SET available = 0 WHERE id = ?", (bike_id,))
        conn.commit()
        update_bike_list()

# Create the main application window
app = tk.Tk()
app.title("Bike Showroom")

# Create and place input fields and labels for customers
customer_name_label = tk.Label(app, text="Name:")
customer_name_label.grid(row=0, column=0, padx=10, pady=10)
customer_name_entry = tk.Entry(app)
customer_name_entry.grid(row=0, column=1, padx=10, pady=10)

customer_phone_label = tk.Label(app, text="Phone:")
customer_phone_label.grid(row=1, column=0, padx=10, pady=10)
customer_phone_entry = tk.Entry(app)
customer_phone_entry.grid(row=1, column=1, padx=10, pady=10)

customer_email_label = tk.Label(app, text="Email:")
customer_email_label.grid(row=2, column=0, padx=10, pady=10)
customer_email_entry = tk.Entry(app)
customer_email_entry.grid(row=2, column=1, padx=10, pady=10)

add_customer_button = tk.Button(app, text="Add Customer", command=add_customer)
add_customer_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create and place the customer list
customer_list = tk.Listbox(app, height=10, width=50)
customer_list.grid(row=4, column=0, columnspan=2, pady=10)
#update_customer_list()

# Create and place input fields and labels for bike
bike_brand_label = tk.Label(app, text="Brand:")
bike_brand_label.grid(row=5, column=0, padx=10, pady=10)
bike_brand_entry = tk.Entry(app)
bike_brand_entry.grid(row=5, column=1, padx=10, pady=10)

bike_model_label = tk.Label(app, text="Model:")
bike_model_label.grid(row=6, column=0, padx=10, pady=10)
bike_model_entry = tk.Entry(app)
bike_model_entry.grid(row=6, column=1, padx=10, pady=10)

bike_year_label = tk.Label(app, text="Year:")
bike_year_label.grid(row=7, column=0, padx=10, pady=10)
bike_year_entry = tk.Entry(app)
bike_year_entry.grid(row=7, column=1, padx=10, pady=10)

bike_price_label = tk.Label(app, text="Price:")
bike_price_label.grid(row=8, column=0, padx=10, pady=10)
bike_price_entry = tk.Entry(app)
bike_price_entry.grid(row=8, column=1, padx=10, pady=10)

add_bike_button = tk.Button(app, text="Add Bike", command=add_bike)
add_bike_button.grid(row=9, column=0, columnspan=2, pady=10)

# Create and place the bike list
bike_list = tk.Listbox(app, height=10, width=50)
bike_list.grid(row=10, column=0, columnspan=2, pady=10)
#update_bike_list()

# Create and place the sell bike button
sell_bike_button = tk.Button(app, text="Sell Bike", command=sell_bike)
sell_bike_button.grid(row=11, column=0, columnspan=2, pady=10)

# Run the application
app.mainloop()

# Close the database connection when the application is closed
conn.close()
