import requests
from bs4 import BeautifulSoup
from services.week_type import *

def parseSSU(faculty_id, group_id, message: types.Message):
    a = requests.get(f"https://sgu.ru/schedule/{faculty_id}/do/{group_id}")
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
                num = j.find(class_="lesson-prop__num")
                denom = j.find(class_="lesson-prop__denom")
                currentNum = ""
                if informationOfLesson is None:
                    informationOfLesson = j.find(class_="lesson-prop__lecture")
                if informationOfLesson is None:
                    informationOfLesson = ""
                else:
                    informationOfLesson = informationOfLesson.text
                if num is None and denom is None:
                    currentNum = ""
                elif num is None:
                    currentNum = "Числитель"
                elif denom is None:
                    currentNum = "Знаменатель"
                lessonNameHtml = j.find(class_="schedule-table__lesson-name")
                if lessonNameHtml is None:
                    lessonName = ""
                else:
                    lessonName = lessonNameHtml.text
                if currentNum == numerator_or_denominator(message) or currentNum=="":
                    informationOfLesson = informationOfLesson + lessonName
                else:
                    informationOfLesson = ""
                curTimeFrame.append(informationOfLesson)
        schedule.append(curTimeFrame)
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

    result = {day: [] for day in days_of_week}

    for row in schedule:
        time_slot = row.pop(0)

        for i, subject in enumerate(row):
            if subject.strip():
                result[days_of_week[i]].append(f"{time_slot}: {subject}")

    return result