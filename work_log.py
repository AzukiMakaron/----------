import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class LogManager(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # 数据库连接配置
        self.config = {
            'user': 'root',
            'password': 'helloworld',
            'host': '60.204.212.12',
            'database': 'InternshipSystem',
            'raise_on_warnings': True
        }

        # 初始化界面
        self.setup_widgets()
        self.fetch_logs()

    def create_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            if conn.is_connected():
                return conn
        except Error as e:
            messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
            return None

    def insert_log(self):
        conn = self.create_connection()
        if conn:
            student_id = self.entry_student_id.get()
            task_description = self.entry_task_description.get()
            date_str = self.entry_date.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

            if not student_id or not task_description or not date:
                messagebox.showerror("Error", "所有字段都是必填的")
                return

            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO WorkLog (StudentID, Date, TaskDescription) VALUES (%s, %s, %s)",
                               (student_id, date, task_description))
                conn.commit()
                messagebox.showinfo("成功", "日志插入成功")
                self.clear_entries()
                self.fetch_logs()
            except Error as e:
                messagebox.showerror("错误", f"日志插入失败: {e}")
            finally:
                cursor.close()
                conn.close()

    def fetch_logs(self):
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT StudentID, Date, TaskDescription FROM WorkLog ORDER BY Date DESC")
                logs = cursor.fetchall()
                self.listbox_logs.delete(0, tk.END)
                for log in logs:
                    formatted_date = log[1].strftime('%Y-%m-%d')
                    self.listbox_logs.insert(tk.END, f"{log[0]} - {formatted_date} - {log[2]}")
            except Error as e:
                messagebox.showerror("错误", f"无法查到该日志: {e}")
            finally:
                cursor.close()
                conn.close()

    def clear_entries(self):
        self.entry_student_id.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_task_description.delete(0, tk.END)

    def setup_widgets(self):
        self.entry_student_id = tk.Entry(self)
        self.entry_student_id.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self, text="学生ID:").grid(row=0, column=0, padx=10, pady=5)

        self.entry_date = tk.Entry(self)
        self.entry_date.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self, text="日期 (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)

        self.entry_task_description = tk.Entry(self)
        self.entry_task_description.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self, text="任务描述:").grid(row=2, column=0, padx=10, pady=5)

        tk.Button(self, text="提交日志", command=self.insert_log).grid(row=3, column=1, pady=10)

        self.listbox_logs = tk.Listbox(self, width=50, height=10)
        self.listbox_logs.grid(row=5, column=0, columnspan=2, padx=10, pady=10)