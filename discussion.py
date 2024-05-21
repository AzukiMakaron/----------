#讨论区
import pymysql
import tkinter as tk
from tkinter import scrolledtext, Listbox, Frame, Label, Button, Entry, messagebox, simpledialog
# 数据库连接参数
db_config = {
    'host': '60.204.212.12',
    'user': 'root',
    'password': 'helloworld',
    'db': 'InternshipSystem',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接数据库
connection = pymysql.connect(**db_config)
connection.close()
# 定义发帖功能
def post_message():
    try:
        author_id = author_id_entry.get()
        content = content_text.get(1.0, tk.END).strip()
        if not author_id or not content:
            messagebox.showerror("错误", "作者ID和内容不能为空！")
            return

        # 重新打开数据库连接
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "INSERT INTO Discussion (AuthorID, Content) VALUES (%s, %sa)"
            cursor.execute(sql, (author_id, content))
            connection.commit()
            messagebox.showinfo("成功", "发帖成功！")
            content_text.delete(1.0, tk.END)
            author_id_entry.delete(0, tk.END)
            load_messages()  # 刷新帖子列表
    except pymysql.MySQLError as e:
        messagebox.showerror("数据库错误", f"无法发帖：{e}")
    finally:
        if connection:
            connection.close()  # 关闭数据库连接


def reply_message():
    try:
        # 用户输入要回复的AuthorID
        selected_author_id = simpledialog.askinteger("回复帖子", "请输入要回复的帖子的作者ID：", parent=root)
        if selected_author_id is None:
            return  # 用户取消了输入

        # 获取当前用户的AuthorID
        current_author_id_str = author_id_entry.get().strip()
        if not current_author_id_str.isdigit():
            messagebox.showerror("错误", "当前作者ID无效，请输入一个整数。")
            return
        current_author_id = int(current_author_id_str)

        # 确认用户输入的AuthorID是否与当前用户的AuthorID匹配
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                # 使用AuthorID来查询帖子
                sql = "SELECT COUNT(*) FROM Discussion WHERE AuthorID = %s"
                cursor.execute(sql, (selected_author_id,))
                result = cursor.fetchone()[0]
                if result > 0:
                    # 作者ID匹配，检查是否是当前用户的帖子
                    if selected_author_id == current_author_id:
                        # 允许回复
                        content = reply_text.get(1.0, tk.END).strip()
                        if not content:
                            messagebox.showerror("错误", "回复内容不能为空！")
                            return
                        # 插入回复到数据库
                        sql = "INSERT INTO Discussion (AuthorID, Content) VALUES (%s, %s)"
                        cursor.execute(sql, (current_author_id, f"Re: {selected_author_id}\n{content}"))
                        connection.commit()
                        messagebox.showinfo("成功", "回复成功！")
                        reply_text.delete(1.0, tk.END)
                        load_messages()  # 刷新帖子列表
                    else:
                        messagebox.showerror("错误", "您没有权限回复此帖子，因为它不属于您。")
                else:
                    messagebox.showerror("错误", "没有找到相应的帖子或作者ID。")
        finally:
            connection.close()
    except pymysql.MySQLError as e:
        messagebox.showerror("数据库错误", f"无法执行操作：{e}")
    except Exception as e:
        messagebox.showerror("错误", f"发生未知错误：{e}")
def load_messages():
    try:
        # 重新打开数据库连接
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "SELECT PostID, AuthorID, Content, PostTime FROM Discussion ORDER BY PostTime DESC"
            cursor.execute(sql)
            posts = cursor.fetchall()
            listbox.delete(0, tk.END)  # 清空列表框
            for post in posts:
                # 更新GUI组件，显示帖子信息
                listbox.insert(tk.END, f"PostID: {post['PostID']} - AuthorID: {post['AuthorID']}\n{post['Content']}\nPostTime: {post['PostTime']}\n")
        connection.close()  # 操作完成后关闭数据库连接
    except pymysql.MySQLError as e:
        messagebox.showerror("数据库错误", f"无法加载帖子：{e}")
    except Exception as e:
        messagebox.showerror("错误", f"发生未知错误：{e}")

# 创建主窗口
root = tk.Tk()
root.title("讨论区")

# 创建作者ID输入框
author_id_frame = Frame(root)
author_id_label = Label(author_id_frame, text="作者ID:")
author_id_label.pack(side=tk.LEFT)
author_id_entry = Entry(author_id_frame)
author_id_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
author_id_frame.pack(fill=tk.X)

# 创建帖子内容输入框
post_frame = Frame(root)
Label(post_frame, text="发帖内容:").pack(side=tk.TOP)
content_text = scrolledtext.ScrolledText(post_frame, height=5, width=50)
content_text.pack(side=tk.TOP, fill=tk.X)
post_frame.pack(fill=tk.X, expand=True)

# 创建发帖按钮
post_button = Button(root, text="发帖", command=post_message)
post_button.pack(fill=tk.X)

# 创建回复内容输入框
reply_frame = Frame(root)
Label(reply_frame, text="回复内容:").pack(side=tk.TOP)
reply_text = scrolledtext.ScrolledText(reply_frame, height=3, width=50)
reply_text.pack(side=tk.TOP, fill=tk.X)
reply_frame.pack(fill=tk.X, expand=True)

# 创建回复按钮
reply_button = Button(root, text="回复", command=reply_message)
reply_button.pack(fill=tk.X)

# 创建帖子列表框
listbox_frame = Frame(root)
Label(listbox_frame, text="帖子列表:").pack(side=tk.TOP)
listbox = Listbox(listbox_frame, width=50, height=15)
listbox.pack(side=tk.TOP, fill=tk.X)
listbox_frame.pack(fill=tk.X, expand=True)

# 加载帖子按钮
load_button = Button(root, text="加载帖子", command=load_messages)
load_button.pack(fill=tk.X)
load_messages()
# 运行主循环
root.mainloop()