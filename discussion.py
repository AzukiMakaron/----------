import tkinter as tk
from tkinter import scrolledtext, Listbox, Frame, Label, Button, Entry, messagebox, simpledialog
import mysql.connector

class DiscussionFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_config = {
            'host': '60.204.212.12',
            'user': 'root',
            'password': 'helloworld',
            'database': 'InternshipSystem',
            'charset': 'utf8mb4'
        }
        tk.Label(self, text="讨论区").pack()
        self.create_widgets()
        self.load_messages()

    def create_widgets(self):
        # 创建作者ID输入框
        author_id_frame = Frame(self)
        author_id_label = Label(author_id_frame, text="作者ID:")
        author_id_label.pack(side=tk.LEFT)
        self.author_id_entry = Entry(author_id_frame)
        self.author_id_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        author_id_frame.pack(fill=tk.X)

        # 创建帖子内容输入框
        post_frame = Frame(self)
        Label(post_frame, text="发帖内容:").pack(side=tk.TOP)
        self.content_text = scrolledtext.ScrolledText(post_frame, height=5, width=50)
        self.content_text.pack(side=tk.TOP, fill=tk.X)
        post_frame.pack(fill=tk.X, expand=True)

        # 创建发帖按钮
        post_button = Button(self, text="发帖", command=self.post_message)
        post_button.pack(fill=tk.X)

        # 创建回复内容输入框
        reply_frame = Frame(self)
        Label(reply_frame, text="回复内容:").pack(side=tk.TOP)
        self.reply_text = scrolledtext.ScrolledText(reply_frame, height=3, width=50)
        self.reply_text.pack(side=tk.TOP, fill=tk.X)
        reply_frame.pack(fill=tk.X, expand=True)

        # 创建回复按钮
        reply_button = Button(self, text="回复", command=self.reply_message)
        reply_button.pack(fill=tk.X)

        # 创建帖子列表框
        listbox_frame = Frame(self)
        Label(listbox_frame, text="帖子列表:").pack(side=tk.TOP)
        self.listbox = Listbox(listbox_frame, width=50, height=15)
        self.listbox.pack(side=tk.TOP, fill=tk.X)
        listbox_frame.pack(fill=tk.X, expand=True)

        # 加载帖子按钮
        load_button = Button(self, text="加载帖子", command=self.load_messages)
        load_button.pack(fill=tk.X)
        
        # 返回按钮
        back_button = Button(self, text="返回", command=self.go_back)
        back_button.pack(fill=tk.X)
    
        
    def post_message(self):
        author_id = self.author_id_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        if not author_id or not content:
            messagebox.showwarning("警告", "作者ID和内容不能为空")
            return

        query = "INSERT INTO Discussion (AuthorID, Content) VALUES (%s, %s)"
        try:
            self.execute_query(query, (author_id, content))
            messagebox.showinfo("成功", "帖子已发布")
            self.content_text.delete("1.0", tk.END)  # 清空输入框
            self.load_messages()  # 重新加载帖子
        except Exception as e:
            messagebox.showerror("错误", str(e))


    def reply_message(self):
        reply_content = self.reply_text.get("1.0", tk.END).strip()
        if not reply_content:
            messagebox.showwarning("警告", "回复内容不能为空")
            return

        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("警告", "请选择一个帖子进行回复")
            return

        post_id = self.listbox.get(selected_index[0]).split()[0]  # 假设帖子ID是列表中每项的第一个元素
        author_id = self.author_id_entry.get()
        query = "INSERT INTO Discussion (AuthorID, Content) VALUES (%s, %s)"
        try:
            self.execute_query(query, (author_id, reply_content))
            messagebox.showinfo("成功", "回复已发布")
            self.reply_text.delete("1.0", tk.END)  # 清空输入框
        except Exception as e:
            messagebox.showerror("错误", str(e))


    def load_messages(self):
        self.listbox.delete(0, tk.END)  # 清空现有列表
        query = "SELECT PostID, Content FROM Discussion ORDER BY PostTime DESC"
        try:
            results = self.execute_query(query)
            for post_id, content in results:
                self.listbox.insert(tk.END, f"{post_id} - {content}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def go_back(self):
        self.forget()
        # super.welcome_label.pack(fill=tk.X)

    def connect_to_database(self):
        return mysql.connector.connect(**self.db_config)

    def execute_query(self, query, params=None):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        try:
            cursor.execute(query, params or ())
            if query.lstrip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                connection.commit()
            return None
        finally:
            cursor.close()
            connection.close()