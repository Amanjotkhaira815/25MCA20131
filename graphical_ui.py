import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --------------------- DATABASE CONNECTION ---------------------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # change this
            password="Amanjot@4509",  # change this
            database="bookstore"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


# --------------------- CRUD FUNCTIONS: BOOKS ---------------------
def load_books():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        for row in tree_books.get_children():
            tree_books.delete(row)
        for r in rows:
            tree_books.insert("", tk.END, values=r)
        conn.close()

def add_book():
    b_name = entry_bname.get()
    author = entry_author.get()
    price = entry_price.get()
    stock = entry_stock.get()
    if not (b_name and author and price and stock):
        messagebox.showwarning("Warning", "All fields are required")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (b_name, author, price, stock) VALUES (%s, %s, %s, %s)", (b_name, author, price, stock))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book added successfully")
    clear_book_entries()
    load_books()

def update_book():
    selected = tree_books.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book to update")
        return
    book_id = tree_books.item(selected[0])['values'][0]
    b_name = entry_bname.get()
    author = entry_author.get()
    price = entry_price.get()
    stock = entry_stock.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET b_name=%s, author=%s, price=%s, stock=%s WHERE book_id=%s",
                   (b_name, author, price, stock, book_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", "Book updated successfully")
    clear_book_entries()
    load_books()

def delete_book():
    selected = tree_books.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book to delete")
        return
    book_id = tree_books.item(selected[0])['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Book deleted successfully")
    load_books()

def clear_book_entries():
    entry_bname.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_stock.delete(0, tk.END)


# --------------------- CRUD FUNCTIONS: CUSTOMERS ---------------------
def load_customers():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        for row in tree_customers.get_children():
            tree_customers.delete(row)
        for r in rows:
            tree_customers.insert("", tk.END, values=r)
        conn.close()

def add_customer():
    name = entry_cname.get()
    email = entry_email.get()
    phone = entry_phone.get()
    address = entry_address.get()
    if not (name and email and phone and address):
        messagebox.showwarning("Warning", "All fields are required")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (c_name, email, phone, address) VALUES (%s, %s, %s, %s)",
                   (name, email, phone, address))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Customer added successfully")
    clear_customer_entries()
    load_customers()

def update_customer():
    selected = tree_customers.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a customer to update")
        return
    customer_id = tree_customers.item(selected[0])['values'][0]
    name = entry_cname.get()
    email = entry_email.get()
    phone = entry_phone.get()
    address = entry_address.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET c_name=%s, email=%s, phone=%s, address=%s WHERE customer_id=%s",
                   (name, email, phone, address, customer_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", "Customer updated successfully")
    clear_customer_entries()
    load_customers()

def delete_customer():
    selected = tree_customers.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a customer to delete")
        return
    customer_id = tree_customers.item(selected[0])['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Customer deleted successfully")
    load_customers()

def clear_customer_entries():
    entry_cname.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_address.delete(0, tk.END)


# --------------------- ORDER FUNCTIONS ---------------------
def place_order():
    try:
        cust_id = int(entry_customer_id.get())
        book_id = int(entry_book_id.get())
        quantity = int(entry_quantity.get())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.callproc('place_order', [cust_id, book_id, quantity])
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Order placed successfully!")
        load_books()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to place order: {e}")

def make_payment():
    try:
        order_id = int(entry_order_id.get())
        method = payment_method.get()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.callproc('make_payment', [order_id, method])
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Payment completed successfully!")
        load_order_summary()
    except Exception as e:
        messagebox.showerror("Error", f"Payment failed: {e}")

def load_order_summary():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_summary")
        rows = cursor.fetchall()
        for row in tree_orders.get_children():
            tree_orders.delete(row)
        for r in rows:
            tree_orders.insert("", tk.END, values=r)
        conn.close()


# --------------------- UI DESIGN ---------------------
root = tk.Tk()
root.title("📚 Online Bookstore Management System")
root.geometry("1100x700")
root.configure(bg="#F4F6F7")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---------- TAB 1: BOOKS CRUD ----------
tab_books = tk.Frame(notebook, bg="#F4F6F7")
notebook.add(tab_books, text="Books")

columns_books = ("ID", "Name", "Author", "Price", "Stock")
tree_books = ttk.Treeview(tab_books, columns=columns_books, show="headings", height=8)
for col in columns_books:
    tree_books.heading(col, text=col)
    tree_books.column(col, anchor=tk.CENTER, width=130)
tree_books.pack(fill="x", pady=10)

form_frame = tk.Frame(tab_books, bg="#F4F6F7")
form_frame.pack(pady=10)
tk.Label(form_frame, text="Name").grid(row=0, column=0)
entry_bname = tk.Entry(form_frame, width=15)
entry_bname.grid(row=0, column=1)
tk.Label(form_frame, text="Author").grid(row=0, column=2)
entry_author = tk.Entry(form_frame, width=15)
entry_author.grid(row=0, column=3)
tk.Label(form_frame, text="Price").grid(row=0, column=4)
entry_price = tk.Entry(form_frame, width=10)
entry_price.grid(row=0, column=5)
tk.Label(form_frame, text="Stock").grid(row=0, column=6)
entry_stock = tk.Entry(form_frame, width=10)
entry_stock.grid(row=0, column=7)

tk.Button(form_frame, text="Add", bg="#2ECC71", fg="white", command=add_book).grid(row=1, column=0, padx=5, pady=5)
tk.Button(form_frame, text="Update", bg="#F1C40F", fg="white", command=update_book).grid(row=1, column=1, padx=5)
tk.Button(form_frame, text="Delete", bg="#E74C3C", fg="white", command=delete_book).grid(row=1, column=2, padx=5)
tk.Button(form_frame, text="Refresh", bg="#3498DB", fg="white", command=load_books).grid(row=1, column=3, padx=5)
load_books()

# ---------- TAB 2: CUSTOMERS CRUD ----------
tab_customers = tk.Frame(notebook, bg="#F4F6F7")
notebook.add(tab_customers, text="Customers")

columns_customers = ("ID", "Name", "Email", "Phone", "Address")
tree_customers = ttk.Treeview(tab_customers, columns=columns_customers, show="headings", height=8)
for col in columns_customers:
    tree_customers.heading(col, text=col)
    tree_customers.column(col, anchor=tk.CENTER, width=150)
tree_customers.pack(fill="x", pady=10)

form2 = tk.Frame(tab_customers, bg="#F4F6F7")
form2.pack(pady=10)
tk.Label(form2, text="Name").grid(row=0, column=0)
entry_cname = tk.Entry(form2, width=15)
entry_cname.grid(row=0, column=1)
tk.Label(form2, text="Email").grid(row=0, column=2)
entry_email = tk.Entry(form2, width=15)
entry_email.grid(row=0, column=3)
tk.Label(form2, text="Phone").grid(row=0, column=4)
entry_phone = tk.Entry(form2, width=10)
entry_phone.grid(row=0, column=5)
tk.Label(form2, text="Address").grid(row=0, column=6)
entry_address = tk.Entry(form2, width=15)
entry_address.grid(row=0, column=7)

tk.Button(form2, text="Add", bg="#2ECC71", fg="white", command=add_customer).grid(row=1, column=0, padx=5, pady=5)
tk.Button(form2, text="Update", bg="#F1C40F", fg="white", command=update_customer).grid(row=1, column=1, padx=5)
tk.Button(form2, text="Delete", bg="#E74C3C", fg="white", command=delete_customer).grid(row=1, column=2, padx=5)
tk.Button(form2, text="Refresh", bg="#3498DB", fg="white", command=load_customers).grid(row=1, column=3, padx=5)
load_customers()

# ---------- TAB 3: ORDERS ----------
tab_orders = tk.Frame(notebook, bg="#F4F6F7")
notebook.add(tab_orders, text="Orders & Payments")

order_frame = tk.Frame(tab_orders, bg="#F4F6F7")
order_frame.pack(pady=10)
tk.Label(order_frame, text="Customer ID").grid(row=0, column=0)
entry_customer_id = tk.Entry(order_frame, width=10)
entry_customer_id.grid(row=0, column=1)
tk.Label(order_frame, text="Book ID").grid(row=0, column=2)
entry_book_id = tk.Entry(order_frame, width=10)
entry_book_id.grid(row=0, column=3)
tk.Label(order_frame, text="Qty").grid(row=0, column=4)
entry_quantity = tk.Entry(order_frame, width=10)
entry_quantity.grid(row=0, column=5)
tk.Button(order_frame, text="Place Order", bg="#2ECC71", fg="white", command=place_order).grid(row=0, column=6, padx=5)

payment_frame = tk.Frame(tab_orders, bg="#F4F6F7")
payment_frame.pack(pady=10)
tk.Label(payment_frame, text="Order ID").grid(row=0, column=0)
entry_order_id = tk.Entry(payment_frame, width=10)
entry_order_id.grid(row=0, column=1)
tk.Label(payment_frame, text="Method").grid(row=0, column=2)
payment_method = ttk.Combobox(payment_frame, values=["Online", "Cash"], width=10)
payment_method.grid(row=0, column=3)
tk.Button(payment_frame, text="Make Payment", bg="#E67E22", fg="white", command=make_payment).grid(row=0, column=4, padx=5)

columns_orders = ("Order ID", "Customer", "Book", "Qty", "Item Total", "Order Total", "Order Status", "Payment Status")
tree_orders = ttk.Treeview(tab_orders, columns=columns_orders, show="headings")
for col in columns_orders:
    tree_orders.heading(col, text=col)
    tree_orders.column(col, anchor=tk.CENTER, width=120)
tree_orders.pack(fill="both", expand=True, pady=10)

tk.Button(tab_orders, text="Refresh Orders", bg="#5DADE2", fg="white", command=load_order_summary).pack(pady=5)

root.mainloop()