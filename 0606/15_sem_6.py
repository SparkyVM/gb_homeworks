# 15_sem_6
"""
Напишите код, который запускается из командной строки и получает на вход путь до директории на ПК.
Соберите информацию о содержимом в виде объектов namedtuple.
Каждый объект хранит:
- имя файла без расширения или название каталога,
- расширение, если это файл,
- флаг каталога,
- название родительского каталога.
В процессе сбора сохраните данные в текстовый файл используя логирование.
"""

import os
from collections import namedtuple
import logging
import argparse

#PATH_FILE = os.path.join(os.getcwd(), 'dir')
logger = logging.getLogger(__name__)
my_format = '{levelname:<10} {asctime:<25} {funcName} {msg}'

logging.basicConfig(filename='mylog1.log', filemode='a', encoding='utf-8', level=logging.INFO, style='{', format=my_format)

File_info = namedtuple('File_info', ['name','extension','is_dir','parent'])

def traverse_directory(directory) -> list:
    results = []
    for root, dirs, files in os.walk(directory,topdown=False):
        if dirs:
            for d in dirs:
                temp_parent = str(root).split('\\')[-1]
                add_obj = File_info(d, '-', True, temp_parent)
                results.append(add_obj)
        if files:
            for f in files:
                temp_full_name = f.split('.')
                temp_parent = str(root).split('\\')[-1]
                add_obj = File_info(temp_full_name[0], temp_full_name[1], False, temp_parent)
                results.append(add_obj)    
    for item in results:
        logger.info(msg=f'{item.name:<20}{item.extension:<8}{item.is_dir:<8}{item.parent:<10}')
        #print(f'{item.name:<20}{item.extension:<8}{item.is_dir:<8}{item.parent:<10}')

#traverse_directory(PATH_FILE)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show directory')
    parser.add_argument('string', metavar='N', type=str, nargs='*', help='input some string')
    args = parser.parse_args()
    traverse_directory(*args.string)
    # python .\\gb_task_15.py 'D:\My\Book\PyFolder\gb_task\dir'
