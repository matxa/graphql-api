"""TypeDefs ⬇
   ▪️ Manager
   ▪️ Company
   ▪️ Job
   ▪️ Employee
"""
from graphene import Field, List, String
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from mongoengine import DoesNotExist
from .models import (
    Manager as ManagerModel,
    Company as CompanyModel,
    Job as JobModel,
    Employee as EmployeeModel
)


class Manager(MongoengineObjectType):
    class Meta:
        model = ManagerModel


class Job(MongoengineObjectType):
    class Meta:
        model = JobModel


class Employee(MongoengineObjectType):
    class Meta:
        model = EmployeeModel


class Company(MongoengineObjectType):
    class Meta:
        model = CompanyModel

    manager = Field(Manager)
    job = Field(Job, title=String())
    jobs = List(Job)
    employees = List(Employee)
    
    def resolve_manager(root, info):
        return ManagerModel.objects.get(id=root.id)

    def resolve_job(root, info, title):
        return JobModel.objects.get(manager_id=root.id, title=title)

    def resolve_jobs(root, info):
        return JobModel.objects.filter(manager_id=root.id)

    def resolve_employees(root, info):
        return EmployeeModel.objects.filter(manager_id=root.id)
