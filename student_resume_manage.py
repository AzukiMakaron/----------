import tkinter as tk
import os
import re
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import minio
from minio.error import S3Error
from user_session import UserSession
#创建minio实例
minio_client = minio.Minio(
    '60.204.217.157:9000', 
    access_key='doufen', 
    secret_key='zwsxhdm233', 
    secure=False
    )
#创建数据库连接
db=mysql.connector.connect(
    host='60.204.212.12',
    user='root',
    password='helloworld',
    database='InternshipSystem'
    )
# 插入学生数据到数据库
def insert_student_info(db, data):
    cursor = db.cursor()
    try:
        # 从UserSession获取当前用户ID
        current_user_id = UserSession.get_user_id()

        # 添加UserID到数据字典
        data['UserID'] = current_user_id

        # 准备SQL语句
        sql = """
        INSERT INTO Student (Username, Name, Department, Major, Class, ResponsibleTeacher, Grade, Skills)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 准备插入数据的值
        values = (
            data['UserID'],
            data.get('学生姓名'), 
            data.get('学生院系'), 
            data.get('学生专业'), 
            data.get('所在班级'), 
            data.get('班主任'), 
            data.get('课程成绩'), 
            data.get('个人技能')
        )

        # 执行SQL语句，并提交到数据库
        cursor.execute(sql, values)
        db.commit()

    except Exception as e:
        db.rollback()  # 在发生错误时回滚
        print(f"插入数据时发生错误：{e}")
    finally:
        cursor.close()  # 确保无论如何都关闭游标
class StudentResumeFrameWork(tk.Frame):
    def __init__(self, parent, minio_client, db):
        super().__init__(parent)
        self.minio_client = minio_client
        self.db = db
        
        # 标题标签
        tk.Label(self, text="学生简历信息管理与查询界面").pack(pady=10)

        # 创建一个容器来放置所有标签和输入框
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20, padx=20)

        # 定义数据输入的标签和字段名
        labels = ['学生姓名', '学生院系', '学生专业', '所在班级', '班主任', '课程成绩', '个人技能']
        self.entries = {}
        for label in labels:
            row = ttk.Frame(form_frame)
            row.pack(fill='x', padx=5, pady=5)
            lbl = ttk.Label(row, text=label + "：", width=15, anchor='w')
            lbl.pack(side='left')
            entry_var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=entry_var, width=50)
            entry.pack(side='right', expand=True)
            self.entries[label] = entry_var

        # 上传简历按钮
        upload_btn = ttk.Button(self, text="上传 PDF 简历", command=self.select_file)
        upload_btn.pack(pady=5)

        # 保存个人信息按钮
        save_btn = ttk.Button(self, text="保存个人信息", command=self.save_data)
        save_btn.pack(pady=5)

        # 下载简历按钮
        download_btn = ttk.Button(self, text="下载 PDF 简历", command=self.download_resume)
        download_btn.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.upload_file_to_minio(file_path)

    def save_data(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        # 这里应该根据您的数据库设计来调整
        try:
            # 假设有一个适当的函数来处理数据的插入
            insert_student_info(self.db,data)
            messagebox.showinfo("成功", "个人信息保存成功！")
        except Exception as err:
            messagebox.showerror("失败", "保存失败，请检查数据或联系管理员！")

    def upload_file_to_minio(self, filepath):
        student_name = self.entries['学生姓名'].get().strip()
        if not student_name:
            messagebox.showerror("失败", "请先输入学生姓名")
            return
        bucket_name = "resume"
        # 移除所有非字母数字字符
        clean_name = re.sub(r'[^\w\s]', '', student_name)
        object_name = f"{clean_name}简历.pdf"
        try:
            # 检查文件是否已存在
            existing = True
            try:
                self.minio_client.stat_object(bucket_name, object_name)
            except S3Error as e:
                if e.code == 'NoSuchKey':
                    existing = False
                else:
                    raise

            if existing:
                # 添加确认对话框询问用户是否覆盖
                if messagebox.askyesno("确认", "文件已存在。要覆盖吗？"):
                    self.minio_client.fput_object(bucket_name, object_name, filepath)
                else:
                    return
            else:
                self.minio_client.fput_object(bucket_name, object_name, filepath)
            messagebox.showinfo("成功", "简历已成功上传！")
        except S3Error as e:
            messagebox.showerror("失败", "简历上传失败，请检查网络连接或联系管理员！错误信息：" + str(e))

    def download_resume(self):
        student_name = self.entries['学生姓名'].get().strip()
        if not student_name:
            messagebox.showerror("失败", "请先输入学生姓名")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_path:
            bucket_name = "resume"
            object_name = f"{student_name}简历.pdf"
            try:
                # 检查云端是否有该文件
                self.minio_client.stat_object(bucket_name, object_name)
                self.minio_client.fget_object(bucket_name, object_name, save_path)
                messagebox.showinfo("成功", "简历已成功下载！")
            except S3Error:
                messagebox.showerror("失败", "无法下载简历，该学生的简历不存在或其他错误！")