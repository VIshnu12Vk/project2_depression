
import xml.etree.ElementTree as ET
import random
from django.http import HttpResponse

file_name = "depression_app/static/depression_app/xml/questionnair_dep.xml"
tree = ET.parse(file_name) 
root = tree.getroot() 
# question_list = []
question_list=[{'dep': ['Do you feel like you have lost hope in yourself and in the world?', 'Do you have any strategies for coping with hopelessness?'], 'score': 10, 'id': 1}, 
 {'dep': ['Are you feeling frustrated about something', 'You seem a bit on edge. Are you feeling irritable, frustrated, or restless?'], 'score': 10, 'id': 1}, 
 {'dep': ['Do you feel remorse for anything you have done?', 'Do you feel like you have been struggling with feelings of guilt, worthlessness, or helplessness lately?'], 'score': 10, 'id': 1},
 {'dep': ["Do you feel like you've lost interessst in activities you used to enjoy?", 'Have you noticed a decrease in your enthusiasm for the things that you used to like to do?'], 'score': 10, 'id': 1},
 {'dep': ["Do you have difficulty completing tasks that normally wouldn't take much effort?", "Have you been feeling like you don't have as much energy as you used to?"], 'score': 20, 'id': 2},
 {'dep': ['Have you noticed any changes in your appetite recently?', 'Have you noticed any noticeable changes in your appetite or weight that were not planned?'], 'score': 10, 'id': 1},
 {'dep': ['Have you had any thoughts of death or suicide lately?', "Is there anything that has been making you feel like life isn't worth living?"], 'score': 20, 'id': 2},
 {'dep': ['Do you feel sleepy during the day even after getting enough sleep at night?', '-Do you have difficulty falling asleep at night?'], 'score': 10, 'id': 1},
 {'dep': ['Do You Have A Past Experience Of Depression?', 'Have you ever experienced depression in the past?'], 'score': 20, 'id': 2},
 {'dep': ['Is Any One In Your Family Had A Depression', 'Have any members of your family experienced depression?'], 'score': 20, 'id': 2}]  
 
def question():
    if  question_list:
        # for question in root.findall('question'):
        #     question_dict = {}
        #     for child in question:
        #         key = child.tag
        #         if key == 'score':
        #             value = int(child.text)
        #         elif key == 'id':
        #             value = int(child.text)
        #         else:
        #             query_list = []
        #             for query in child.findall('query'):
        #                 query_list.append(query.text)
        #             value = query_list
        #         question_dict[key] = value
        #     question_list.append(question_dict)
        #     a=True
    
        random_element = random.choice(question_list)
        # print(random_element['dep'][0])
        random_index = question_list.index(random_element)
        question_list.pop( random_index)
    else:
        return False
    return random_element['dep'][0]

# print(question())
