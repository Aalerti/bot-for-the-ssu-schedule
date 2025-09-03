from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from services.database import get_all_faculties, get_groups_by_faculty

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
