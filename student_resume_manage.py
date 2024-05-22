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

    def upload_file_to_minio(self, filepath):
        client = create_minio_client()
        bucket_name = "resume"  # 存数据桶的名字
        object_name = os.path.basename(filepath)
        try:
            client.fput_object(bucket_name, object_name, filepath)
            messagebox.showinfo("上传成功", f"简历 {filepath} 上传成功.")
        except S3Error as exc:
            messagebox.showerror("上传失败", "上传失败，请联系管理员修复")

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
    # def save_resume_info(self, user_id, file_name): #同步将文件存入数据库，做权限认证
    #     try:
    #         mycursor = mydb.cursor()
    #         sql = "INSERT INTO resumes (user_id, file_name) VALUES (%s, %s)"
    #         val = (user_id, file_name)
    #         mycursor.execute(sql, val)
    #         mydb.commit()
    #     except mysql.connector.Error as err:
    #         messagebox.showerror("数据库错误，请联系管理员")
    def download_resume(self):
        try:
            mycursor = mydb.cursor()
            sql = "SELECT file_name FROM resumes WHERE user_id = %s"
            val = (sign_in.userId,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            if result:
                file_name = result[0]
                self.download_file_from_minio(file_name)
            else:
                messagebox.showwarning("无简历", "当前用户没有上传简历。")
        except mysql.connector.Error as err:
            messagebox.showerror("数据库错误", f"无法查询简历信息: {err}")

    def download_file_from_minio(self, file_name):
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 initialfile=file_name)
        if save_path:
            client = create_minio_client()
            bucket_name = "resume"
            try:
                client.fget_object(bucket_name, file_name, save_path)
                messagebox.showinfo("下载成功", f"简历 {file_name} 下载成功.")
            except S3Error as exc:
                messagebox.showerror("下载失败", "下载失败，请联系管理员修复")

if __name__ == "__main__":
    app = StudentInfoApp()
    app.mainloop()