"""All models ⬇
[ ▪️ Manager, ▪️ Employee, ▪️ Job, ▪️ Company ]
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    ObjectIdField,
    StringField,
    ListField,
    EmailField,
    DateTimeField
)


class Manager(Document):
    meta = {'collection': 'managers'}
    first_name = StringField(required=True, max_length=20)
    last_name = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=80)
    date_created = DateTimeField(default=datetime.now)


class Employee(Document):
    meta = {'collection': 'employees'}
    manager_id = ObjectIdField()
    jobs = ListField()
    first_name = StringField(required=True, max_length=20)
    last_name = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50)
    password = StringField(required=True, max_length=80)
    date_created = DateTimeField(default=datetime.now)


class Job(Document):
    meta = {'collection': 'jobs'}
    manager_id = ObjectIdField()
    title = StringField(required=True, unique=True)
    description = StringField(required=True, max_length=400)
    employees = ListField()
    date_created = DateTimeField(default=datetime.now)


class Company(Document):
    meta = {'collection': 'companies'}
    name = StringField(required=True, max_length=20)
    description = StringField(required=True, max_length=400)
    jobs = ListField()
    employees = ListField()
    date_created = DateTimeField(default=datetime.now)
