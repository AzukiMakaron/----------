import mysql.connector
from tkinter import filedialog, Tk
import os

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='60.204.217.157',
            user='root',
            password='helloworld',
            database='StudentFiles'
        )
        self.cursor = self.conn.cursor()

    def insert_pdf_record(self, filename, oss_url):
        query = "INSERT INTO PDFUploads (filename, oss_url) VALUES (%s, %s)"
        self.cursor.execute(query, (filename, oss_url))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

def upload_file_to_oss(file_path):
    # 这里应替换为 OSS 上传逻辑
    # 模拟返回 OSS 上的 URL
    return f"http://60.204.217.157:9000/{os.path.basename(file_path)}"

def select_and_upload():
    root = Tk()
    root.withdraw()  # 隐藏 Tkinter 主窗口
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        oss_url = upload_file_to_oss(file_path)
        filename = os.path.basename(file_path)
        db_manager = DatabaseManager()
        db_manager.insert_pdf_record(filename, oss_url)
        db_manager.close()
        print(f"文件 {filename} 存入MySQL.")

