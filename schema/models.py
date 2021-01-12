"""All models ⬇
[ ▪️ Employee, ▪️ Company ]
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


class Employee(Document):
    meta = {'collection': 'employees'}
    companies = ListField()
    pending_requests = ListField()
    first_name = StringField(required=True, max_length=20)
    last_name = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=80)
    date_created = DateTimeField(default=datetime.now)


class Company(Document):
    meta = {'collection': 'companies'}
    company_name = StringField(required=True, max_length=20)
    description = StringField(required=True, max_length=400)
    first_name = StringField(required=True, max_length=20)
    last_name = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=80)
    employees = ListField()
    pending_requests = ListField()
    date_created = DateTimeField(default=datetime.now)
