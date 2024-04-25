from models import *


query = member.select().where(member.firstName == 'Mohamed')
for member in query:
    print(member.firstName, member.lastName)

query = chapter.select().where(chapter.chapterName == 'Madison County')
for chapter in query:
    print(chapter.chapterName)

query = event.select().where(event.eventName == 'Community Building')
for event in query:
    print(event.eventName)

query = donation.select().where(donation.item == 'Laptop')
for donation in query:
    print(donation.item)

