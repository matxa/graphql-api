"""All Mutations ⬇
   ▪️ CreateManager
   ▪️ CreateCompany
   ▪️ CreateJob
   ▪️ CreateEmployee
"""
import graphene
from graphql import GraphQLError
from graphene_mongo import MongoengineObjectType
from .models import (
    Manager as ManagerModel,
    Company as CompanyModel,
    Job as JobModel,
    Employee as EmployeeModel
)
from mongoengine.errors import NotUniqueError, DoesNotExist
from .type_defs import (
    Company,
    Manager,
    Job,
    Employee
)
from .utils import hash_pwd
import uuid


class CreateCompany(graphene.Mutation):
    class Arguments:
        name = graphene.NonNull(graphene.String)
        manager_email = graphene.NonNull(graphene.String)
        description = graphene.String()
        
    company = graphene.Field(lambda: Company)

    def mutate(root, info, name, manager_email, description):
        try:
            if CompanyModel.objects.get(
                id=ManagerModel.objects.get(
                    email=manager_email).id) is not None:
                    raise GraphQLError("Manager Already has a company")
            company = CompanyModel(
                id=ManagerModel.objects.get(email=manager_email).id,
                name=name,
                description=description
                )
            company.save()
            return CreateCompany(company=company)
        except Exception as e:
            raise GraphQLError(e)


class CreateManager(graphene.Mutation):
    class Arguments:
        first_name = graphene.NonNull(graphene.String)
        last_name = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    manager = graphene.Field(lambda: Manager)

    def mutate(root, info, first_name, last_name, email, password):
        try:
            manager = ManagerModel(first_name=first_name, last_name=last_name,
                                   email=email, password=hash_pwd(password))
            manager.save()
            return CreateManager(manager=manager)
        except NotUniqueError:
            raise GraphQLError("A manager with that email already exist")


class CreateJob(graphene.Mutation):
    class Arguments:
        manager_email = graphene.NonNull(graphene.String)
        title = graphene.NonNull(graphene.String)
        description = graphene.String()

    job = graphene.Field(lambda: Job)

    def mutate(root, info, manager_email, title, description):
        try:
            job = JobModel(
                manager_id=ManagerModel.objects.get(email=manager_email).id,
                title=title,
                description=description,
            )
            company = CompanyModel.objects.get(
                id=ManagerModel.objects.get(email=manager_email).id)
            job.save()
            company.jobs.append(job.id)
            company.save()
            return CreateJob(job=job)
        except Exception as e:
            raise GraphQLError(e)


class CreateEmployee(graphene.Mutation):
    class Arguments:
        manager_email = graphene.NonNull(graphene.String)
        first_name = graphene.NonNull(graphene.String)
        last_name = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)

    employee = graphene.Field(Employee)
        
    def mutate(root, info, first_name, last_name, email, manager_email):
        try:
            try:
                EmployeeModel.objects.get(
                    email=email,
                    manager_id=ManagerModel.objects.get(
                        email=manager_email).id)
            except DoesNotExist:
                employee = EmployeeModel(
                    manager_id=ManagerModel.objects.get(
                        email=manager_email).id,
                        first_name=first_name,
                        last_name=last_name,
                        email=email, 
                        password=str(uuid.uuid4()))
                company = CompanyModel.objects.get(
                    id=ManagerModel.objects.get(email=manager_email).id)
                employee.save()
                company.employees.append(employee.id)
                company.save()
                return CreateEmployee(employee=employee)
        except NotUniqueError:
            raise GraphQLError("Employee with that email already exist")


class Mutation(graphene.ObjectType):
    create_manager = CreateManager.Field()
    create_company = CreateCompany.Field()
    create_job = CreateJob.Field()
    create_employee = CreateEmployee.Field()
