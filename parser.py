#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time


schedule_url = 'http://www.rsvpu.ru/raspisanie-zanyatij-ochnoe-otdelenie/'
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
    site = requests.get(schedule_url)
    site.encoding = 'utf-8'
    Soup = BeautifulSoup(site.text, 'html.parser')
    dictionary['groups'] = get_info(Soup,'get_group')
    dictionary['lecturers'] = get_info(Soup,'fprep')
    json.dump(dictionary, open('documents/links.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

#this function return all schedule

#this function return all schedule
def get_schedule(group,type):
    """this function return schedule to one day"""
    list_group = json.load(open('links.json', 'r', encoding='utf-8'))
    if type == 0:
        query_data = {'v_gru': list_group['groups'][group]}
    else:
        query_data = {'v_prep': list_group['lecturers'][group]}
    html_schedule = requests.get(schedule_url, params = query_data).text
    bs = BeautifulSoup(html_schedule.encode('utf-8'), 'html.parser')

    subjects = []
    study_day = []

    for link in bs.find_all(class_='disciplina'):
        temp = []
        for tag in link.find_all(class_='disciplina_cont'):
            temp.append((tag.get_text()).split('\n'))
        subjects.append(temp)

    for days in bs.find_all(class_ = 'day_date'):
        temp = days.get_text().split('\n')
        study_day.append(temp[1])
        study_day.append(temp[2])

    container = {}
    for day in range(0,14):
        #temp = datetime.datetime.strptime(study_day[day].strip(), "%d.%m.%Y")
        list = str(datetime.datetime.strptime(study_day[day].strip(),'%d.%m.%Y'))
        container[list] = []
        #container += study_day[day] + '\n' + Weekdays[day//2] + '\n'
        for lesson in range(0,7):
            container[list].append((subjects[day][lesson][2],subjects[day][lesson][3]))
            #container +=  + " " + subjects[day][lesson][3] + '\n'
    return container
def get_schedule_day(group,type):
    schedule = get_schedule(group,type)
    for t in schedule.keys():
        if datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S').day == datetime.date.today().day:
            print(schedule[t])


def get_schedule_tomorrow(group,type):
    schedule = get_schedule(group, type)
    for t in schedule.keys():
        if datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S').day == datetime.date.today().day +1 :
            print(schedule[t])

def get_schedule_week(group,type):
    schedule = get_schedule(group, type)
    for i in range(0,6):
        for t in schedule.keys():
            if datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S').day == datetime.date.today().day + i:
                print(schedule[t])

