# from datetime import datetime, timedelta
# import pytz
#
# def getCZ(saratov_date):
#     current_year = saratov_date.year
#     if saratov_date.month >= 9:
#         semester_start = datetime(current_year, 9, 1)
#     else:
#         semester_start = datetime(current_year - 1, 9, 1)
#
#     days_since_monday = semester_start.weekday()
#     first_monday = semester_start - timedelta(days=days_since_monday)
#
#     target_monday = saratov_date - timedelta(days=saratov_date.weekday())
#
#     week_number = (target_monday - first_monday).days // 7
#
#     if week_number % 2 == 0:
#         return "числитель"
#     else:
#         return "знаменатель"
#
# def main():
#     print(getCZ(datetime(2024,12,31)))
#
#
# main()
import requests
from bs4 import BeautifulSoup

a = requests.get("https://sgu.ru/schedule/knt/do/151")
html = a.text
soup = BeautifulSoup(html, 'html.parser')
scheduleHTML = soup.find("tbody")
windows = scheduleHTML.find_all("tr")
# print(windows[0])
schedule = []
for i in windows:
    curTimeFrame = []
    time = i.find(class_="schedule-table__header")
    curTimeFrame.append(time.text)
    currentLessons = i.find_all(class_="schedule-table__col")
    for j in currentLessons:
        if j.text == " ":
            curTimeFrame.append("")
        else:
            informationOfLesson = j.find(class_="lesson-prop__practice")
            if informationOfLesson is None:
                informationOfLesson = j.find(class_="lesson-prop__lecture")
            if informationOfLesson is None:
                informationOfLesson = ""
            else:
                informationOfLesson = informationOfLesson.text
            lessonNameHtml = j.find(class_="schedule-table__lesson-name")
            if lessonNameHtml is None:
                lessonName = ""
            else:
                lessonName = lessonNameHtml.text
            informationOfLesson = informationOfLesson + lessonName
            curTimeFrame.append(informationOfLesson)
    schedule.append(curTimeFrame)

print(schedule)
# text = soup.find_all(class_="schedule-table__lesson-name")