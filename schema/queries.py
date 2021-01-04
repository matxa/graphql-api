"""All Queries ⬇
   ▪️ company ➡ Get all information about company given the rigth credentials
       ↪ manager → get manager of company
       ↪ job → get job by title
       ↪ jobs → get all available jobs in in the company
       ↪ employees → get all employees of the company
"""
import graphene
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from .models import (
    Manager as ManagerModel,
    Company as CompanyModel,
    Job as JobModel,
    Employee as EmployeeModel
)
from mongoengine.errors import NotUniqueError, DoesNotExist
from .type_defs import (
    Manager,
    Job,
    Employee,
    Company
)
from .utils import hash_pwd, check_pwd


class Query(graphene.ObjectType):
    company = graphene.Field(
        Company,
        email=graphene.NonNull(graphene.String),
        password=graphene.NonNull(graphene.String))

    def resolve_company(root, info, email, password):
        try:
            company = CompanyModel.objects.get(
                id=ManagerModel.objects.get(email=email).id)
            if check_pwd(password,
             ManagerModel.objects.get(email=email).password):
                return company
            raise GraphQLError("Wrong password")
        except DoesNotExist:
            raise GraphQLError(
                f"Manager with the email: {email} doesn't exist")
