import oracledb
import customtkinter as ctk
from tkinter import ttk

# --- 1. تفعيل المترجم (Thick Mode) ---
try:
    oracledb.init_oracle_client(lib_dir=r"C:\instantclient_19_30")
except Exception as e:
    print(f"Oracle Client Error: {e}")

# --- 2. إعدادات النافذة الرئيسية ---
app = ctk.CTk()
app.geometry("1100x900")
app.title("Pharmacy Pro Management System")
app.configure(fg_color="#FFE4E1") # الخلفية البينك Misty Rose

# --- 3. تنسيق الجداول (UI Styling) ---
style = ttk.Style()
style.theme_use("clam")

# تنسيق العناوين (تصليح إيرور Style)
style.configure("Treeview.Heading", 
                font=("Arial", 12, "bold"), 
                background="#FFB6C1", 
                foreground="black")

style.configure("Treeview", 
                background="#FFF0F5", 
                foreground="black", 
                rowheight=30, 
                fieldbackground="#FFF0F5",
                font=("Arial", 11))

style.map("Treeview", background=[('selected', '#FF69B4')])

# --- 4. الدوال البرمجية (Database Logic) ---

def connect_db():
    return oracledb.connect(user="pharmacy2", password="22222", dsn="localhost:1521/xe")

def show_table_data(table_name):
    """دالة عامة لعرض أي جدول أو View"""
    for i in tree.get_children():
        tree.delete(i)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name.upper()}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        for row in rows:
            tree.insert("", "end", values=row)
        status_label.configure(text=f"Displaying: {table_name}", text_color="green")
        cursor.close()
        conn.close()
    except Exception as e:
        # التعامل مع اسم Medicines/Mediciens تلقائياً
        if table_name.upper() == "MEDICINES":
             show_table_data("MEDICIENS")
        else:
            status_label.configure(text=f"Error: {table_name} not found!", text_color="red")
            print(f"Database Error: {e}")

def calculate_accounting():
    """حساب إجمالي المبيعات باستخدام الاسم الصح TOTAL_PRICE"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # التعديل بناءً على الـ SQL الخاص بكِ
        cursor.execute("SELECT SUM(TOTAL_PRICE) FROM SALES")
        result = cursor.fetchone()[0]
        accounting_result.configure(text=f"Total Revenue: {result if result else 0} EGP")
        status_label.configure(text="Finance Updated!", text_color="green")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Accounting Error: {e}")
        accounting_result.configure(text="Finance Error")

# --- 5. تصميم الواجهة (UI Layout) ---

title_label = ctk.CTkLabel(app, text="Pharmacy Management System", 
                           font=("Courier", 35, "bold"), text_color="#C71585")
title_label.pack(pady=20)

# فريم أزرار الجداول
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

tables_list = ["CATEGORIES", "SUPPLIERS", "EMPLOYEES", "MEDICIENS", "SALES", "CUSTOMERS"]

for i, table in enumerate(tables_list):
    btn = ctk.CTkButton(btn_frame, text=table, width=155, height=45, 
                        fg_color="#FF69B4", hover_color="#C71585",
                        font=("Arial", 13, "bold"),
                        command=lambda t=table: show_table_data(t))
    btn.grid(row=i//3, column=i%3, padx=15, pady=10)

# زرار الـ View (الفاتورة المعتمدة)
view_btn = ctk.CTkButton(app, text="🧾 Show Pharmacy Invoice View 🧾", 
                         width=450, height=60, 
                         fg_color="#9370DB", hover_color="#4B0082", 
                         font=("Arial", 18, "bold"),
                         command=lambda: show_table_data("pharmacy_invoice"))
view_btn.pack(pady=20)

# جدول العرض
tree_frame = ctk.CTkFrame(app)
tree_frame.pack(pady=10, fill="both", expand=True, padx=40)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# --- قسم الحسابات المميز ---
finance_frame = ctk.CTkFrame(app, fg_color="#FFF0F5", corner_radius=15)
finance_frame.pack(pady=20, padx=40, fill="x")

accounting_result = ctk.CTkLabel(finance_frame, text="Total Revenue: -- EGP", 
                                font=("Arial", 22, "bold"), text_color="#C71585")
accounting_result.pack(side="left", padx=40, pady=20)

acc_btn = ctk.CTkButton(finance_frame, text="💰 Calculate Finance", 
                        width=200, height=50, 
                        fg_color="#2E8B57", hover_color="#1E6B47", 
                        font=("Arial", 15, "bold"),
                        command=calculate_accounting)
acc_btn.pack(side="right", padx=40, pady=20)

status_label = ctk.CTkLabel(app, text="Ready | connected to pharmacy_invoice", font=("Arial", 14))
status_label.pack(pady=10)

app.mainloop()