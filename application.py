import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re
from user_session import UserSession
# 数据库连接
mydb = mysql.connector.connect(
    host="60.204.212.12",
    user="root",
    passwd="helloworld",
    database="InternshipSystem"
)

class InternshipApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  # 现在接受父级窗口作为参数
        self.pack(expand=True, fill=tk.BOTH)  # 确保填充父级窗口
        self.create_widgets()

    def create_widgets(self):
        # self.geometry("600x400")
        
        self.tabControl = ttk.Notebook(self)
        
        # Check user role and adjust tabs accordingly
        self.adjust_tabs_based_on_role()

        self.tabControl.pack(expand=1, fill="both")


    def create_student_tab(self):
        # 学生界面布局
        self.student_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.student_frame, text='学生')
        self.student_id_var = tk.IntVar()
        ttk.Label(self.student_frame, text="学生ID:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.student_frame, textvariable=self.student_id_var).grid(row=0, column=1, padx=10, pady=10)
        
        self.job_listbox = tk.Listbox(self.student_frame, width=50, height=15)
        self.job_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(self.student_frame, text="查看岗位", command=self.view_jobs).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.student_frame, text="申请岗位", command=self.apply_for_job).grid(row=2, column=1, padx=10, pady=10)

    def create_company_tab(self):
        # 企业界面布局
        self.company_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.company_frame, text='企业')
        self.company_id_var = tk.IntVar()
        ttk.Label(self.company_frame, text="企业ID:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.company_frame, textvariable=self.company_id_var).grid(row=0, column=1, padx=10, pady=10)
        
        self.application_listbox = tk.Listbox(self.company_frame, width=50, height=15)
        self.application_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(self.company_frame, text="查看申请", command=self.view_applications).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.company_frame, text="接受申请", command=lambda: self.update_application_status('accepted')).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(self.company_frame, text="拒绝申请", command=lambda: self.update_application_status('rejected')).grid(row=2, column=2, padx=10, pady=10)
    def get_user_role(self):
        user_id = UserSession.get_user_id()
        if user_id:
            cursor = mydb.cursor()
            cursor.execute("SELECT Role FROM User WHERE Username = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
        return None
    def adjust_tabs_based_on_role(self):
        role = self.get_user_role()
        
        if role == '学生':
            self.create_student_tab()
        elif role == '企业':
            self.create_company_tab()
        elif role =='管理员':
            self.create_student_tab()
            self.create_company_tab()
        else:
            messagebox.showerror("错误", "不可用的身份.")
    def view_jobs(self):
        self.job_listbox.delete(0, tk.END)
        cursor = mydb.cursor()
        query = """
        SELECT Internship.JobID, Internship.JobDescription, Company.Name
        FROM Internship
        JOIN Company ON Internship.CompanyID = Company.CompanyID
        """
        cursor.execute(query)
        jobs = cursor.fetchall()
        for job in jobs:
            self.job_listbox.insert(tk.END, f"工作ID:{job[0]}, 公司名称: {job[2]}, 岗位描述: {job[1]}")

    def apply_for_job(self):
        selected_job = self.job_listbox.get(tk.ACTIVE)
        if selected_job:
            # 使用正则表达式提取 JobID
            match = re.search(r"工作ID:(\d+)", selected_job)
            if match:
                job_id = int(match.group(1))
                student_id = self.student_id_var.get()

                # 检查学生是否已经申请过该公司的任何岗位
                cursor = mydb.cursor()
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM Application
                    JOIN Internship ON Application.JobID = Internship.JobID
                    WHERE Application.StudentID = %s AND Internship.CompanyID = (
                        SELECT CompanyID FROM Internship WHERE JobID = %s
                    )
                    """,
                    (student_id, job_id)
                )
                count = cursor.fetchone()[0]
                if count > 0:
                    messagebox.showwarning("警告", "您已经申请过该公司的岗位，请勿重复投递")
                else:
                    cursor.execute("INSERT INTO Application (StudentID, JobID, ApplicationStatus) VALUES (%s, %s, %s)",(student_id, job_id, 'applied'))
                    # mydb.commit()
                    messagebox.showinfo("成功", "申请成功提交")
            else:
                messagebox.showwarning("警告", "无法提取岗位ID")
        else:
            messagebox.showwarning("警告", "请选择一个岗位进行申请")

    def view_applications(self):
        self.application_listbox.delete(0, tk.END)
        company_id = self.company_id_var.get()
        cursor = mydb.cursor()
        query = """
        SELECT Application.ApplicationID, Student.Name, Application.JobID, Application.ApplicationStatus 
        FROM Application 
        JOIN Student ON Application.StudentID = Student.StudentID 
        WHERE Application.JobID IN (SELECT JobID FROM Internship WHERE CompanyID = %s)
        """
        cursor.execute(query, (company_id,))
        applications = cursor.fetchall()
        for app in applications:
            self.application_listbox.insert(tk.END, f"申请号: {app[0]}, 申请人: {app[1]}, 岗位ID: {app[2]}, 状态: {app[3]}")

    def update_application_status(self, status):
        selected_app = self.application_listbox.get(tk.ACTIVE)
        if selected_app:
            # 使用正则表达式提取 申请号
            match = re.search(r"申请号: (\d+)", selected_app)
            if match:
                application_id = int(match.group(1))
                cursor = mydb.cursor()
                cursor.execute(
                    "UPDATE Application SET ApplicationStatus = %s WHERE ApplicationID = %s", 
                    (status, application_id)
                )
                mydb.commit()
                messagebox.showinfo("成功", f"申请状态已更新为 {status}")
                self.view_applications()
            else:
                messagebox.showwarning("警告", "无法提取申请ID")
        else:
            messagebox.showwarning("警告", "请选择一个申请进行更新")

if __name__ == "__main__":
    app = InternshipApp()
    app.mainloop()