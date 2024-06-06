# 15_sem_5
"""
Функция получает на вход текст вида: “1-й четверг ноября”, “3-я среда мая” и т.п.
Преобразуйте его в дату в текущем году.
Логируйте ошибки, если текст не соответсвует формату.

Дорабатываем задачу 4.
- Добавьте возможность запуска из командной строки.
- При этом значение любого параметра можно опустить. В этом случае берётся первый в месяце день недели, текущий день недели и/или текущий месяц.
* Научите функцию распознавать не только текстовое названия дня недели и месяца, но и числовые, т.е не мая, а 5.
"""

from datetime import datetime
import logging
import argparse

WEEKDAYS = ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']
MONTHS = ['янв','фев','мар','апр','мая','июн','июл','авг','сен','окт','ноя','дек']

logger = logging.getLogger(__name__)
my_format = '{levelname:<10} {asctime:<25} {funcName} {msg}'

logging.basicConfig(filename='mylog1.log', filemode='a', encoding='utf-8', level=logging.INFO, style='{', format=my_format)

def is_cnt_day(item: str) -> bool:
    if '-' in item:
        return True

def is_day_of_week(item: str) -> bool:
    if item in WEEKDAYS:
        return True
    
def is_month(item: str) -> bool:
    if item[:3] in MONTHS:
        return True

def what_day (dt: str) -> int:
    global WEEKDAYS
    global MONTHS
    dt_list = dt.split()
    if len(dt_list) == 3:
        cnt, weekday, month = dt_list
        cnt = int(cnt[0])
        if weekday in WEEKDAYS:
            weekday = WEEKDAYS.index(weekday)
        else:
            logger.error(msg='Неверный формат дня недели')
        if month[:3] in MONTHS:
            month = [i+1 for i in range(len(MONTHS)) if month.startswith(MONTHS[i])][0]
        else:
            logger.error(msg='Неверный формат месяца')
        first_day = datetime(year=datetime.now().year, month=month, day=1).weekday()
        WEEKDAYS = WEEKDAYS[first_day:] + WEEKDAYS[:first_day]

    else:           # Обработка, если один из параметров опущен
        if is_month(dt_list[1]):            # обработка месяца
            month = [i+1 for i in range(len(MONTHS)) if dt_list[1].startswith(MONTHS[i])][0]
        elif is_month(dt_list[0]):
            month = [i+1 for i in range(len(MONTHS)) if dt_list[0].startswith(MONTHS[i])][0]
        else:
            month = datetime.now().month        

        if is_day_of_week(dt_list[1]):      # обработка дня недели
            weekday = WEEKDAYS.index(dt_list[1])
        elif is_day_of_week(dt_list[0]):
            weekday = WEEKDAYS.index(dt_list[0])
        else:
            weekday = datetime.now().weekday()

        if is_cnt_day(dt_list[0]):
            cnt = int(dt_list[0][0])
        else:
            cnt = 1
    day = 1
                    # Поиск даты
    while True:
        if datetime(year=datetime.now().year, month=month, day=day).weekday() == weekday:            
            cnt -= 1
            if not cnt:
                return datetime(year=datetime.now().year, month=month, day=day).date()
        day += 1

#print(what_day('1-я среда'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lets find a date...')
    parser.add_argument('string', metavar='N', type=str, nargs='*', help='input some string')
    args = parser.parse_args()
    print(what_day(*args.string))
    # python .\\gb_task_15.py '1-й четверг ноября'
