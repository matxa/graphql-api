"""TypeDefs ⬇
   ▪️ Company
   ▪️ Employee
"""
from graphene import Field, List, String, ObjectType
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from mongoengine import DoesNotExist
from .models import (
    Company as CompanyModel,
    Employee as EmployeeModel
)


class Employee(MongoengineObjectType):
    class Meta:
        model = EmployeeModel

    companies = List(lambda: Company)
    pending_requests = List(lambda: Company)

    def resolve_companies(root, info):
        return CompanyModel.objects.filter(
            employees__contains=root.id)

    def resolve_pending_requests(root, info):
        return CompanyModel.objects.filter(
            pending_requests__contains=root.id)


class Company(MongoengineObjectType):
    class Meta:
        model = CompanyModel

    employees = List(lambda: Employee)
    pending_requests = List(lambda: Employee)

    def resolve_employees(root, info):
        return EmployeeModel.objects.filter(
            companies__contains=root.id)

    def resolve_pending_requests(root, info):
        return EmployeeModel.objects.filter(
            pending_requests__contains=root.id)
