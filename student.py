#首页实现
import tkinter as tk
from tkinter import messagebox

def open_module(module_name):
    try:
        if module_name == "学生简历信息管理与查询界面":
            import student_resume_manage
            student_resume_manage.run()
     #  elif module_name == "岗位和应聘":
     #     import application
     #       application.run()
        elif module_name == "实习评价":
            import internship_review
            internship_review.run()
        elif module_name == "学生工作日志":
            import work_log
            work_log.run()
        elif module_name == "讨论区":
            import discussion
            discussion.run()
    except ImportError:
        messagebox.showerror("错误", f"模块 {module_name} 未找到.")

def main1():
    root = tk.Tk()
    root.title("学生实习信息管理系统")
     # 设置窗口大小和位置
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    tk.Button(root, text="学生简历信息管理与查询界面", command=lambda: open_module("学生简历信息管理与查询界面")).pack(pady=10)
 #   tk.Button(root, text="岗位和应聘", command=lambda: open_module("岗位和应聘")).pack(pady=10)
    tk.Button(root, text="实习评价", command=lambda: open_module("实习评价")).pack(pady=10)
    tk.Button(root, text="学生工作日志", command=lambda: open_module("学生工作日志")).pack(pady=10)
    tk.Button(root, text="讨论区", command=lambda: open_module("讨论区")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main1()