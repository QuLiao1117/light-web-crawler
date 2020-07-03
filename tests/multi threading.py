#!/usr/bin/python3
# encoding=utf-8
from multiprocessing import Pool
import time
import os

def action1(a, b=50):
    for i in range(b):
        print(a, os.getpid(), ' ', i)  # os.getpid(): pid简单来说就是每个进程的“身份证”
        time.sleep(0.1)

if __name__ == '__main__':  # 还要添加这行，否则可能出现异常

    ci = Pool(3)  # 创建一个进程池，容量为3个进程
    ci.apply_async(action1, args=('进程一',))  # 启动第一个子进程...
    ci.apply_async(action1, args=('进程二', 50))  # 和普通进程的启动方式有很大不同仔细看
    ci.apply_async(action1, args=('进程三', 60))  # Pool的最基本格式记住←
# 注意：程序现在有4个进程在运行：上面的三个子进程 和一个最为核心的：主进程

    ci.close()  # 关闭进程池（但池子内已启动的子进程还会继续进行）
    ci.join()  # 等待进程池内的所有子进程完毕
    print('比如说这最后的一行输出就是主进程执行任务打印出来的')
