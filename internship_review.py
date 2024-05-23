import tkinter as tk
from tkinter import messagebox
import mysql.connector

def connect_to_database():
    """
    连接到MySQL数据库并返回连接对象。
    """
    try:
        connection = mysql.connector.connect(
            host="60.204.212.12",
            user="root",
            password="helloworld",
            database="InternshipSystem"
        )
        print("连接成功")  # 打印成功消息
        return connection
    except mysql.connector.Error as e:
        print("连接失败:", e)  # 打印错误消息
        return None

def create_review(connection, student_id, job_id, score, comment):
    """
    在数据库中创建新的实习评价。
    """
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO InternshipReview (StudentID, JobID, Score, Comment) VALUES (%s, %s, %s, %s)"
        val = (student_id, job_id, score, comment)
        cursor.execute(sql, val)  # 执行SQL命令
        connection.commit()  # 提交事务
        messagebox.showinfo("成功！", "评价创建成功")  # 显示成功消息
    except mysql.connector.Error as e:
        messagebox.showerror("失败", "评价创建失败: " + str(e))  # 显示错误消息

def fetch_reviews(connection, student_id):
    """
    获取指定学生的所有实习评价。
    """
    try:
        cursor = connection.cursor()
        sql = """
        SELECT c.Name, r.Score, r.Comment
        FROM InternshipReview r
        JOIN Internship i ON r.JobID = i.JobID
        JOIN Company c ON i.CompanyID = c.CompanyID
        WHERE r.StudentID = %s
        """
        val = (student_id,)
        cursor.execute(sql, val)  # 执行SQL查询
        reviews = cursor.fetchall()  # 获取所有结果
        if not reviews:
            messagebox.showinfo("无评价", "没有找到该学生评价")  # 如果没有评价，显示消息
        else:
            review_text = ""
            for review in reviews:
                review_text += f"公司名称: {review[0]}, 评分: {review[1]}, 评论: {review[2]}\n"
            messagebox.showinfo("评价", review_text)  # 显示评价
    except mysql.connector.Error as e:
        messagebox.showerror("错误", "获取评价时出错: " + str(e))  # 显示错误消息

def fetch_all_reviews(connection):
    """
    获取所有学生的实习评价。
    """
    try:
        cursor = connection.cursor()
        sql = """
        SELECT c.Name, r.Score, r.Comment
        FROM InternshipReview r
        JOIN Internship i ON r.JobID = i.JobID
        JOIN Company c ON i.CompanyID = c.CompanyID
        """
        cursor.execute(sql)  # 执行SQL查询
        reviews = cursor.fetchall()  # 获取所有结果
        if not reviews:
            messagebox.showinfo("无评价", "没有找到任何评价")  # 如果没有评价，显示消息
        else:
            review_text = ""
            for review in reviews:
                review_text += f"公司名称: {review[0]}, 评分: {review[1]}, 评论: {review[2]}\n"
            messagebox.showinfo("所有评价", review_text)  # 显示所有评价
    except mysql.connector.Error as e:
        messagebox.showerror("错误", "获取所有评价时出错: " + str(e))  # 显示错误消息

def submit_review():
    """
    提交新的评价。
    """
    student_id = int(student_id_entry.get())
    job_id = int(job_id_entry.get())
    score = int(score_entry.get())
    comment = comment_entry.get("1.0", "end-1c")
    create_review(connection, student_id, job_id, score, comment)

def view_reviews():
    """
    查看指定学生的评价。
    """
    student_id = int(student_id_entry.get())
    fetch_reviews(connection, student_id)

def view_all_reviews():
    """
    查看所有学生的评价。
    """
    fetch_all_reviews(connection)

# 连接到数据库
connection = connect_to_database()

if connection:
    # 创建Tkinter主窗口
    root = tk.Tk()
    root.title("实时评价系统")

    # 设置窗口居中
    window_width = 800
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) / 2
    y_coordinate = (screen_height - window_height) / 2
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # 配置行和列的权重，使得界面元素可以自动调整大小
    for i in range(5):
        root.grid_rowconfigure(i, weight=1)
    for j in range(2):
        root.grid_columnconfigure(j, weight=1)

    # 学生ID标签和输入框
    student_id_label = tk.Label(root, text="学生 ID:")
    student_id_label.grid(row=0, column=0, sticky="e")
    student_id_entry = tk.Entry(root)
    student_id_entry.grid(row=0, column=1, sticky="w")

    # 职位ID标签和输入框
    job_id_label = tk.Label(root, text="职位 ID:")
    job_id_label.grid(row=1, column=0, sticky="e")
    job_id_entry = tk.Entry(root)
    job_id_entry.grid(row=1, column=1, sticky="w")

    # 评分标签和输入框
    score_label = tk.Label(root, text="评分:")
    score_label.grid(row=2, column=0, sticky="e")
    score_entry = tk.Entry(root)
    score_entry.grid(row=2, column=1, sticky="w")

    # 评论标签和文本框
    comment_label = tk.Label(root, text="评论:")
    comment_label.grid(row=3, column=0, sticky="e")
    comment_entry = tk.Text(root, height=5, width=30)
    comment_entry.grid(row=3, column=1, sticky="w")

    # 提交按钮
    submit_button = tk.Button(root, text="提交", command=submit_review)
    submit_button.grid(row=4, column=0, sticky="e")

    # 查看评价按钮
    view_button = tk.Button(root, text="查看评价", command=view_reviews)
    view_button.grid(row=4, column=1, sticky="w")

    # 查看所有评价按钮
    view_all_button = tk.Button(root, text="查看所有评价", command=view_all_reviews)
    view_all_button.grid(row=5, column=0, columnspan=2)

    # 启动主事件循环
    root.mainloop()
