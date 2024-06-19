import requests
import time
import threading
import multiprocessing
import asyncio, aiohttp, aiofiles

"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, 
название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
"""
PATH = 'images/'
urls = ['https://i.pinimg.com/originals/21/7a/02/217a027d0fa652a3c447aa91318c3e28.jpg',
    'https://i.ytimg.com/vi/rxl6yAwAfJ8/maxresdefault.jpg',
    'https://i.pinimg.com/originals/09/ed/61/09ed61a7d7be574e298a2fc851a66df4.jpg',
    'https://i.pinimg.com/originals/be/98/4f/be984fa05eeb049647989f5e6ad68d5a.jpg',
    'https://wallbox.ru/resize/2560x1440/wallpapers/main/201313/dcd91dfae5e0d6e.jpg',
    'https://wallpapers.com/images/hd/silly-cat-pictures-2038-x-1409-kwcruupdy87dek93.jpg'
]

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

def loader_process(file):
    start_process_time = time.time()
    response = requests.get(file)
    if response.status_code == 200:
        filename = file.split('/')[-1]
        with open(PATH + filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}    in {time.time() - start_process_time:.2f} seconds")
    else:
        print('Ошибка при загрузке')

async def loader_async(file):
    start_async_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(file) as response:
            if response.status == 200:
                filename = file.split('/')[-1]
                async with aiofiles.open(PATH + filename, 'wb') as f:   
                    await f.write(await response.read())
                print(f"Downloaded {filename}    in {time.time() - start_async_time:.2f} seconds")


async def main_async():
    tasks = [asyncio.create_task(loader_async(file)) for file in urls]
    await asyncio.gather(*tasks)

if __name__ =='__main__':

    regim = int(input("Введите режим выполнения (1-многопоточный, 2-многопроцессорный 3-асинхронный): "))
    if regim == 1:
        print('Выбран многопоточный режим')
        print('-'*20)
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
    elif regim == 2:
        print('Выбран многопроцессорный режим')
        print('-'*20)

        processes = []
        start_time = time.time()

        for pic in urls:
            p = multiprocessing.Process(target=loader_thread, args=(pic, ))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        print('-'*20)
        print(f'Общее время выполнения программы - {time.time() - start_time:.2f}')
    elif regim == 3:
        print('Выбран асинхронный режим')
        print('-'*20)
        start_time = time.time()
        asyncio.run(main_async())
        print('-'*20)
        print(f'Общее время выполнения программы - {time.time() - start_time:.2f}')

    else:
        print('Не корректный режим')