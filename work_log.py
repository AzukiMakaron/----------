#日志管理


import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'helloworld',
    'host': '60.204.212.12',
    'database': 'InternshipSystem',
    'raise_on_warnings': True
}

# 创建数据库连接
def create_connection():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
        return None

# 初始化数据库表（如果尚未创建）
# def init_db():
#     conn = create_connection()
#     if conn is not None:
#         try:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS WorkLog (
#                     LogID INT AUTO_INCREMENT PRIMARY KEY,
#                     StudentID INT,
#                     Date DATE,
#                     TaskDescription TEXT
#                 )
#             """)
#             conn.commit()
#             messagebox.showinfo("Success", "Database initialized successfully")
#         except Error as e:
#             messagebox.showerror("Error", f"Error initializing database: {e}")
#         finally:
#             if conn.is_connected():
#                 cursor.close()
#                 conn.close()

# 插入日志
def insert_log():
    conn = create_connection()
    if conn is not None:
        student_id = entry_student_id.get()
        task_description = entry_task_description.get()
        date_str = entry_date.get()
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        if not student_id or not task_description or not date:
            messagebox.showerror("Error", "所有字段都是必填的")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO WorkLog (StudentID, Date, TaskDescription) VALUES (%s, %s, %s)",
                           (student_id, date, task_description))
            conn.commit()
            messagebox.showinfo("Success", "Log inserted successfully")
            fetch_logs()
        except Error as e:
            messagebox.showerror("Error", f"Failed to insert log: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# 获取日志
# 获取并按日期排序日志
def fetch_logs():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # 添加 ORDER BY 子句来按日期排序
            cursor.execute("SELECT  StudentID, Date, TaskDescription FROM WorkLog ORDER BY Date DESC")
            logs = cursor.fetchall()
            listbox_logs.delete(0, tk.END)  # 清空日志列表框
            for log in logs:
                # 格式化日期显示
                formatted_date = log[1].strftime('%Y-%m-%d')
                listbox_logs.insert(tk.END, f"{log[0]} - {formatted_date} - {log[2]}")
        except Error as e:
            messagebox.showerror("Error", f"Failed to fetch logs: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
# 删除日志
def delete_log():
    conn = create_connection()
    if conn is not None:
        try:
            selected_log_id = int(entry_log_id.delete(0, tk.END).get())
            cursor = conn.cursor()
            cursor.execute("DELETE FROM WorkLog WHERE LogID = %s", (selected_log_id,))
            conn.commit()
            messagebox.showinfo("Success", "Log deleted successfully")
            fetch_logs()  # 刷新日志列表
        except ValueError:
            messagebox.showerror("Error", "Please select a valid log ID")
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete log: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
# 创建主窗口
root = tk.Tk()
root.title("学生实习日志管理系统")

# 调用初始化数据库函数
# init_db()
# 创建输入框和标签
entry_student_id = tk.Entry(root)
entry_student_id.grid(row=0, column=1, padx=10, pady=5)

label_student_id = tk.Label(root, text="学生ID:")
label_student_id.grid(row=0, column=0, padx=10, pady=5)

entry_date = tk.Entry(root)
entry_date.grid(row=1, column=1, padx=10, pady=5)

label_date = tk.Label(root, text="日期 (YYYY-MM-DD):")
label_date.grid(row=1, column=0, padx=10, pady=5)

entry_task_description = tk.Entry(root)
entry_task_description.grid(row=2, column=1, padx=10, pady=5)

label_task_description = tk.Label(root, text="任务描述:")
label_task_description.grid(row=2, column=0, padx=10, pady=5)

button_submit = tk.Button(root, text="提交日志", command=insert_log)
button_submit.grid(row=3, column=1, pady=10)

# 创建日志ID输入框（用于删除功能）
label_log_id = tk.Label(root, text="Log ID (for deletion):")
label_log_id.grid(row=3, column=0, padx=10, pady=5)
entry_log_id = tk.Entry(root)
entry_log_id.grid(row=4, column=0, padx=10, pady=5)

# 创建删除按钮
button_delete = tk.Button(root, text="Delete Log", command=delete_log)
button_delete.grid(row=4, column=1, pady=10)

# 创建日志列表框
listbox_logs = tk.Listbox(root, width=50, height=10)
listbox_logs.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# 刷新日志列表框
fetch_logs()

# 启动GUI主循环
root.mainloop()