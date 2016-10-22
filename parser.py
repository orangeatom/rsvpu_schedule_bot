#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import datetime

library = {}
groups = {}
lecturers = {}
schedule_site = 'http://www.rsvpu.ru/raspisanie-zanyatij-ochnoe-otdelenie/'

def update_schedule_group():
    site = requests.get(schedule_site)
    site.encoding = 'utf-8'
    Soup = BeautifulSoup(site.text, 'html.parser')
    box = Soup.find(id='get_group')
    for opt in box.find_all('option'):
        groups[opt.text.lower()] = opt['value']


def update_schedule_lecturer():
    site = requests.get(schedule_site)
    site.encoding = 'utf-8'
    Soup = BeautifulSoup(site.text,'html.parser')
    box = Soup.find(id='fprep')
    for opt in box.find_all('option'):
        lecturers[opt.text.lower()] = opt['value']


def update_links():
    update_schedule_group()
    update_schedule_lecturer()
    library['groups'] = groups
    library['lecturers'] = lecturers
    json.dump(library, open('documents/links.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

#this function return all schedule
def get_schedule(group,type):
    #not change
    listgroup = json.load(open('documents/links.json', 'r', encoding='utf-8'))
    if (type == 0):
        site = requests.get(schedule_site + '?v_gru=' + listgroup['groups'][group])
    else: site = requests.get(schedule_site + '?v_prep=' + listgroup['lecturers'][group])
    site.encoding = 'utf-8'
    bs = BeautifulSoup(site.text, 'html.parser')
    #not change
    Mylist = []
    Mylist_days = []
    Weekdays = ('Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье')

    for link in bs.find_all(class_='disciplina'):
        temp = []
        for tag in link.find_all(class_='disciplina_cont'):
            temp.append((tag.get_text()).split('\n'))
        Mylist.append(temp)

    for days in bs.find_all(class_ = 'day_date'):
        temp = days.get_text().split('\n')
        Mylist_days.append(temp[1])
        Mylist_days.append(temp[2])
    container = ""

    for day in range(0,14):
        lesson = 0
        #print(Mylist_days[day] + '\n' + Weekdays[day//2])
        temp = datetime.datetime.strptime(Mylist_days[day].strip(), "%d.%m.%Y")
        if  datetime.datetime.now().day + 2 == temp.day:
            container += Mylist_days[day] + '\n' + Weekdays[day//2] + '\n'
            #print(temp)
            for lesson in range(0,7):
                #print(Mylist[day][lesson][2] + " " + Mylist[day][lesson][3])
                container += Mylist[day][lesson][2] + " " + Mylist[day][lesson][3] + '\n'
                lesson += 1

        day += 1
    #print(container)
    return container

