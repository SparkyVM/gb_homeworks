# 15_1
"""
Возьмите любые 1-3 задания из прошлых домашних заданий. Добавьте к ним логирование ошибок и полезной информации. Также реализуйте возможность запуска из командной строки с 
передачей параметров. Данная промежуточная аттестация оценивается по системе "зачет" / "не зачет" "Зачет" ставится, если Слушатель успешно выполнил задание. "Незачет" ставится, 
если Слушатель не выполнил задание. Критерии оценивания: 1 - Слушатель написал корректный код для задачи, добавил к ним логирование ошибок и полезной информации.
"""


import csv
import logging
import argparse

logger = logging.getLogger(__name__)
my_format = '{levelname:<10} {asctime:<20} {funcName} {msg}'
logging.basicConfig(filename='mylog1.log', filemode='a', encoding='utf-8', level=logging.INFO, style='{', format=my_format)

class Student:
    def __init__(self, name: str, subjects_file: dict):
        self.name = str(name)
        self.subjects = self.load_subjects(subjects_file)   

    def __getattr__(self, name):
        # Позволяет получать значения атрибутов предметов (оценок и результатов тестов) по их именам.
        return self.subjects[name]

    def __setattr__(self, name, value):
        #Дескриптор, который проверяет установку атрибута name. Убеждается, что name начинается с заглавной буквы и состоит только из букв.
        if name == 'name':
            if isinstance(value, str) and value.replace(" ", "").isalpha() and value.istitle():
                object.__setattr__(self, name, value)                 
            else:
                logger.error(msg='ФИО должно состоять только из букв и начинаться с заглавной буквы')
        else:
            object.__setattr__(self, name, value)        

    def __str__(self):
        res = []
        for subj in self.subjects:
            if self.subjects[subj]:
                res.append(subj)
        logger.info(msg=f'Студент: {self.name}\tПредметы: {str(res)[1:-1].replace("'",'')}')
        return f'Студент: {self.name}\nПредметы: {str(res)[1:-1].replace("'",'')}'

    def load_subjects(self, subjects_file) -> dict:
        # Загружает предметы из файла CSV. Использует модуль csv для чтения данных из файла и добавляет предметы в атрибут subjects.
        return_dict = {}
        with open (subjects_file, 'r', newline='') as f:
            csv_file = csv.reader(f, delimiter=',' ,dialect='excel')
            for line in csv_file:
                for subject in line:
                    return_dict[subject] = None
        return return_dict

    def add_grade(self, in_str):
        # Добавляет оценку по заданному предмету. Убеждается, что оценка является целым числом от 2 до 5.
        subject, grade = in_str.split()
        if subject in self.subjects:
            if 2 <= int(grade) <= 5 :
                if not self.subjects[subject]:
                    self.subjects[subject] = {'grade': [], 'test': [] }
                self.subjects[subject]['grade'].append(int(grade))
            else:
                logger.error(msg='Оценка должна быть целым числом от 2 до 5')
        else:
            logger.error(msg=f'Предмет {subject} не найден')

    def add_test_score(self, subject, test_score):
        # Добавляет результат теста по заданному предмету. Убеждается, что результат теста является целым числом от 0 до 100.
        if subject in self.subjects:
            if 0 <= test_score <= 100 :
                if not self.subjects[subject]:
                    self.subjects[subject] = {'grade': [], 'test': [] }
                self.subjects[subject]['test'].append(test_score)
            else:
                logger.error(msg='Результат теста должен быть целым числом от 0 до 100')
        else:
            logger.error(msg=f'Предмет {subject} не найден')

    def get_average_test_score(self, subject): 
        # Возвращает средний балл по тестам для заданного предмета
        if subject in self.subjects:
            logger.info(msg=f'Средний результат по тестам по {subject}: {sum(self.subjects[subject]["test"]) / len(self.subjects[subject]["test"])}')
        else:
            logger.error(msg=f'Предмет {subject} не найден')

    def get_average_grade(self): 
        # Возвращает средний балл по всем предметам.
        res = 0
        cnt = 0
        for subj in self.subjects:
            if self.subjects[subj]:
                res += sum(self.subjects[subj]['grade'])
                cnt += len(self.subjects[subj]['grade'])
        logger.info(msg=f'Средний балл: {(res/cnt if cnt !=0 else 0)}')


if __name__ == '__main__':
    student = Student("Иван Иванов", "0606\\subjects.csv")
    print(student)
    parser = argparse.ArgumentParser(description='Info about student...')
    parser.add_argument('string', metavar='subject', type=str, nargs='*', help='input some string')
    #parser.add_argument('numbers', metavar='N', type=str, nargs='*', help='input some string')
    args = parser.parse_args()
    student.add_grade(*args.string )
    print(student)
    average_grade = student.get_average_grade()
    print(f"Средний балл: {average_grade}")
    # python .\\15_hw.py 'Математика', '4'

'''
    student = Student("Иван Иванов", "subjects.csv")

    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)

    student.add_grade("История", 5)
    student.add_test_score("История", 92)

    average_grade = student.get_average_grade()
    #print(f"Средний балл: {average_grade}")

    average_test_score = student.get_average_test_score("Математика")
    #print(f"c математике: {average_test_score}")

'''