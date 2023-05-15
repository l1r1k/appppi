import pathlib
import json
import os
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask
from flask_restful import Api, Resource, reqparse

class items:
    def __init__(self, id, dicts):
        self.id = id
        self.dicts = dicts     

def click():
    URL = "https://mpt.ru/studentu/raspisanie-zanyatiy/"
    URL_CHANGE_SCHEDULE = "https://mpt.ru/studentu/izmeneniya-v-raspisanii/"

    allSpecials = []
    groups = []
    ruquest_schedule = requests.get(URL)
    request_change_schedule = requests.get(URL_CHANGE_SCHEDULE)
    print(f'{ruquest_schedule.status_code} OK')
    print(request_change_schedule.status_code)
    soup = bs(ruquest_schedule.text, "html.parser")
    soup_change_schedule = bs(request_change_schedule.text, "html.parser")

    current_week_from_html = soup.find('h3').text.replace('Неделя: ','')

    test = soup.find('ul', class_='nav nav-tabs')

    for data in test:
        data.find('li')
        allSpecials.append(data.text)

    allSpecials.sort()
    del allSpecials[0:7]

    allGroups = dict.fromkeys(allSpecials, [])

    test = test.find_next('ul', class_='nav nav-tabs')

    index01 = 0

    for group in test:
        group.find('li')
        temp = group.text
        temp = temp.replace('\n','')
        link = group.find_next('a')
        temp += ' ' + link.get('href').replace('#', '')
        groups.append(temp)
        if temp == '' or temp.startswith(' '):
            index01 += 1

    groups.sort()

    del groups[0:index01]

    allGroups['09.02.01'] = groups

    groups06 = []

    test = test.find_next('ul', class_='nav nav-tabs')

    index06 = 0

    for group06 in test:
        group06.find('li')
        temp06 = group06.text
        temp06 = temp06.replace('\n','')
        link06 = group06.find_next('a')
        temp06 += ' ' + link06.get('href').replace('#', '')
        groups06.append(temp06)
        if temp06 == '' or temp06.startswith(' '):
            index06 += 1

    groups06.sort()

    del groups06[0:index06]

    allGroups['09.02.06'] = groups06

    groups07 = []

    test = test.find_next('ul', class_='nav nav-tabs')

    index07 = 0

    for group07 in test:
        group07.find('li')
        temp07 = group07.text
        temp07 = temp07.replace('\n','')
        link07 = group07.find_next('a')
        temp07 += ' ' + link07.get('href').replace('#', '')
        groups07.append(temp07)
        if temp07 == '' or temp07.startswith(' '):
            index07 += 1

    groups07.sort()
    del groups07[0:index07]

    allGroups['09.02.07'] = groups07

    groups10 = []

    test = test.find_next('ul', class_='nav nav-tabs')

    index10 = 0

    for group10 in test:
        group10.find('li')
        temp10 = group10.text
        temp10 = temp10.replace('\n','')
        link10 = group10.find_next('a')
        temp10 += ' ' + link10.get('href').replace('#', '')
        groups10.append(temp10)
        if temp10 == '' or temp10.startswith(' '):
            index10 += 1

    groups10.sort()

    del groups10[0:index10]

    allGroups['10.02.05'] = groups10

    groups40 = []

    test = test.find_next('ul', class_='nav nav-tabs')

    index40 = 0

    for group40 in test:
        group40.find('li')
        temp40 = group40.text
        temp40 = temp40.replace('\n','')
        link40 = group40.find_next('a')
        temp40 += ' ' + link40.get('href').replace('#', '')
        groups40.append(temp40)
        if temp40 == '' or temp40.startswith(' '):
            index40 += 1

    groups40.sort()
    del groups40[0:index40]

    allGroups['40.02.01'] = groups40

    groups1kurs = []

    test = test.find_next('ul', class_='nav nav-tabs')

    index1kurs = 0

    for group1kurs in test:
        group1kurs.find('li')
        temp1kurs = group1kurs.text
        temp1kurs = temp1kurs.replace('\n','')
        link1kurs = group1kurs.find_next('a')
        temp1kurs += ' ' + link1kurs.get('href').replace('#', '')
        groups1kurs.append(temp1kurs)
        if temp1kurs == '' or temp1kurs.startswith(' '):
            index1kurs += 1

    groups1kurs.sort()
    del groups1kurs[0:index1kurs]

    allGroups['Отделение первого курса'] = groups1kurs

    week_legend = {'Неделя': current_week_from_html}  

    def get_schedule(id: str, soup: bs):
        week = []
        schedule = soup.find('div', id = id)
        schedule = schedule.find_all('table')
        for table in schedule:
            day = table.find_next('h4').text
            i = 0
            for i in range(int(len(day))):
                if day[i].isupper() and day[i + 1].islower():
                    day = day[0:i]
                    break
            day = day.replace('\n', '')
            day += ' ' + table.find_next('span').text
            day = day.strip()
            week.append(day)
        dict_schedule = dict.fromkeys(week, [])
        for table in schedule:
            subjects = []
            day = table.find_next('h4').text
            i = 0
            for i in range(int(len(day))):
                if day[i].isupper() and day[i + 1].islower():
                    day = day[0:i]
                    break
            day = day.replace('\n', '')
            day += ' ' + table.find_next('span').text
            day = day.strip()
            tr_from_html = table.find_next('tbody')
            tr_from_html = tr_from_html.find_next('tbody')
            tr_from_html = tr_from_html.find_all('tr')
            subject_str = ''
            for td_from_html in tr_from_html:
                if td_from_html.find('div') is not None:
                    subject_str = td_from_html.find('td').text + ' '
                    if week[0] == 'Числитель':
                        td_from_html = td_from_html.find_next('div', class_='label label-danger')
                        subject_str += td_from_html.text.strip() + ' '
                        td_from_html = td_from_html.find_next('div', class_='label label-danger')
                        subject_str += td_from_html.text.strip()
                    else:
                        td_from_html = td_from_html.find_next('div', class_='label label-info')
                        subject_str += td_from_html.text.strip() + ' '
                        td_from_html = td_from_html.find_next('div', class_='label label-info')
                        subject_str += td_from_html.text.strip()
                else:
                    subject_str = td_from_html.text
                subject_str = subject_str.replace('\n', ' ')
                
                subjects.append(subject_str)
            subjects = list(filter(len, map(str.strip, subjects)))
            dict_schedule[day] = subjects
        return dict_schedule

    all_groups_schedule = {}

    for special in allGroups:
        if special != 'Неделя':
            for group in allGroups[special]:
                index = 0
                for index in range(int(len(group))):
                    if group[index].isspace() and (group[index + 1].islower() or group[index + 1].isdigit()):
                        id_group = group[index + 1: int(len(group))]
                        name_group = group[0: index]
                        break
                name_group = name_group.replace('/', ';')
                all_groups_schedule[name_group] = get_schedule(id_group, soup)

    def get_change_schedule(soup: bs):
        days_dict = {}
        days_list = []
        groups_with_changed_subjects_list = []
        days_schedule = soup.find_all('h4')
        groups = soup.find('hr').find_all_previous('caption')
        for day in days_schedule:
            days_list.append(day.text)
        days_dict = dict.fromkeys(days_list, [])
        subjects_changed = soup.find('hr').find_all_previous('table')
        for day in days_list:
            for group in groups:
                i = 0
                group_formated = group.text
                for i in range(int(len(group_formated))):
                    if group_formated[i].isspace():
                        group_formated = group_formated[i + 1:int(len(group_formated))]
                        break
                group_formated = group_formated.replace('/', ';')    
                groups_with_changed_subjects_list.append(group_formated)
            groups_with_changed_subjects_dict = dict.fromkeys(groups_with_changed_subjects_list, [])
            for subjects in subjects_changed:
                subjects_list = []
                name_group = subjects.find('caption').text
                for i in range(int(len(name_group))):
                    if name_group[i].isspace():
                        name_group = name_group[i + 1:int(len(name_group))]
                        name_group = name_group.replace('/', ';')
                        break
                subject = subjects.find_all('tr')
                for line in subject:
                    subject_line = line.text.replace('\n', 'C').replace(' ', 'T').strip()
                    j = 0
                    first_index_T = 0
                    last_index_T = 0
                    for j in range(int(len(subject_line))):
                        if subject_line[j] == 'T' and subject_line[j + 1] == 'T':
                            first_index_T = j
                            while j <= (int(len(subject_line))):
                                if subject_line[j] == 'T' and subject_line[j + 1] != 'T':
                                    last_index_T = j
                                    break
                                j += 1    
                            break
                    subject_line = subject_line[:first_index_T] + subject_line[last_index_T:]
                    subject_line = subject_line.replace('C', ' ').replace('T', ' ').strip()
                    subjects_list.append(subject_line)
                groups_with_changed_subjects_dict[name_group] = subjects_list
            days_dict[day] = groups_with_changed_subjects_dict
            if len(days_list) > 1:
                groups_with_changed_subjects_list.clear()
                groups = soup.find('hr').find_all_next('caption')
                subjects_changed = soup.find('hr').find_all_next('table')
        return days_dict
    
    def get_schedule_time(soup:bs):
        time = {}
        time_from_html = soup.find('table', class_='table').find_next('table', class_='table')
        time_from_html = time_from_html.find_next('tbody')
        for item in time_from_html:
            if not item.text.isspace() and item.text.find('Р') == -1:
                key_dict = item.text.strip()
                content_dict = item.text.strip()
                key_dict = key_dict[1:2]
                content_dict = content_dict[9:]
                print(f'{key_dict}+{content_dict}')
                time[key_dict] = content_dict
        print(time)
        return time


    time_schedule = get_schedule_time(soup)
    
    changed_schedule = get_change_schedule(soup_change_schedule)

    all_groups_class = []
    all_groups_schedule_class = []
    changed_schedule_class = []
    week_class = []
    time_class = []

    for item in allGroups:
        class_item = items(item, allGroups[item])
        all_groups_class.append(class_item.__dict__)

    for item in all_groups_schedule:
        class_item = items(item, all_groups_schedule[item])
        all_groups_schedule_class.append(class_item.__dict__)

    for item in changed_schedule:
        class_item = items(item, changed_schedule[item])
        changed_schedule_class.append(class_item.__dict__)

    for item in time_schedule:
        class_item = items(item, time_schedule[item])
        time_class.append(class_item.__dict__)

    class_item = items('Неделя', week_legend['Неделя'])
    week_class.append(class_item.__dict__)
        

    full_info_dict = {'groups': all_groups_class, 'schedule': all_groups_schedule_class, 'changed_schedule': changed_schedule_class}

    week_write = json.dumps(week_class, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    pathlib.Path(os.path.abspath("week.json")).write_text(week_write, encoding="utf-8")

    groups_write = json.dumps(all_groups_class, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    pathlib.Path(os.path.abspath("info.json")).write_text(groups_write, encoding="utf-8")

    schedule_write = json.dumps(all_groups_schedule_class, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    pathlib.Path(os.path.abspath("schedule.json")).write_text(schedule_write, encoding="utf-8")

    changed_schedule_write = json.dumps(changed_schedule_class, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    pathlib.Path(os.path.abspath("changedschedule.json")).write_text(changed_schedule_write, encoding="utf-8")

    time_write = json.dumps(time_class, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    pathlib.Path(os.path.abspath("timeschedule.json")).write_text(time_write, encoding="utf-8")

    full_info = json.dumps(full_info_dict, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    pathlib.Path(os.path.abspath("fullinfo.json")).write_text(full_info, encoding="utf-8")


click()
app = Flask(__name__)
api = Api(app)

class Quote(Resource):
    def get(self,id='0'):
        read_groups = pathlib.Path(os.path.abspath("info.json")).read_text(encoding="utf-8")

        groups = json.loads(read_groups)
        if id == '0':
            return groups, 200
        for quote in groups:
            if(quote['id'] == id):
                return quote, 200
        return "Quote not found", 404
    
class Schedule(Resource):
    def get(self,id='0'):
        read_schedule = pathlib.Path(os.path.abspath("schedule.json")).read_text(encoding="utf-8")

        schedule = json.loads(read_schedule)
        if id == '0':
            return schedule, 200
        for quote in schedule:
            if(quote['id'] == id):
                return quote, 200
        return "Quote not found", 404
    
class ChangedSchedule(Resource):
    def get(self,id='0'):
        read_changed_schedule = pathlib.Path(os.path.abspath("changedschedule.json")).read_text(encoding="utf-8")

        changed_schedule = json.loads(read_changed_schedule)
        if id == '0':
            return changed_schedule, 200
        if (len(changed_schedule) > 0):
            if (id[:-1] in changed_schedule[0]['dicts'] and id[-1] == '1'):
                return changed_schedule[0]['dicts'].get(id[:-1]), 200
        if (len(changed_schedule) > 1):
            if (id[:-1] in changed_schedule[1]['dicts'] and id[-1] == '2'):
                return changed_schedule[1]['dicts'].get(id[:-1]), 200
            
        return "Quote not found", 404
    
class Week(Resource):
    def get(self,id='Неделя'):
        read_week = pathlib.Path(os.path.abspath("week.json")).read_text(encoding="utf-8")

        week = json.loads(read_week)
        if id == 'Неделя':
            return week, 200
        return "Quote not found", 404
    
class Time(Resource):
    def get(self,id='0'):
        read_time = pathlib.Path(os.path.abspath("timeschedule.json")).read_text(encoding="utf-8")

        time = json.loads(read_time)
        if id == '0':
            return time, 200
        for quote in time:
            if(quote['id'] == id):
                return quote, 200
        return "Quote not found", 404   

    
api.add_resource(Quote, "/groups", "/groups/", "/groups/<string:id>")
api.add_resource(Schedule, "/schedule", "/schedule/", "/schedule/<string:id>")
api.add_resource(ChangedSchedule, "/changed_schedule", "/changed_schedule/", "/changed_schedule/<string:id>")
api.add_resource(Week, "/Week", "/Week/", "/Week/<string:id>")
api.add_resource(Time, "/time", "/Time/", "/Time/<string:id>")

if __name__ == '__main__':
    app.run(debug=True)
