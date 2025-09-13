from typing import Dict, List, Any, Optional
from aiogram import types
from services.week_type import numerator_or_denominator

import peewee as pw

database = pw.SqliteDatabase('users.db')
class BaseModel(pw.Model):
    class Meta:
        database = database

class User(BaseModel):
    user_id = pw.IntegerField(unique=True)
    faculty_id = pw.CharField()
    group_id = pw.IntegerField()
def init_database():
    database.connect()
    database.create_tables([User])

import re
def parse_lesson_info(lesson_str):

    room_pattern = r'ауд\.\s*(\d+[^,]*)(?:,\s*([\w\s-]*корп\.?))?'
    room_match = re.search(room_pattern, lesson_str)


    if room_match:
        room = room_match.group(1).strip()
        if room_match.group(2):
            room += ", " + room_match.group(2).strip()

        lesson_str = re.sub(room_pattern, '', lesson_str).strip()
    else:
        room = None


    lecturer_pattern = r'([А-ЯЁ][а-яё]*\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.)'
    lecturer_match = re.search(lecturer_pattern, lesson_str)

    if lecturer_match:
        lecturer = lecturer_match.group(1).strip()
        # Удаляем имя преподавателя из исходной строки
        lesson_str = re.sub(lecturer_pattern, '', lesson_str).strip()
    else:
        lecturer = None


    lesson_type_pattern = r'^(ЛЕКЦИЯ|ПРАКТИКА|СЕМИНАР|ЛАБОРАТОРНАЯ)\s+'
    lesson_type_match = re.match(lesson_type_pattern, lesson_str)

    if lesson_type_match:
        lesson_type = lesson_type_match.group(1)
        subject = re.sub(lesson_type_pattern, '', lesson_str).strip()
    else:
        lesson_type = None
        subject = lesson_str.strip()

    return {
        'type': lesson_type,
        'subject': subject,
        'lecturer': lecturer,
        'room': room
    }


def show_day_schedule_to_user(schedule: dict, day: str, week_type: str) -> str:
    day_schedule = schedule.get(day, [])

    # Если пар нет
    if not day_schedule:
        return f"📅 {day} ({week_type})\n\nПар нет! 🎉"

    # Формируем заголовок
    result = f"📅 {day} ({week_type})\n\n"

    # Обрабатываем каждую пару
    for i, lesson_str in enumerate(day_schedule, 1):
        # Очищаем строку от лишних пробелов и переносов
        cleaned_str = re.sub(r'\s+', ' ', lesson_str).strip()


        # Разделяем времмя и предмет
        if ": " in cleaned_str:
            time, subject = cleaned_str.split(": ", 1)
            time = time.strip()
            subject = subject.strip()

            parsed = parse_lesson_info(subject)


            if subject.startswith('-'):
                subject = subject[1:].strip()

            subject = f"{parsed['type']}: {parsed['subject']}\n"
            if parsed['lecturer']:
                subject += f"Преподаватель: {parsed['lecturer']}\n"
            if parsed['room']:
                subject += f"Аудитория: {parsed['room']}"
        else:
            time = "Время не указано"
            subject = cleaned_str.strip()

        # Добавляем номер пары
        result += f"{i}. 🕒 {time} - {subject}\n\n"


    return result

def show_week_schedule_to_user(schedule: dict, week_type: str) -> str:
    result = f"📅 Неделя: ({week_type})\n\n"

    if not dict:
        return f"📅 На эту неделю пар нет или ещё не добавили)🎉\n\n"


    for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]:
        day_schedule = schedule.get(day, [])
        if not day_schedule:
            result += f"📅 {day} ({week_type})Пар нет! 🎉\n\n"
        else:
            result += f"📅 {day}\n\n"

        # Обрабатываем каждую пару
        for i, lesson_str in enumerate(day_schedule, 1):
            # Очищаем строку от лишних пробелов и переносов
            cleaned_str = re.sub(r'\s+', ' ', lesson_str).strip()


            # Разделяем времмя и предмет
            if ": " in cleaned_str:
                time, subject = cleaned_str.split(": ", 1)
                time = time.strip()
                subject = subject.strip()

                parsed = parse_lesson_info(subject)


                if subject.startswith('-'):
                    subject = subject[1:].strip()

                subject = f"{parsed['type']}: {parsed['subject']}\n"
                if parsed['lecturer']:
                    subject += f"Преподаватель: {parsed['lecturer']}\n"
                if parsed['room']:
                    subject += f"Аудитория: {parsed['room']}"
            else:
                time = "Время не указано"
                subject = cleaned_str.strip()


            result += f"{i}. 🕒 {time} - {subject}\n\n"


    return result


def get_user_faculty_id(user_id: int) -> Optional[str]:

    userFaculty = User.select().where(User.user_id == user_id).first().faculty_id
    return userFaculty

def get_user_group(user_id: int) -> Optional[str]:

    userGroup = User.select().where(User.user_id == user_id).first().group_id
    return userGroup


def get_all_faculties() -> Optional[Dict]:
    return {
        "knt": "Факультет информатики",
        "mm": "Факультет математики",
        "ff": "Факультет физики"
    }
def get_groups_by_faculty(faculty_id: str) -> Optional[List[str]]: # может словарь надо, не знаю пока что
    if faculty_id == "knt":
        return ["111", "121", "131", "132", "141", "151", "171", "173", "181","142", "211", "221", "231", "241", "251", "271", "273", "281","311", "321", "331", "341", "351", "361", "381","411", "421", "431", "441", "451", "481","531"]
    elif faculty_id == "mm":
        return ["111", "112", "121", "131", "141", "142", "151", "152","211", "212", "221", "231", "241", "242", "251", "252","311", "312", "321", "331", "341", "342", "351", "352","411", "412", "421", "431", "441", "442", "451","118", "127", "137", "147", "148","218", "227", "237", "247", "248"]
    elif faculty_id == "ff":
        return ["1011", "1021", "1031", "1041", "1051", "1061", "1071", "1081", "1082", "1091", "1101", "1111","2011", "2021", "2031", "2041", "2051", "2061", "2071", "2081", "2082", "2091", "2101", "2111","3011", "3021", "3031", "3032", "3041", "3051", "3071", "3081", "3082", "3091", "3111","4011", "4022", "4031", "4032", "4033", "4041", "4051", "4052", "4061", "4071", "4081", "4082", "4091", "4101", "4111","1211", "1221", "1223", "1224", "1231", "1232", "1233", "1241", "1251", "1252", "1281", "1291", "1301", "1311","2211", "2221", "2222", "2223", "2224", "2231", "2232", "2233", "2241", "2251", "2252", "2281", "2291", "2292", "2311"]
    else:
        return None
def set_user_faculty(user_id: int, faculty_id: str):
    user = User.select().where(User.user_id == user_id).first()
    user.faculty_id = faculty_id
    user.save()
    return


def set_user_group(user_id: int, group_name: str):
    user = User.select().where(User.user_id == user_id).first()
    user.group_id = group_name
    user.save()
    return

def delete_user_data(user_id: int):
    User.delete().where(User.user_id == user_id).execute()
    user = User.select().where(User.user_id == user_id).first()
    if user is None:
        user = User(user_id=user_id, faculty_id='', group_id=0)
        user.save()
    return

def group_exists(faculty_id: str, group_id: str) -> bool:
    all_groups = get_groups_by_faculty(faculty_id)
    return group_id in all_groups

def faculty_exists(faculty_id: str) -> bool:
    all_faculties = get_all_faculties()
    return faculty_id in all_faculties