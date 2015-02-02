# coding:utf-8
import time
import base64
import os
import sys
import re
import threading
import _winreg
import hashlib
from multiprocessing.dummy import Pool as ThreadPool
from shutil import copy2

print u'''
            * * * * * * * * * * * * * * * * * * * *
                           使用方法
            1. 将要备份好友的聊天记录导出为mht格式
            2. 与该文件放在同一文件夹下
            3. 执行该文件
            * * * * * * * * * * * * * * * * * * * *
'''

thread_num = 20
curr_path = os.path.dirname(sys.argv[0])
mht_pic_md5 = []


# 获取所有mht文件的完整路径，返回列表
def get_mht_list():
    tmp = os.listdir(curr_path)
    # 获取所有mht文件名
    tmp[:] = [n for n in tmp if n.lower().endswith('.mht')]
    # 拼接mht文件的完整路径
    mht_list = [curr_path+os.sep+n for n in tmp]
    return mht_list


# 获取所有mht文件中base64编码的图片
def get_mht_pic(mht_list):
    pattern = re.compile(r'\.dat\n\n([\s\S]*?)\n\n')
    for mht in mht_list:
        with open(mht, 'r') as f:
            tmp = pattern.findall(f.read())
            # 对base64编码的图片解码并计算md5
            md5 = lambda x: hashlib.md5(base64.b64decode(''.join(x.split('\n')))).hexdigest()
            tmp[:] = [md5(n) for n in tmp]
            # tmp[:] = [''.join(n.split('\n')) for n in tmp]
        mht_pic_md5.extend(tmp)


# 获取QQ所有图片完整路径，返回列表
def get_pic_list(img_path):
    pic_list = []
    for path, dirs, files in os.walk(img_path):
        pic_list.extend([os.path.join(path, f) for f in files])
    return pic_list


# 修饰器，线程加锁
mutex = threading.Lock()
def add_mutex(func):
    def dector(*args, **kwargs):
        mutex.acquire()
        func(*args, **kwargs)
        mutex.release()
    return dector


# 若图片匹配，备份
@add_mutex
def backup(pic):
    with open(pic, 'rb') as f:
        pic_stream = f.read()
        # if base64.b64encode(pic_stream) in mht_pic_md5:
        if hashlib.md5(pic_stream).hexdigest() in mht_pic_md5:
            pic_bak = 'bak' + os.path.dirname(pic.split(':')[1])
            print pic
            try:
                if not os.path.exists(pic_bak):
                    os.makedirs(pic_bak)
            except:
                pass
            copy2(pic, pic_bak)


def main():
    mht_list = get_mht_list()
    if not mht_list:
        print u'请确保目录下有mht文件\n'
        return
    print u'共有%s个mht文件中的图片需要备份\n'%len(mht_list)

    print u'请输入你的QQ号码(6-10位纯数字)：'
    qq = raw_input()
    print u'正在搜索mht文件中待备份图片，请稍后....'
    get_mht_pic(mht_list)
    if not mht_pic_md5:
        print u'mht文件中未包含可备份图片\n'
        return
    print u'共找到%s张待备份图片'%len(mht_pic_md5)
    # QQ图片文件夹
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders')
    documents_path = _winreg.QueryValueEx(key, 'Personal')[0]
    img_path = documents_path + os.sep + 'Tencent Files/' + qq + '/Image/'
    print u'正在统计QQ聊天记录图片, 请稍后....'
    pic_list = get_pic_list(img_path)
    if not pic_list:
        print u'未找到QQ聊天记录图片文件夹，请确保输入了正确的QQ号码\n'
        main()
    
    pool = ThreadPool(thread_num)
    print u'正在备份....'
    pool.map(backup, pic_list)
    print u'备份完成\n图片保存在当前路径的bak文件夹下\n'


if __name__ == '__main__':
    main()
    os.system('pause')
