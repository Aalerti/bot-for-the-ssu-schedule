from aiogram import types
from datetime import datetime, timedelta, date
import pytz

#
def numerator_or_denominator(message: types.Message) -> str:
    utc_time = message.date

    if utc_time.tzinfo is not None:
        utc_time = utc_time.astimezone(pytz.utc)
    else:
        utc_time = pytz.utc.localize(utc_time)

    saratov_zone = pytz.timezone('Europe/Saratov')
    saratov_time = utc_time.astimezone(saratov_zone)
    saratov_date = saratov_time.date()

    week_type = determine_week_type(saratov_date)
    return week_type

def determine_week_type(saratov_date) -> str:
    if isinstance(saratov_date, datetime):
        saratov_date = saratov_date.date()

    current_year = saratov_date.year
    if saratov_date.month >= 9:

        semester_start = date(current_year, 9, 1)
    else:
        semester_start = date(current_year - 1, 9, 1)

    days_since_monday = semester_start.weekday()
    first_monday = semester_start - timedelta(days=days_since_monday)

    target_monday = saratov_date - timedelta(days=saratov_date.weekday())

    week_number = (target_monday - first_monday).days // 7

    if week_number % 2 == 0:
        return "Числитель"
    else:
        return "Знаменатель"