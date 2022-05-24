#下载器
from cmath import inf
import time
import win32com
from win32com.client import Dispatch, constants
thunder = win32com.client.Dispatch('ThunderAgent.Agent64.1')

tasklist = []

def read_config(sourcepath):
   f = open(sourcepath,encoding = "utf-8")
   lines = f.readlines()
   f.close()
   for line in lines:
       row =  line.replace('\\n','').split(',')
       info = []
       for attr in row: info.append(attr)
       tasklist.append(info)
   

def add_task(info):
     print('\n')
     print( "添加任务：" + repr(info))
     print('\n')
     thunder.AddTask(info[1], info[0], "E://Download/电影天堂/")
     thunder.CommitTasks()

def main():
    #下载
    while(len(tasklist) > 0): 
        info = tasklist[0]
        tasklist.remove(info)
        add_task(info)
        time.sleep(5*60)
        



if __name__ == '__main__':
    read_config('E://Download/dy2018_movie.txt')
    print('爬虫启动成功！')
    main()
    print('爬虫执行完毕！')
   