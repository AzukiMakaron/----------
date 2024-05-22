#登录界面
import mysql.connector

mydb = mysql.connector.connect(
  host="60.204.212.12",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="helloworld",   # 数据库密码
  database="InternshipSystem" #数据库
)


# mycursor=mydb.cursor()
# sql="select UserID from User where Username= %s"
# username=('zws',)
# mycursor.execute(sql,username)
# myresult=mycursor.fetchall()
userId=1

