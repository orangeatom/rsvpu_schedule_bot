from peewee import *
from query_bot import User, Teacher, Group
import parser

database = SqliteDatabase('documents/users.db')
print('creation database')
database.connect()
print('creation tables')
database.create_tables([User, Group, Teacher], safe=True)
database.close()

groups, teachers = parser.update_links().values()

print('fill fields of groups')
for group in groups:
    GR,_ = Group.create_or_get(group_id=groups[group], group_name=group)
    GR.save()

print('fill fields of teachers')
for teacher in teachers:
    TC,_ = Teacher.create_or_get(teacher_id=teachers[teacher], teacher_name=teacher)
    TC.save()
print('complete!')
