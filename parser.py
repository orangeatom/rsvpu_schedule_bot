#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time

library = {}
schedule_site = 'http://www.rsvpu.ru/raspisanie-zanyatij-ochnoe-otdelenie/'

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
    site = requests.get(schedule_site)
    site.encoding = 'utf-8'
    Soup = BeautifulSoup(site.text, 'html.parser')
    library['groups'] = get_info(Soup,'get_group')
    library['lecturers'] = get_info(Soup,'fprep')
    json.dump(library, open('documents/test.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    json.dump(library, open('documents/links.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

#this function return all schedule
def get_schedule(group,type,long):
    """this function return schedule to one day"""
    list_group = json.load(open('documents/links.json', 'r', encoding='utf-8'))
    if type == 0:
        query_data = {'v_gru': list_group['groups'][group]}
    else:
        query_data = {'v_prep': list_group['lecturers'][group]}

    rq = requests.get(schedule_site,  params = query_data).text


    bs = BeautifulSoup(rq.encode('utf-8'), 'html.parser')

    #print(time.time() - t1)
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
        temp = datetime.datetime.strptime(Mylist_days[day].strip(), "%d.%m.%Y")
        if  datetime.datetime.now().day + 1 == temp.day:
            container += Mylist_days[day] + '\n' + Weekdays[day//2] + '\n'
            for lesson in range(0,7):
                container += Mylist[day][lesson][2] + " " + Mylist[day][lesson][3] + '\n'
            days += 1
    return container

