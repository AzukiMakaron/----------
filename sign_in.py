import tkinter as tk
from admin  import main
from student import main1
from company import main2
from tkinter import  messagebox
import mysql.connector
from user_session import UserSession
# 创建数据库
conn =  mysql.connector.connect(
     host = "60.204.212.12", # 数据库主机地址
     user = "root", # 数据库用户名
     passwd = "helloworld", # 数据库密码
     database = "InternshipSystem"
)

# 获取游标
cursor = conn.cursor()

# def get_user_role(user_name):
#     """从数据库获取用户角色"""
#     try:
#         connection = conn
#         cursor = connection.cursor()
#         cursor.execute("SELECT Role FROM User WHERE Username = %s", (user_name,))
#         role = cursor.fetchone()
#         return role[0] if role else None
#     except mysql.connector.Error as e:
#         print(f"Error: {e}")
#     finally:
#         if connection:
#             connection.close()

#调用函数登录注册屏幕居中
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def getLoginUser(username):
    sql="select Role from User where Username=%s"
    cursor.execute(sql,(username,))
    role=cursor.fetchone()
    return role[0] if role else None
# 创建登录界面
def login(username, password):
    connection = conn
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM User WHERE Username=%s AND Password=%s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()

            if user:
                UserSession.set_user_id(user[0])  # 假设用户ID是查询结果的第一列
                role = user[2]  # 角色信息在元组中的第三个位置
                if role == '管理员':
                    messagebox.showinfo("登录成功", "欢迎回来，{}管理员".format(username))
                    window.destroy()
                    open_new_admin()
                elif role == '学生':
                    messagebox.showinfo("登录成功", "欢迎回来，{}学生".format(username))
                    window.destroy()
                    open_new_student()
                elif role == '企业':
                    messagebox.showinfo("登录成功", "欢迎回来，{}公司".format(username))
                    window.destroy()
                    open_new_company()
                else:
                    messagebox.showerror("错误", "未知身份角色！")
            else:
                messagebox.showerror("登录失败", "用户名或密码错误，请重试")
    except mysql.connector.Error as e:
        print(f"错误: {e}")
def get_current_user():
    """获取当前登录用户"""
    return entry_login_username.get()
#负责跳转管理员功能界面函数
def open_new_admin():
    main()

#负责跳转公司功能函数
def open_new_student():
    main1()

#负责跳转公司功能界面
def open_new_company():
    main2()


def zhuce():
    # Get username and password from entry widgets
    username = entry_reg_username.get()
    password = entry_reg_password.get()
    confirm_password = entry_confirm_password.get()
    role = role_var.get()  # 获取身份信息

    # 检查输入的两次的密码是否相同
    if password != confirm_password:
        messagebox.showerror("注册失败", "两次密码不相同")
        return

        # 创建游标
    cursor = conn.cursor()


    sql_check_username="SELECT * FROM User WHERE Username = %s"
    cursor.execute(sql_check_username,(username,))
    existing_user=cursor.fetchone()

#判断用户名是否已经存在
    if existing_user:
        messagebox.showerror("注册失败","用户名已存在")
        # cursor.close()
        # conn.close()
        return




    # 插入用户名和密码到 users 表中
    sql = "INSERT INTO User (username, password, role) VALUES (%s, %s, %s)"
    val = (username, password, role)
    cursor.execute(sql, val)



    # 提交更改
    conn.commit()

    # 关闭游标和数据库连接
    # cursor.close()
    # conn.close()

    # 显示注册成功信息
    messagebox.showinfo("注册成功", "用户{}，注册成功!".format(username))




#函数跳转负责隐藏注册界面显示登录界面
def switch_to_login():
    zhuce_frame.pack_forget()
    login_frame.pack()


#函数跳转负责隐藏登录界面显示注册界面
def switch_to_zhuce():
    login_frame.pack_forget()
    zhuce_frame.pack()


# 创建新窗口并居中屏幕
window = tk.Tk()
window.title("登录注册界面")

window_width = 800
window_height = 600
center_window(window, window_width, window_height)



# 设计登录界面
login_frame = tk.Frame(window)


#登录用户名文本框
label_login_username = tk.Label(login_frame, text="用户名：")
label_login_username.pack()
entry_login_username = tk.Entry(login_frame)
entry_login_username.pack()

#登录密码文本框
label_login_password = tk.Label(login_frame, text="密码：")
label_login_password.pack()
entry_login_password = tk.Entry(login_frame, show="*")
entry_login_password.pack()

#登录按钮
button_login = tk.Button(login_frame, text="登录",command=lambda: login(entry_login_username.get(), entry_login_password.get()))#lamba后面的用于返回当点击登录按钮时，将会调用login函数，并传入文本框中的用户名和密码作为参数。非常抱歉给您带来的困惑。
button_login.pack()
username=entry_login_username.get()

#注册按钮
button_switch_to_zhuce = tk.Button(login_frame, text="注册", command=switch_to_zhuce)
button_switch_to_zhuce.pack()


# 设计创造注册界面
zhuce_frame = tk.Frame(window)

#用户名文本框
label_reg_username = tk.Label(zhuce_frame, text="用户名：")
label_reg_username.pack()
entry_reg_username = tk.Entry(zhuce_frame)
entry_reg_username.pack()
#密码文本框
label_reg_password = tk.Label(zhuce_frame, text="密码：")
label_reg_password.pack()
entry_reg_password = tk.Entry(zhuce_frame, show="*")
entry_reg_password.pack()
#确认密码文本框
label_confirm_password = tk.Label(zhuce_frame, text="确认密码：")
label_confirm_password.pack()
entry_confirm_password = tk.Entry(zhuce_frame, show="*")
entry_confirm_password.pack()

#身份下拉框
label_role = tk.Label(zhuce_frame, text="身份：")
label_role.pack()
role_var = tk.StringVar(zhuce_frame)
role_var.set("学生")  # 默认选择学生角色
role_dropdown = tk.OptionMenu(zhuce_frame, role_var, "学生", "企业", "管理员")
role_dropdown.pack()

#注册按钮
button_register = tk.Button(zhuce_frame, text="注册", command=zhuce)
button_register.pack()
#返回登录按钮
button_switch_to_login = tk.Button(zhuce_frame, text="返回登录", command=switch_to_login)
button_switch_to_login.pack()

current_username=entry_login_username.get()
wel_label = tk.Label(window, text="欢迎使用学生实习信息管理系统", font=("Arial", 20))
wel_label.pack()
# 最初显示登录界面
login_frame.pack()


if __name__ == '__main__':
    window.mainloop()