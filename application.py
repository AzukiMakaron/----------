import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


# 数据库连接函数
def create_db_connection(config):
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("MySQL Database connection successful")
    except Error as err:
        print(f"The error '{err}' occurred")
    return connection


# 查询实习职位
def query_internships():
    conn = create_db_connection(db_config)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SET time_zone ='+08:00'")
        query = "SELECT JobID, JobDescription, PostDate FROM Internship"
        try:
            cursor.execute(query)
            internships = cursor.fetchall()
            internships_list.delete(0, tk.END)
            for internship in internships:
                internships_list.insert(tk.END,
                                        f"JobID: {internship[0]}, Description: {internship[1]}, PostDate: {internship[2]}")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
            conn.close()


# 应聘职位
def apply_for_internship():
    student_id = student_id_entry.get()
    job_id = job_id_entry.get()

    if not student_id or not job_id:
        messagebox.showerror("Error", "Please fill in both Student ID and Job ID")
        return

    conn = create_db_connection(db_config)
    if conn.is_connected():
        cursor = conn.cursor()
        query = "INSERT INTO Application (StudentID, JobID, ApplicationStatus) VALUES (%s, %s, 'applied')"
        val = (student_id, job_id)
        try:
            cursor.execute(query, val)
            conn.commit()
            messagebox.showinfo("Success", "Application submitted successfully!")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
            conn.close()


# 创建GUI窗口
root = tk.Tk()
root.title("学生实习日志管理系统")

# 设置窗口大小
window_width = 800
window_height = 600
root.geometry(f'{window_width}x{window_height}')

# 数据库配置信息
db_config = {
    'host': '60.204.212.12',
    'user': 'root',
    'passwd': 'helloworld',
    'database': 'InternshipSystem'
}

# 输入框
tk.Label(root, text="Student ID:").pack()
student_id_entry = tk.Entry(root)
student_id_entry.pack()

tk.Label(root, text="Job ID:").pack()
job_id_entry = tk.Entry(root)
job_id_entry.pack()

# 查询和应聘按钮
query_button = tk.Button(root, text="Query Internships", command=query_internships)
query_button.pack()

apply_button = tk.Button(root, text="Apply for Internship", command=apply_for_internship)
apply_button.pack()

# 显示查询结果的列表
internships_list = tk.Listbox(root)
internships_list.pack()

# 运行GUI
root.mainloop()