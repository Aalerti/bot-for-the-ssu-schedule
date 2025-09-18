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
        "knt": "Факультет компьютерных наук и информационных технологий",
        "mm": "Механико-математический факультет",
        "ifg": "Институт филологии и журналистики",
        "bf": "Биологический факультет",
        "gf": "Географический факультет",
        "gl": "Геологический факультет",
        "ih": "Институт химии",
        "ff": "Институт физики",
        "imo": "Институт истории и международных отношений",
        "sf": "Социологический факультет",
        "gdrin": "Факультет гуманитарных дисциплин, русского и иностранных языков (ПИ)",
        "ef": "Экономический факультет",
        "law": "Юридический факультет",
        "fps": "Факультет психологии",
        "fmend": "Факультет физико-математических и естественно-научных дисциплин (ПИ)",
        "fp": "Философский факультет",
        "fmimt": "Факультет фундаментальной медицины и медицинских технологий",
        "piii": "Факультет искусств (ПИ)",
        "uf": "Юридический факультет",
        "fppso": "Факультет психолого-педагогического и специального образования (ПИ)",
        "piifk": "Факультет физической культуры и спорта"
    }
def get_groups_by_faculty(faculty_id: str) -> Optional[List[str]]: # может словарь надо, не знаю пока что
    if faculty_id == "knt":
        return ["111", "121", "131", "132", "141", "151", "171", "173", "181","142", "211", "221", "231", "241", "251", "271", "273", "281","311", "321", "331", "341", "351", "361", "381","411", "421", "431", "441", "451", "481","531"]
    elif faculty_id == "mm":
        return ["111", "112", "121", "131", "141", "142", "151", "152","211", "212", "221", "231", "241", "242", "251", "252","311", "312", "321", "331", "341", "342", "351", "352","411", "412", "421", "431", "441", "442", "451","118", "127", "137", "147", "148","218", "227", "237", "247", "248"]
    elif faculty_id == "ff":
        return ["1011", "1021", "1031", "1041", "1051", "1061", "1071", "1081", "1082", "1091", "1101", "1111","2011", "2021", "2031", "2041", "2051", "2061", "2071", "2081", "2082", "2091", "2101", "2111","3011", "3021", "3031", "3032", "3041", "3051", "3071", "3081", "3082", "3091", "3111","4011", "4022", "4031", "4032", "4033", "4041", "4051", "4052", "4061", "4071", "4081", "4082", "4091", "4101", "4111","1211", "1221", "1223", "1224", "1231", "1232", "1233", "1241", "1251", "1252", "1281", "1291", "1301", "1311","2211", "2221", "2222", "2223", "2224", "2231", "2232", "2233", "2241", "2251", "2252", "2281", "2291", "2292", "2311"]
    elif faculty_id == "bf":
        return ["121", "122", "123", "124", "221", "222", "223", "224", "321", "322", "323", "324", "421", "422", "423", "424", "141", "142", "143", "151", "241", "242", "243", "251", "161", "261", "361"]
    elif faculty_id == "gf":
        return ["111", "121", "122", "131", "141", "211", "221", "222", "231", "241",  "311", "321", "322", "331", "341","411", "421", "422", "423", "431", "441","115", "125", "145", "146","215", "225", "245", "246"]
    elif faculty_id == "gl":
        return ["151", "251", "351", "352", "451", "452", "551", "552", "103", "131", "203", "231", "303", "403"]
    elif faculty_id == "imo":
        return ["111", "112", "121", "131", "141", "211", "212", "221", "231", "241", "311", "312", "321", "331", "341", "411", "412", "421", "431", "441", "161", "162", "163", "166", "261", "262", "263", "266", "267", "268"]
    elif faculty_id == "ifg":
        return ["111", "112", "113", "121", "122", "123", "124", "131", "132", "133", "141", "142", "211", "212", "213", "221", "222", "223", "231", "232", "233", "241", "242", "311", "312", "313", "321", "322", "323", "331", "332", "341", "342", "411", "412", "421", "422", "423", "431", "432", "441", "442", "161", "162", "163", "164", "261", "262", "263", "264", "361", "362", "363", "364", "151", "152", "153", "154", "155", "156", "157", "251", "252", "253", "254", "255", "256", "257"]
    elif faculty_id == "ih":
        return ["111", "112", "131", "141", "211", "212", "231", "232", "241", "311", "312", "313", "331", "341", "411", "412", "413", "431", "441", "151", "152", "251", "252"]
    elif faculty_id == "sf":
        return ["111", "121", "141", "151", "171", "211", "221", "241", "242", "251", "252", "271", "311", "321", "341", "342", "351", "352", "371", "411", "421", "441", "451", "471", "162", "163", "165", "264", "265"]
    elif faculty_id == "gdrin":
        return [
    "111", "112", "113", "114", "121", "131", "141", "142", "143", "151", "152", "161",
    "211", "212", "213", "214", "221", "231", "241", "242", "243", "251", "252", "261",
    "311", "312", "313", "314", "321", "331", "341", "342", "343", "351", "361",
    "411", "412", "413", "421", "431", "441", "442", "443", "451", "461",
    "171", "181", "191",
    "271", "281", "291"
]
    elif faculty_id == "piii":
        return ["101", "102", "103", "104", "109", "201", "202", "203", "204", "301", "302", "304", "401", "402", "403", "121", "221"]
    elif faculty_id == "fps":
        return [
    "161", "162",
    "261", "262",
    "361", "362",
    "461", "462",
    "151", "152", "163", "164", "165", "166", "167", "168", "169", "171",
    "251", "263", "264", "265", "266", "267", "268", "269", "271"
]
    elif faculty_id == "fppso":
        return [
    "101", "111", "112", "121", "131", "141", "151", "161", "171",
    "201", "211", "212", "221", "231", "241", "251", "261", "271",
    "301", "303", "311", "312", "321", "331", "341", "351", "371", "391",
    "401", "411", "412", "421", "431", "441", "451", "471", "491",
    "102", "114", "123", "132", "133", "144", "145", "172", "192",
    "202", "214", "223", "232", "233", "244", "245", "272", "292"
]
    elif faculty_id == "fmend":
        return [
    "111", "121", "131", "141", "151", "161",
    "211", "221", "231", "241", "251",
    "311", "312", "321", "331", "332", "341", "351", "352",
    "411", "412", "421", "431", "441", "451", "452",
    "120", "135", "140", "150",
    "220", "235", "240", "250"
]
    elif faculty_id == "piifk":
        return [
    "101", "102", "103", "108",
    "201", "202", "203", "208",
    "301", "302", "303",
    "401", "402", "408",
    "106", "107",
    "206"
]
    elif faculty_id == "fmimt":
        return [
    "111", "121", "131",
    "211", "221", "231",
    "311", "321", "331",
    "411", "421", "431",
    "511", "521", "531"
]
    elif faculty_id == "fp":
        return ["111", "141", "151", "211", "241", "251", "311", "331", "341", "351", "411", "431", "441", "451", "171", "172", "181", "191", "271", "272", "281", "291", "371", "372", "381", "391", "112", "113", "142", "152", "212", "213", "232", "242", "252", "262"]
    elif faculty_id == "ef":
        return [
    "111", "112", "121", "122", "141",
    "211", "212", "213", "221", "222", "241",
    "311", "312", "313", "321", "322", "341",
    "411", "412", "413", "421", "422", "441",
    "101",
    "201",
    "301",
    "151", "171",
    "251", "261"
]
    elif faculty_id == "uf":
        return [
    "141", "151", "191",
    "241", "251", "291", "292",
    "341", "351", "391",
    "441", "451", "491", "492",
    "541", "551", "591",
    "161", "162", "163", "164", "165",
    "261", "262", "263", "264", "265",
    "111", "112", "121", "131", "132",
    "211", "212", "221", "231", "232",
    "311", "312", "321", "331", "332",
    "411", "412", "421", "431", "432",
    "181",
    "281", "282",
    "381"
]
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