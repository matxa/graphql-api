"""All Queries ⬇
    ▪️ company ➡ Get all information about company given the rigth credentials
        ↪ manager → get manager of company
        ↪ job → get job by title
        ↪ jobs → get all available jobs in in the company
        ↪ employees → get all employees of the company
    ▪️ employee ➡ Get all information about employee given the right credentials
        ↪ manager → get manager of employee
        ↪ job → get job by title
        ↪ jobs → get all the jobs the employee is working for in the company
"""
import graphene
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from .models import (
    Company as CompanyModel,
    Employee as EmployeeModel
)
from mongoengine.errors import NotUniqueError, DoesNotExist
from .type_defs import (
    Employee,
    Company
)
from .utils import hash_pwd, check_pwd


class Query(graphene.ObjectType):
    company = graphene.Field(
        Company,
        email=graphene.NonNull(graphene.String),
        password=graphene.NonNull(graphene.String))

    employee = graphene.Field(
        Employee,
        email=graphene.NonNull(graphene.String),
        password=graphene.NonNull(graphene.String))

    def resolve_company(root, info, email, password):
        try:
            company = CompanyModel.objects.get(email=email)
            if check_pwd(password,
             CompanyModel.objects.get(email=email).password):
                return company
        except DoesNotExist:
            raise GraphQLError(
                f"Company with the email: {email} doesn't exist")

    def resolve_employee(root, info, email, password):
        try:
            employee = EmployeeModel.objects.get(email=email)
            if check_pwd(password,
             EmployeeModel.objects.get(email=email).password):
                return employee
        except DoesNotExist:
            raise GraphQLError(
                f"Employee with the email: {email} doesn't exist")
