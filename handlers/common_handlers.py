import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from services.database import (get_user_group,
                               get_user_faculty_id, show_day_schedule_to_user,
                               show_week_schedule_to_user)
from services.week_type import determine_week_type
from datetime import timedelta
from parser.parse import parseSSU
import pytz

router = Router()

@router.message(F.text.in_(["📅 Завтра","📅 Сегодня"]))
async def handler_day(message: types.Message):
    try:
        daysplus = 0
        if message.text=="📅 Сегодня":
            daysplus = 1
        elif message.text=="📅 Завтра":
            daysplus = 2
        user_faculty = get_user_faculty_id(message.from_user.id)
        user_group = get_user_group(message.from_user.id)
        if (not user_group):
            await message.answer("Сначала нужно зарегистрироваться. Напиши /start")
            return

        utc_time = message.date

        if utc_time.tzinfo is not None:
            utc_time = utc_time.astimezone(pytz.utc)
        else:
            utc_time = pytz.utc.localize(utc_time)

        saratov_zone = pytz.timezone('Europe/Saratov')
        saratov_time = utc_time.astimezone(saratov_zone)
        saratov_date = saratov_time.date() + timedelta(days=daysplus)
        week_type = determine_week_type(saratov_date)

        schedule = parseSSU()

        day_name = get_name_of_day(saratov_date.weekday())

        await message.answer(show_day_schedule_to_user(schedule, day_name, week_type))

    except Exception as e:
        logging.error(f"Error in handler_today: {e}")
        await message.answer(f"Произошла ошибка при получении расписания. Попробуйте позже {e}")



@router.message(F.text == "📅 Неделя")
async def handler_week(message: types.Message):
    try:
        user_faculty = get_user_faculty_id(message.from_user.id)
        user_group = get_user_group(message.from_user.id)
        if (not user_group):
            await message.answer("Сначала нужно зарегистрироваться. Напиши /start")
            return

        utc_time = message.date

        if utc_time.tzinfo is not None:
            utc_time = utc_time.astimezone(pytz.utc)
        else:
            utc_time = pytz.utc.localize(utc_time)

        saratov_zone = pytz.timezone('Europe/Saratov')
        saratov_time = utc_time.astimezone(saratov_zone)
        saratov_date = saratov_time.date() + timedelta(days=1)
        week_type = determine_week_type(saratov_date)

        schedule = get_group_schedule(user_faculty, user_group, week_type)

        await message.answer(show_week_schedule_to_user(schedule, week_type))

    except Exception as e:
        logging.error(f"Errom in handler_week: {e}")
        await message.answer("Произошла ошибка при получении расписания. Попробуйте позже")

@router.message(F.text == "❓ Помощь")
async def handle_help(message: types.Message):
    help_text = """
        🤖 <b>Помощь по боту:</b>
        
        📅 <b>Сегодня</b> - показать расписание на сегодня
        📅 <b>Завтра</b> - показать расписание на завтра
        📋 <b>Неделя</b> - показать расписание на всю неделю
        
        🔄 <b>Сменить группу</b> - начать регистрацию заново
        
        📊 Бот показывает актуальное расписание твоей группы.
    """
    await message.answer(help_text, parse_mode="HTML")

@router.message(F.text == "📋 Меню")
async def handle_menu(message: types.Message):

    user_group = get_user_group(message.from_user.id)

    if not user_group:
        await message.answer("Сначала нужно зарегистрироваться. Напиши /start")
        return

    from services.keyboards import get_main_keyboard
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🔄 Сменить группу")
async def handle_change_group(message: types.Message, state: FSMContext):
    """
        Обработчик кнопки смены группы.
        Начинает процесс регистрации заново.
    """
    try:
        await state.clear()

        from services.database import delete_user_data
        delete_user_data(message.from_user.id)


        from handlers.start import Registration
        from services.keyboards import get_faculties_keyboard

        await message.answer(
            "Давай выберем новую группу. Сначала выбери факультет:",
            reply_markup=get_faculties_keyboard()
        )


        await state.set_state(Registration.choosing_faculty)

    except Exception as e:
        logging.error(f"Error in handle_change_group: {e}")
        await message.answer("Произошла ошибка при смене группы. Попробуйте позже.")


def get_name_of_day(day_number: int) -> str:
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return  days[day_number - 1]

