import tkinter as tk
from tkinter import filedialog, font as tkfont

class StudentInfoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("学生信息和简历上传")
        self.geometry("400x350")  # 设置窗口大小
        self.resizable(False, False)  # 窗口大小不可变

        self.custom_font = tkfont.Font(family="Helvetica", size=12)  # 自定义字体

        # 创建并放置标签和输入框
        labels = [
            '学生姓名', '学生院系', '学生专业', '所在班级', '班主任', '课程成绩', '个人技能'
        ]
        self.entries = {}
        for i, label in enumerate(labels):
            lbl = tk.Label(self, text=label + "：", font=self.custom_font)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry_var = tk.StringVar()
            entry = tk.Entry(self, textvariable=entry_var, font=self.custom_font)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[label] = entry_var

        # 创建并放置按钮
        upload_btn = tk.Button(self, text="上传 PDF 简历", command=self.select_file, font=self.custom_font)
        upload_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        save_btn = tk.Button(self, text="保存数据到 MySQL", command=self.save_data, font=self.custom_font)
        save_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def select_file(self):
        """选择文件并上传到 MinIO"""
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.upload_file_to_minio(file_path)

    def upload_file_to_minio(self, filepath):
        """模拟上传文件到 MinIO"""
        print(f"Uploading {filepath} to MinIO...")

    def save_data(self):
        """模拟保存数据到数据库"""
        data = {label: entry.get() for label, entry in self.entries.items()}
        print("Saving to MySQL:", data)

# 应用主程序入口
if __name__ == "__main__":
    app = StudentInfoApp()
    app.mainloop()