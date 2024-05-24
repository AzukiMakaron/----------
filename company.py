import tkinter as tk
from tkinter import messagebox
from discussion import DiscussionFrame
from student_resume_manage import StudentResumeFrameWork
import mysql.connector
import minio
from application import InternshipApp
from internship_review import ReviewApp
from work_log import LogManager
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
def main2():
    root = tk.Tk()
    root.title("学生实习信息管理系统 企业端")

    # 设置窗口大小和位置
    window_width = 800
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    welcome_label = tk.Label(root, text="欢迎使用学生实习信息管理系统中心v0.1\n作者:豆粉不想敲，申漪漪想摆烂，牛基基拖油瓶，皓皓想吐槽，世博不干活", font=('Arial', 16), pady=200)
    welcome_label.pack()
    # 创建主容器用于放置不同模块的 Frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
   
    def switch_frame(frame_class):
        # 清除当前内容
        for widget in main_frame.winfo_children():
            widget.destroy()
        # 隐藏 welcome_label
        welcome_label.pack_forget()
        # 创建新的 Frame
        frame = frame_class(main_frame)
        frame.pack(fill=tk.BOTH, expand=True)

    # 定义各模块的 Frame 类
    class StudentResumeFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            tk.Label(self, text="学生简历信息管理与查询界面").pack()
            # 在这里添加更多控件
            self.student_resume_manage_frame = StudentResumeFrameWork(self,minio_client,db)
            self.student_resume_manage_frame.pack(fill=tk.BOTH, expand=True)

    class ApplicationFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            tk.Label(self, text="岗位和应聘").pack()
            # 在这里添加更多控件
            self.application_frame = InternshipApp(self)
            self.application_frame.pack(fill=tk.BOTH, expand=True)

    # class InternshipReviewFrame(tk.Frame):
    #     def __init__(self, parent):
    #         super().__init__(parent)
    #         tk.Label(self, text="实习评价").pack()
    #         # 在这里添加更多控件
    #         self.internship_review_frame = ReviewApp(self)
    #         self.internship_review_frame.pack(fill=tk.BOTH, expand=True)

    # class WorkLogFrame(tk.Frame):
    #     def __init__(self, parent):
    #         super().__init__(parent)
    #         tk.Label(self, text="学生工作日志").pack()
    #         # 在这里添加更多控件
    #         self.work_log_frame = LogManager(self)
    #         self.work_log_frame.pack(fill=tk.BOTH, expand=True)

    # 重命名本地的 DiscussionFrame 类
    class LocalDiscussionFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            # tk.Label(self, text="讨论区").pack()
            # 创建 discussion.py 中的 DiscussionFrame 实例
            self.discussion_frame = DiscussionFrame(self)
            self.discussion_frame.pack(fill=tk.BOTH, expand=True)

    # 添加菜单按钮和事件处理
    menu_frame = tk.Frame(root)
    menu_frame.pack(side=tk.TOP, fill=tk.X)
    # 使用重命名后的 LocalDiscussionFrame
    # tk.Button(menu_frame, text="讨论区", command=lambda: switch_frame(LocalDiscussionFrame)).pack(side=tk.LEFT)
    
    # 添加菜单按钮
    menu_frame = tk.Frame(root)
    menu_frame.pack(side=tk.TOP, fill=tk.X)
    tk.Button(menu_frame, text="学生简历信息管理与查询界面", command=lambda: switch_frame(StudentResumeFrame)).pack(side=tk.LEFT)
    tk.Button(menu_frame, text="岗位和应聘", command=lambda: switch_frame(ApplicationFrame)).pack(side=tk.LEFT)
    # tk.Button(menu_frame, text="实习评价", command=lambda: switch_frame(InternshipReviewFrame)).pack(side=tk.LEFT)
    # tk.Button(menu_frame, text="学生工作日志", command=lambda: switch_frame(WorkLogFrame)).pack(side=tk.LEFT)
    tk.Button(menu_frame, text="讨论区", command=lambda: switch_frame(LocalDiscussionFrame)).pack(side=tk.LEFT)

    root.mainloop()

# if __name__ == "__main__":
#     main()