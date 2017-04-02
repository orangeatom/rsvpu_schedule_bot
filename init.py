"""this module prepare workspase for work"""
import peewee
from query_bot import User, Teacher, Group
import parser



localDB = peewee.SqliteDatabase('documents/users.db')
print('creation database')
localDB.connect()
print('creation tables')
try:
    localDB.drop_table(Group)
    print("table Group is dropped")
    localDB.drop_table(Teacher)
    print("table Teacher is dropped")
except:
    pass

localDB.create_tables([User, Group, Teacher], safe=True)
localDB.close()

groups, teachers = parser.update_links().values()
print('fill fields of groups')
i = 0
for group in groups:
    GR = Group.create(group_id=groups[group], group_name=group)
    GR.save()

print(len(teachers))
print('fill fields of teachers')
for teacher in teachers:
    TC = Teacher.create(teacher_id=teachers[teacher], teacher_name=teacher)
    TC.save()

print('complete!')
