import requests
from bs4 import BeautifulSoup
from services.week_type import *

def parseSSU(faculty_id, group_id, message: types.Message):
    a = requests.get(f"https://sgu.ru/schedule/{faculty_id}/do/{group_id}")
    html = a.text
    soup = BeautifulSoup(html, 'html.parser')
    scheduleHTML = soup.find("tbody")
    weekType = numerator_or_denominator(message)
    windows = scheduleHTML.find_all("tr")
    schedule = []
    for i in windows:
        lessons = i.find_all(class_="schedule-table__col")
        num = 0
        curTimeFrame = []
        for j in lessons:
            lessonsInDayCurrentTimeFrame = j.find_all(class_="schedule-table__lesson")
            if len(lessonsInDayCurrentTimeFrame) ==0:
                curTimeFrame.append("")
                continue
            elif len(lessonsInDayCurrentTimeFrame) ==1:
                currentNum = ""
                lesson = lessonsInDayCurrentTimeFrame[0]
                try:
                    currentNum = lesson.find(class_="lesson-prop__num").text
                except:
                    pass
                try:
                    if "Ч" not in currentNum:
                        currentNum = lesson.find(class_="lesson-prop__denom").text
                except:
                    pass
                if weekType in currentNum or currentNum=="":
                    lectOrPract = lesson.find(class_="lesson-prop__practice")
                    if lectOrPract is None:
                        lectOrPract = j.find(class_="lesson-prop__lecture")
                    if lectOrPract is None:
                        lectOrPract = ""
                    else:
                        lectOrPract = lectOrPract.text
                    lessonNameHtml = lesson.find(class_="schedule-table__lesson-name")
                    lessonName = lessonNameHtml.text
                    teacherNameHtml = lesson.find(class_="schedule-table__lesson-teacher")
                    roomNameHtml = lesson.find(class_="schedule-table__lesson-room")
                    teacherName = " " + teacherNameHtml.text
                    roomName = " " + roomNameHtml.text
                    lessonInfo = lectOrPract + lessonName + teacherName + roomName
                    curTimeFrame.append(lessonInfo)
                else:
                    curTimeFrame.append("")
            elif len(lessonsInDayCurrentTimeFrame)>1:
                for lesson in lessonsInDayCurrentTimeFrame:
                    currentNum = ""
                    try:
                        currentNum = lesson.find(class_="lesson-prop__num").text
                    except:
                        pass
                    try:
                        if "Ч" not in currentNum:
                            currentNum = lesson.find(class_="lesson-prop__denom").text
                    except:
                        pass
                    if weekType in currentNum or currentNum=="":
                        lectOrPract = lesson.find(class_="lesson-prop__practice")
                        if lectOrPract is None:
                            lectOrPract = j.find(class_="lesson-prop__lecture")
                        if lectOrPract is None:
                            lectOrPract = ""
                        else:
                            lectOrPract = lectOrPract.text
                        lessonNameHtml = lesson.find(class_="schedule-table__lesson-name")
                        lessonName = lessonNameHtml.text
                        teacherNameHtml = lesson.find(class_="schedule-table__lesson-teacher")
                        roomNameHtml = lesson.find(class_="schedule-table__lesson-room")
                        teacherName = " " + teacherNameHtml.text
                        roomName = " " + roomNameHtml.text
                        lessonInfo = lectOrPract + lessonName + teacherName + roomName
                        curTimeFrame.append(lessonInfo)
                        break
                    else:
                        if lesson == lessonsInDayCurrentTimeFrame[-1]:
                            curTimeFrame.append("")
                        continue
            num+=1
        schedule.append(curTimeFrame)
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

    week_schedule = {day: [] for day in days_of_week}

    for i, daily_activities in enumerate(schedule):
        for j, activity in enumerate(daily_activities):
            week_schedule[days_of_week[j % len(days_of_week)]].append(activity)

    result = week_schedule

    return result

