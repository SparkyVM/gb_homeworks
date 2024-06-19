import requests
import time
import threading
import argparse

"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, 
название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
"""
PATH = 'images/'

def loader_thread(file):
    start_thread_time = time.time()
    response = requests.get(file)
    if response.status_code == 200:
        filename = file.split('/')[-1]
        with open(PATH + filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}    in {time.time() - start_thread_time:.2f} seconds")
    else:
        print('Ошибка при загрузке')

def func_loader (urls):
    threads = []
    start_time = time.time()

    for pic in urls:
        t = threading.Thread(target=loader_thread, args=(pic, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print('-'*20)
    print(f'Общее время выполнения программы - {time.time() - start_time:.2f}')

if __name__ =='__main__':

    parser = argparse.ArgumentParser(description='Downloading...')
    parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
    args = parser.parse_args()
    func_loader(args.list)

    # python .\\hw_4_cmd.py -l https://i.ytimg.com/vi/rxl6yAwAfJ8/maxresdefault.jpg https://i.pinimg.com/originals/09/ed/61/09ed61a7d7be574e298a2fc851a66df4.jpg https://i.pinimg.com/originals/be/98/4f/be984fa05eeb049647989f5e6ad68d5a.jpg