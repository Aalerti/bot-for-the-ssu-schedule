import logging

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from services.keyboards import get_faculties_keyboard, FacultyCallback, GroupCallback
from services.database import *

router = Router()

class Registration(StatesGroup):
    choosing_faculty = State()
    choosing_group = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        user = User.select().where(User.user_id == message.from_user.id).first()
        if user is None:
            user = User(user_id=message.from_user.id, faculty_id='', group_id=0)
            user.save()
        user_group = get_user_group(message.from_user.id)
        if user_group !=0:
            from services.keyboards import get_main_keyboard
            await message.answer(
                f"Привет! Твоя группа: {user_group}. Выбери действие:",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                "Привет! Я показываю расписания для всего СГУ им. Чернышевского. Для начала выбери свой факультет:",
                reply_markup=get_faculties_keyboard()  # Добавляем инлайн-клавиатуру
            )
            await state.set_state(Registration.choosing_faculty)

    except Exception as e:
        logging.error(f"Unexpected error in cmd_start: {e}")
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")



@router.callback_query(Registration.choosing_faculty, FacultyCallback.filter())
async def process_faculty_selection(callback: types.CallbackQuery, callback_data: FacultyCallback, state: FSMContext):
    try:

        from services.database import faculty_exists
        if not faculty_exists(callback_data.faculty_id):
            await callback.answer("Ошибка: выбранный факультет не найден")
            return

        await state.update_data(faculty_id=callback_data.faculty_id)

        from services.keyboards import get_groups_keyboard
        groups_keyboard = get_groups_keyboard(callback_data.faculty_id)

        if not groups_keyboard.inline_keyboard:
            await callback.answer("Для этого факультета нет групп")
            return

        await callback.message.edit_text(
            "Теперь выбери свою группу:",
            reply_markup=groups_keyboard
        )

        await state.set_state(Registration.choosing_group)
        await callback.answer(text="Факультет выбран", show_alert=True)

    except Exception as e:
        logging.error(f"Unexpected error in process_faculty_selection: {e}")
        await callback.answer("Произошла непредвиденная ошибка. Попробуйте позже.")


@router.callback_query(Registration.choosing_group, GroupCallback.filter())
async def process_group_selection(
        callback: types.CallbackQuery,
        callback_data: GroupCallback,
        state: FSMContext
):
    try:

        data = await state.get_data()
        faculty_id = data.get('faculty_id')

        if not faculty_id:
            await callback.answer("Ошибка: не выбран факультет. Начните регистрацию заново /start")
            await state.clear()
            return

        from services.database import get_groups_by_faculty, group_exists
        faculty_groups = get_groups_by_faculty(faculty_id)

        if faculty_groups is None:
            await callback.answer("Ошибка конфигурации: для этого факультета нет групп")
            await state.clear()
            return

        if not group_exists(faculty_id, callback_data.group_name):
            await callback.answer("Ошибка: выбранная группа не принадлежит факультету")
            await state.clear()
            return

        from services.database import set_user_faculty, set_user_group
        try:
            set_user_faculty(callback.from_user.id, faculty_id)
            set_user_group(callback.from_user.id, callback_data.group_name)
        except Exception as e:

            logging.error(f"Database error for user {callback.from_user.id}: {e}")
            await callback.answer("Ошибка сохранения данных. Попробуйте позже.")
            return

        await state.clear()

        await callback.message.edit_text(
            f"Отлично! Ты зарегистрирован в группе {callback_data.group_name}. Теперь ты можешь использовать бота."
            ,reply_markup=None
        )
        from services.keyboards import get_main_keyboard
        await callback.message.answer(
            "Выбери действие:",
            reply_markup=get_main_keyboard()
        )

        await callback.answer()

    except Exception as e:
        logging.error(f"Unexpected error in process_group_selection: {e}")
        await callback.answer("Произошла непредвиденная ошибка. Попробуйте позже.")