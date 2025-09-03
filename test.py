from datetime import datetime, timedelta
import pytz

def getCZ(saratov_date):
    current_year = saratov_date.year
    if saratov_date.month >= 9:
        semester_start = datetime(current_year, 9, 1)
    else:
        semester_start = datetime(current_year - 1, 9, 1)

    days_since_monday = semester_start.weekday()
    first_monday = semester_start - timedelta(days=days_since_monday)

    target_monday = saratov_date - timedelta(days=saratov_date.weekday())

    week_number = (target_monday - first_monday).days // 7

    if week_number % 2 == 0:
        return "числитель"
    else:
        return "знаменатель"

def main():
    print(getCZ(datetime(2024,12,31)))


main()