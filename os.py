#!/usr/bin/python3

import os
import sys
from pwd import getpwuid
import datetime

def statfile(f):
    format = 'Файл: '
    statinfo =  os.lstat(f)
    t1 = format + os.path.split(f)[1] + " Размер: " + str(statinfo.st_size) + " Владелец: " + str(getpwuid(statinfo.st_uid).pw_name)
    t1+= " Дата последнего изменения: " + datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    t1+= " Права доступа: " + str(oct(statinfo.st_mode)[-3:])
    return t1

def listdirs(s):
    n = 0
    for t in sorted(os.listdir(s)):
        if os.path.isdir(s+"/"+t):
            format = 'Каталог: '
            t1 = format + t
        else:
            s1 = s+"/"+t
            t1 = statfile(s1)
        print(t1)
        n += 1
    return n

if len(sys.argv) == 2:
    s = sys.argv[1]
    if os.path.isdir(s):
        print("Всего файлов и каталогов:", listdirs(s))
    elif os.path.isfile(s):
        print(statfile(s))
    else:
        print('Нет такого файла или каталога.')
else:
    print('Недостаточно аргументов')