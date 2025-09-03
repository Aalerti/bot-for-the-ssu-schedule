from typing import Dict, List, Any, Optional
from aiogram import types
from services.week_type import numerator_or_denominator

def get_group_schedule(faculty_id: str, group_id: str, week_type: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Эта функция будет заменена на реальный парсер.
    Пока что я составил свое расписание мечты :).
    """
    # week_type - это "числитель" или "знаменатель"
    return {
        "monday": [
            {"time": "9:00", "subject": "Математика", "teacher": "Иванов И.И.", "room": "101"},
            {"time": "10:50", "subject": "Физика", "teacher": "Петров П.П.", "room": "202"}
        ],
        "tuesday": [
            {"time": "9:00", "subject": "Программирование", "teacher": "Сидоров С.С.", "room": "Лаб. 505"}
        ],
    }

def show_today_schedule_to_user(schedule: Dict[str, List[Dict[str, str]]]) -> str:
    """
    Заглушка.
    Позже будет возвращать оформленное расписание на сегодня.
    """
    answer: str = ""

def show_tomorrow_schedule_to_user(schedule: Dict[str, List[Dict[str, str]]]) -> str:
    """
    Заглушка.
    Позже будет возвращать оформленное расписание на завтра.
    """
    answer: str = ""

def show_week_schedule_to_user(schedule: Dict[str, List[Dict[str, str]]]) -> str:
    """
    Заглушка.
    Позже будет возвращать оформленное расписание на всю неделю.
    """
    answer: str = ""

"""
Функции для обращения к базе данных, возвращают все три нужных параметра для парсера 
"""
def get_week_type(message: types.Message) -> str:
    numerator_or_denominator(message)

def get_user_data(user_id: int) -> Optional[Dict]:
    """
    Заглушка.
    Получить данные пользователя из БД
    """

def get_user_faculty_id(user_id: int) -> Optional[int]:
    """
    Заглушка.
    Позже будет возвращать факультет пользователя из БД.
    """
    return 12 # 12 условно айди КНИИТА

def get_user_group(user_id: int) -> Optional[str]:
    """
    Заглушка.
    Позже будет возвращать группу пользователя из БД.
    """
    return "151" # условно 5 айди програмнной инженерии

def get_all_faculties() -> Optional[Dict]:
    """
    Заглушка.
    Получить все факультеты
    """
def get_groups_by_faculty(faculty_id: int) -> Optional[List[str]]: # может словарь надо, не знаю пока что
    """
    Заглушка.
    Получить группы по факультету
    """

def set_user_faculty(user_id: int, faculty_id: int):
    """
    Заглушка.
    Сохранить факультет пользователя
    """

def set_user_group(user_id: int, group_name: str):
    """
    Заглушка.
    Сохранить группу пользователя
    """

def save_user_in_database(user_id: int, faculty_id: int, group_id: str):
    """
    Заглушка.
    Сохранить пользователя в бд
    """

def group_exists(faculty_id: int, group_id: str) -> bool:
    """
    Заглушка.
    Функция для проверки существования группы в бд
    """

def faculty_exists(faculty_id: int) -> bool:
    """
    Заглушка.
    Функция для проверки существования факультета в бд
    """