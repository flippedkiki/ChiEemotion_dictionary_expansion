# -*- coding: utf-8 -*-
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host = '192.168.235.36',  # 远程主机的ip地址，
                                            user = 'chili_select',   # MySQL用户名
                                            db = 'chili',   # database名
                                            passwd = 'chili_select',   # 数据库密码
                                            port = 3306,  #数据库监听端口，默认3306
                                            charset = "utf8")  #指定utf8编码的连接
cursor = conn.cursor()  # 创建一个光标，然后通过光标执行sql语句
cursor.execute("SELECT `body` FROM `news` WHERE `language` = 'chi' LIMIT 2000")
with open('resources','a') as f:
    for news in cursor.fetchall():
        f.write(''.join(news)+'\n') # 将cursor得到的数据全部写入'resources'文件中
cursor.close(); conn.close()  #最后记得关闭光标和连接，防止数据泄露