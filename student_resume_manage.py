import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont, simpledialog
from minio import Minio
from minio.error import S3Error
import mysql.connector
import sign_in

# Minio云服务器模拟OSS存储PDF简历
def create_minio_client():
    return Minio(
        "60.204.217.157:9000",
        access_key="doufen",
        secret_key="zwsxhdm233",
        secure=False  # 使用HTTP协议
    )

# 连接到MySQL数据库
mydb = mysql.connector.connect(
    host="60.204.212.12",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="helloworld",  # 数据库密码
    database="InternshipSystem"  # 数据库名称
)

class StudentInfoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("学生信息和简历上传")
        self.geometry("450x450")  # 设置窗口大小
        self.resizable(False, False)  # 窗口大小不可变

        self.custom_font = tkfont.Font(family="Helvetica", size=12)  # 自定义字体

        # 使用 ttk 样式
        style = ttk.Style(self)
        style.theme_use("clam")  # 可以使用 "clam", "alt", "default", "classic" 等主题

        # 创建并放置标签和输入框
        labels = [
            '学生姓名', '学生院系', '学生专业', '所在班级', '班主任', '课程成绩', '个人技能'
        ]
        self.entries = {}
        for i, label in enumerate(labels):
            lbl = ttk.Label(self, text=label + "：", font=self.custom_font)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry_var = tk.StringVar()
            entry = ttk.Entry(self, textvariable=entry_var, font=self.custom_font)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[label] = entry_var

        # 创建并放置按钮
        upload_btn = ttk.Button(self, text="上传 PDF 简历", command=self.select_file)
        upload_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        save_btn = ttk.Button(self, text="上传个人信息", command=self.save_data)
        save_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        download_btn = ttk.Button(self, text="下载 PDF 简历", command=self.download_resume)
        download_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def select_file(self):
        """选择文件并上传到 MinIO"""
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.upload_file_to_minio(file_path)


    def save_data(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        try:
            mycursor = mydb.cursor()
            sql = """
            INSERT INTO Student (UserID, Name, Department, Major, Class, ResponsibleTeacher, Grade, Skills) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (sign_in.userId, data['学生姓名'], data['学生院系'], data['学生专业'], data['所在班级'], data['班主任'], data['课程成绩'], data['个人技能'])
            mycursor.execute(sql, val)
            mydb.commit()  # 数据库操作需要commit来确保数据被保存
            messagebox.showinfo("成功", "个人信息上传成功！")
        except mysql.connector.Error as err:
            messagebox.showerror("上传失败，请联系管理员修复")

    def upload_file_to_minio(self, filepath):
    # """上传文件到 MinIO，并将文件名改为 '学生姓名简历.pdf'"""
        student_name = self.entries['学生姓名'].get()
        if not student_name.strip():  # 确保学生姓名不为空且不只包含空白字符
            messagebox.showerror("上传失败", "请先输入学生姓名")
            return  # 如果学生姓名为空或仅包含空格，显示错误并结束函数

        client = create_minio_client()
        bucket_name = "resume"  # 数据桶的名称
        object_name = student_name + "简历.pdf"  # 新文件名

        try:
            client.fput_object(bucket_name, object_name, filepath)  # 上传文件到 MinIO
            messagebox.showinfo("上传成功", f"简历已上传为 {object_name}.")
        except S3Error as exc:
            messagebox.showerror("上传失败", "上传失败，请联系管理员修复")

    def download_resume(self):
        """从 MinIO 下载指定学生的 PDF 简历"""
        student_name = self.entries['学生姓名'].get()
        if student_name:
            self.download_file_from_minio(student_name)
        else:
            messagebox.showerror("错误", "请先输入学生姓名")

    def download_file_from_minio(self, student_name):
        """从 MinIO 下载文件"""
        resume_name = student_name + "简历.pdf"

        # 用户选择保存文件的位置和文件名
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 initialfile=resume_name)
        if save_path:
            client = create_minio_client()
            bucket_name = "resume"
            try:
                # 从 MinIO 服务器下载文件
                client.fget_object(bucket_name, resume_name, save_path)
                messagebox.showinfo("下载成功", f"简历 {resume_name} 下载成功.")
            except S3Error as exc:
                # 如果遇到 S3Error 异常，显示下载失败信息
                messagebox.showerror("下载失败", "简历不存在")

if __name__ == "__main__":
    app = StudentInfoApp()
    app.mainloop()