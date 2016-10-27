from peewee import *
from dele import User, Teacher,Group
import parser

database = SqliteDatabase('documents/users.db')

database.connect()
database.create_tables([User, Group, Teacher], safe=True)
database.close()

groups = parser.update_links()['groups']
teachers = parser.update_links()['lecturers']

for group in groups:
    GR = Group.create_or_get(group_id=groups[group], group_name=group)
    GR[0].save()

for teacher in teachers:
    TC = Teacher.create_or_get(teacher_id=teachers[teacher], teacher_name=teacher)
    TC[0].save()



