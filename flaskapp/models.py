from peewee import *
from datetime import datetime
from peewee import Model, CharField
from flask_login import UserMixin

# Database Configuration
################################
mydb = PostgresqlDatabase("postgres",host="db",user="postgres",password="postgres")

class baseModel(Model):
    class Meta:
        database = mydb

# Class Definitionsa
# https://docs.peewee-orm.com/en/latest/peewee/models.html


class User(UserMixin):
    # Assuming a single user
    id = 1

    def get_id(self):
        return str(self.id)




class member(baseModel):
    memberid = PrimaryKeyField()
    firstname = CharField(100)
    middlename = CharField(100)
    lastname = CharField(100)
    phonenumber = CharField(100)
    score = IntegerField()
    memberaddress = CharField(255)
    numberofeventsattended = IntegerField()
    status = CharField(15)
   

class chapter(baseModel):
    chaptername = CharField(primary_key=True)
    numberofmembers = IntegerField()
    chapterlead = CharField()
    chapteremail = CharField()

class event(baseModel):
    eventname = CharField(primary_key=True)  # CamelCase as in your PostgreSQL
    venue = CharField()
    theme = CharField() 
    eventdate = DateField() 
    numberofmembersattended = IntegerField() 
    # chaptername = CharField()

class donation(baseModel):
    donationId = AutoField()
    donor = ForeignKeyField(member, backref='donations')  # Ensure this matches the column name in your DB
    item = CharField()
    monetaryWorth = IntegerField()






