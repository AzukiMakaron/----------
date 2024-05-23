import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ReviewApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.connection = self.connect_to_database()
        self.setup_gui()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="60.204.212.12",
                user="root",
                password="helloworld",
                database="InternshipSystem"
            )
            print("数据库连接成功")
            return connection
        except mysql.connector.Error as e:
            print("数据库连接失败:", e)
            return None

    def setup_gui(self):
        self.pack(fill=tk.BOTH, expand=True)

        # 创建左侧的文本框用于显示评价信息
        self.review_text_box = tk.Text(self, height=15, width=50)
        self.review_text_box.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

        # 创建界面元素，放置在右侧
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=0, column=1, sticky="n")

        tk.Label(entry_frame, text="学生ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.student_id_entry = tk.Entry(entry_frame)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        tk.Label(entry_frame, text="工作ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.job_id_entry = tk.Entry(entry_frame)
        self.job_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(entry_frame, text="评分:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.score_entry = tk.Entry(entry_frame)
        self.score_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(entry_frame, text="评论:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.comment_entry = tk.Entry(entry_frame)
        self.comment_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.create_button = tk.Button(entry_frame, text="创建评价", command=self.create_review_button_clicked)
        self.create_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.fetch_button = tk.Button(entry_frame, text="获取评价", command=self.fetch_reviews_button_clicked)
        self.fetch_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.fetch_all_button = tk.Button(entry_frame, text="获取所有评价", command=self.fetch_all_reviews)
        self.fetch_all_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def display_reviews(self, reviews):
        """
        将查询出的评价数据显示在文本框中。
        """
        self.review_text_box.delete('1.0', tk.END)
        if not reviews:
            self.review_text_box.insert(tk.END, "没有找到任何评价\n")
        else:
            for review in reviews:
                self.review_text_box.insert(tk.END, f"公司名称: {review[0]}, 评分: {review[1]}, 评论: {review[2]}\n")

    def fetch_reviews(self, student_id):
        try:
            cursor = self.connection.cursor()
            sql = """
            SELECT c.Name, r.Score, r.Comment
            FROM InternshipReview r
            JOIN Internship i ON r.JobID = i.JobID
            JOIN Company c ON i.CompanyID = c.CompanyID
            WHERE r.StudentID = %s
            """
            val = (student_id,)
            cursor.execute(sql, val)
            reviews = cursor.fetchall()
            self.display_reviews(reviews)
        except mysql.connector.Error as e:
            messagebox.showerror("错误", "获取评价时出错，请稍后再试。")

    def fetch_reviews_button_clicked(self):
        student_id = self.student_id_entry.get()
        if student_id:
            self.fetch_reviews(student_id)
        else:
            messagebox.showinfo("提示", "请输入学生ID")

    def create_review(self, student_id, job_id, score, comment):
        try:
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO InternshipReview (StudentID, JobID, Score, Comment)
            VALUES (%s, %s, %s, %s)
            """
            val = (student_id, job_id, score, comment)
            cursor.execute(sql, val)
            self.connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            messagebox.showerror("错误", "创建评价时出错，请稍后再试。")
            return 0

    def create_review_button_clicked(self):
        student_id = self.student_id_entry.get()
        job_id = self.job_id_entry.get()
        score = self.score_entry.get()
        comment = self.comment_entry.get()
        if student_id and job_id and score and comment:
            rows_changed = self.create_review(student_id, job_id, score, comment)
            if rows_changed > 0:
                messagebox.showinfo("成功", "评价创建成功")
                self.fetch_reviews(student_id)  # Optionally refresh the list
            else:
                messagebox.showinfo("失败", "评价创建失败")
        else:
            messagebox.showinfo("提示", "请填写所有字段")

    def fetch_all_reviews(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT c.Name, r.Score, r.Comment FROM InternshipReview r JOIN Internship i ON r.JobID = i.JobID JOIN Company c ON i.CompanyID = c.CompanyID"
            cursor.execute(sql)
            reviews = cursor.fetchall()
            self.display_reviews(reviews)
        except mysql.connector.Error as e:
            messagebox.showerror("错误", "获取所有评价时出错，请稍后再试。")

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("实习评价系统")
#     app = ReviewApp(root)
#     root.mainloop()