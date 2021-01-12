"""All Queries ⬇
    ▪️ company ➡ Get all information about company given the rigth credentials
        ↪ employees
        ↪ pending_requests
    ▪️ employee ➡ Get all information about employee given the right credentials
        ↪ companies
        ↪ pending_requests
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
