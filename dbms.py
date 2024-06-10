import sqlite3
from datetime import date
import streamlit as st

# Database operations
def initialize_db():
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                            customer_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone TEXT,
                            address TEXT
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Medicines (
                            medicine_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            manufacturer TEXT,
                            price REAL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Stock (
                            stock_id INTEGER PRIMARY KEY,
                            medicine_id INTEGER,
                            quantity INTEGER,
                            FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id)
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
                            sale_id INTEGER PRIMARY KEY,
                            customer_id INTEGER,
                            medicine_id INTEGER,
                            quantity INTEGER,
                            sale_date DATE,
                            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                            FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id)
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Pharmacists (
                            pharmacist_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            shift TEXT
                        )''')

        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def add_customer(name, phone, address):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Customers (name, phone, address) VALUES (?, ?, ?)', (name, phone, address))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def add_medicine(name, manufacturer, price):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Medicines (name, manufacturer, price) VALUES (?, ?, ?)', (name, manufacturer, price))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def add_stock(medicine_id, quantity):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Stock (medicine_id, quantity) VALUES (?, ?)', (medicine_id, quantity))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def make_sale(customer_id, medicine_id, quantity):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        sale_date = date.today().strftime('%Y-%m-%d')
        cursor.execute('INSERT INTO Sales (customer_id, medicine_id, quantity, sale_date) VALUES (?, ?, ?, ?)', (customer_id, medicine_id, quantity, sale_date))
        cursor.execute('UPDATE Stock SET quantity = quantity - ? WHERE medicine_id = ?', (quantity, medicine_id))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def view_customers():
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Customers')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def view_medicines():
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Medicines')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def view_stock():
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Stock')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def view_sales():
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Sales')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

# Initialize the database
initialize_db()

# Streamlit UI
st.title("Pharmacy Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Add Customer", "Add Medicine", "Add Stock", "Make Sale", "View Data"])

if page == "Add Customer":
    st.header("Add Customer")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    if st.button("Add Customer"):
        if name and phone and address:
            add_customer(name, phone, address)
            st.success("Customer added successfully")
        else:
            st.error("All fields are required")

elif page == "Add Medicine":
    st.header("Add Medicine")
    name = st.text_input("Medicine Name")
    manufacturer = st.text_input("Manufacturer")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    if st.button("Add Medicine"):
        if name and manufacturer and price:
            add_medicine(name, manufacturer, price)
            st.success("Medicine added successfully")
        else:
            st.error("All fields are required")

elif page == "Add Stock":
    st.header("Add Stock")
    medicine_id = st.number_input("Medicine ID", min_value=1, step=1)
    quantity = st.number_input("Quantity", min_value=0, step=1)
    if st.button("Add Stock"):
        if medicine_id and quantity >= 0:
            add_stock(medicine_id, quantity)
            st.success("Stock added successfully")
        else:
            st.error("All fields are required")

elif page == "Make Sale":
    st.header("Make Sale")
    customer_id = st.number_input("Customer ID", min_value=1, step=1)
    medicine_id = st.number_input("Medicine ID", min_value=1, step=1)
    quantity = st.number_input("Quantity", min_value=1, step=1)
    if st.button("Make Sale"):
        if customer_id and medicine_id and quantity:
            make_sale(customer_id, medicine_id, quantity)
            st.success("Sale recorded successfully")
        else:
            st.error("All fields are required")

elif page == "View Data":
    st.header("View Data")
    data_type = st.selectbox("View", ["Customers", "Medicines", "Stock", "Sales"])
    if data_type == "Customers":
        st.subheader("Customers")
        customers = view_customers()
        for customer in customers:
            st.write(customer)
    elif data_type == "Medicines":
        st.subheader("Medicines")
        medicines = view_medicines()
        for medicine in medicines:
            st.write(medicine)
    elif data_type == "Stock":
        st.subheader("Stock")
        stock = view_stock()
        for item in stock:
            st.write(item)
    elif data_type == "Sales":
        st.subheader("Sales")
        sales = view_sales()
        for sale in sales:
            st.write(sale)
