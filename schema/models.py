"""All models ⬇
[ ▪️ Employee, ▪️ Company, ▪️ Calendar ]
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine.fields import (
    ObjectIdField,
    StringField,
    ListField,
    EmailField,
    DateTimeField,
    DecimalField
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


class Day(EmbeddedDocument):
    hours = DecimalField(default=0)
    description = StringField(default="N/A", max_length=250)
    location = StringField(default="N/A", max_length=20)


class Calendar(Document):
    meta = {'collection': 'calendars'}
    employee_id = ObjectIdField()
    company_id = ObjectIdField()
    week_id = StringField()
    sunday = EmbeddedDocumentField(Day, default=Day)
    monday = EmbeddedDocumentField(Day, default=Day)
    tuesday = EmbeddedDocumentField(Day, default=Day)
    wednesday = EmbeddedDocumentField(Day, default=Day)
    thursday = EmbeddedDocumentField(Day, default=Day)
    friday = EmbeddedDocumentField(Day, default=Day)
    saturday = EmbeddedDocumentField(Day, default=Day)
