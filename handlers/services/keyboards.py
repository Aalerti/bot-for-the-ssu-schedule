from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from services.database import get_all_faculties, get_groups_by_faculty

"""
Inline keyboards
"""
class FacultyCallback(CallbackData, prefix="faculty"):
    faculty_id: int

class GroupCallback(CallbackData, prefix="group"):
    group_name: str

def get_faculties_keyboard() -> InlineKeyboardMarkup:
    faculties = get_all_faculties()

    buttons = []
    for faculty_id, faculty_name in faculties.items():
        button = InlineKeyboardButton(
            text=faculty_name,
            callback_data=FacultyCallback(faculty_id=faculty_id).pack()
        )
        buttons.append([button])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_groups_keyboard(faculty_id: int) -> InlineKeyboardMarkup:
    # groups: List[str]
    groups = get_groups_by_faculty(faculty_id=faculty_id)
    if not groups:
        return InlineKeyboardMarkup(inline_keyboard=[])

    buttons = []
    for group_name in groups:
        button = InlineKeyboardButton(
            text=group_name,
            callback_data=GroupCallback(group_name=group_name).pack()
        )
        buttons.append([button])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

"""
Reply keyboards
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
        Создает основную клавиатуру с кнопками расписания.
        ReplyKeyboardMarkup - это статичная клавиатура, которая появляется снизу экрана.
    """
    today_btn = KeyboardButton(text="📅 Сегодня")
    tomorrow_btn = KeyboardButton(text="📆 Завтра")
    week_btn = KeyboardButton(text="📋 Неделя")
    help_btn = KeyboardButton(text="❓ Помощь")
    menu_btn = KeyboardButton(text="📋 Меню",)
    change_group_btn = KeyboardButton(text="🔄 Сменить группу")

    return ReplyKeyboardMarkup(
        keyboard=[
            [today_btn,tomorrow_btn],
            [week_btn],
            [help_btn, menu_btn, change_group_btn]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
