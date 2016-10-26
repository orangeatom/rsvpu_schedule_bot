#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time


schedule_url_full_day = 'http://www.rsvpu.ru/raspisanie-zanyatij-ochnoe-otdelenie/'
schedule_url_half_day = 'http://www.rsvpu.ru/racpisanie-zanyatij-zaochnoe-otdelenie/'
Weekdays = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')

def validate_option(opt):
    text = opt.text.lower()
    if 'вакан' in text or 'выберите' in text:
        return False
    else:
        return True


def get_info(soup,text):
    container = {}
    box = soup.find(id=text)
    for opt in box.find_all('option'):
        if(validate_option(opt)):
            container[opt.text.lower()] = opt['value']
    return container

def update_links():
    dictionary = {}
    site = requests.get(schedule_url_full_day)
    site.encoding = 'utf-8'
    Soup = BeautifulSoup(site.text, 'html.parser')
    dictionary['groups'] = get_info(Soup,'get_group')
    dictionary['lecturers'] = get_info(Soup,'fprep')
    json.dump(dictionary, open('documents/links.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


#this function return all schedule
def get_schedule(group,type):
    """this function return schedule to one day"""
    list_group = json.load(open('documents/links.json', 'r', encoding='utf-8'))
    if type == 0:
        query_data = {'v_gru': group}
        html_schedule = requests.get(schedule_url_full_day, params=query_data).text
    else:
        query_data = {'v_prep': group}
        html_schedule = requests.get(schedule_url_half_day, params=query_data).text

    bs = BeautifulSoup(html_schedule.encode('utf-8'), 'html.parser')

    sbj = []
    study_day = []

    for subjects in bs.find_all(class_='disciplina'):
        date = []
        for tag in subjects.find_all(class_='disciplina_cont'):
            date.append((tag.get_text()).split('\n'))
        sbj.append(date)

    for days in bs.find_all(class_ = 'day_date'):
        date = days.get_text().split('\n')
        study_day.append(date[1])
        study_day.append(date[2])

    container = {}
    for day in range(0,14):
        list = str(datetime.datetime.strptime(study_day[day].strip(),'%d.%m.%Y'))
        container[list] = []
        for lesson in range(0,7):
            container[list].append((sbj[day][lesson][2],sbj[day][lesson][3]))
    return container

def get_schedule_today(group, type):
    schedule = get_schedule(group,type)
    result = []
    for t in schedule.keys():
        if datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S').day == datetime.date.today().day:
            result.append(schedule[t])
            break

    return result

def get_schedule_tomorrow(group, type):
    schedule = get_schedule(group, type)
    result = []
    for t in schedule.keys():
        if datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S').day == datetime.date.today().day + 1:
            result.append(schedule[t])
            break
    return result

def get_schedule_week(group, type):
    schedule = get_schedule(group, type)
    result = []
    for i in range(0,7):
        diff = datetime.date.today() + datetime.timedelta(days=i)
        for t in schedule.keys():
            if datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S').day == diff.day:
                result.append(schedule[t])
    return result


