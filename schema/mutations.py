"""All Mutations ⬇
   ▪️ CreateCompany
   ▪️ CreateEmployee
   ▪️ RequestEmployee
   ▪️ AcceptRequest
   ▪️ Decline Request
   ▪️ DeleteEmployee
   ▪️ DeleteCompany
   ▪️ DeleteEmployeeFromCompany
"""
from bson import ObjectId
import bcrypt
import graphene
from graphql import GraphQLError
from graphene_mongo import MongoengineObjectType
from .models import (
    Company as CompanyModel,
    Employee as EmployeeModel
)
from mongoengine.errors import NotUniqueError, DoesNotExist
from .type_defs import (
    Company,
    Employee,
)
from .utils import hash_pwd, check_pwd


class CreateCompany(graphene.Mutation):
    class Arguments:
        company_name = graphene.NonNull(graphene.String)
        description = graphene.String()
        first_name = graphene.NonNull(graphene.String)
        last_name = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)
        
    company = graphene.Field(lambda: Company)

    def mutate(root, info, company_name, description,
                first_name, last_name, email, password):
        try:
            company = CompanyModel(
                company_name=company_name,
                description=description,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hash_pwd(password))
            company.save()
            return CreateCompany(company=company)
        except NotUniqueError:
            raise GraphQLError("A company with that email already exist")


class CreateEmployee(graphene.Mutation):
    class Arguments:
        first_name = graphene.NonNull(graphene.String)
        last_name = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    employee = graphene.Field(lambda: Employee)
        
    def mutate(root, info, first_name, last_name, email, password):
        try:
            employee = EmployeeModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=bcrypt.hashpw(password, bcrypt.gensalt(14)))
            employee.save()
            return CreateEmployee(employee=employee)
        except NotUniqueError:
            raise GraphQLError("Employee with that email already exist")


class RequestEmployee(graphene.Mutation):
    class Arguments:
        company_email = graphene.NonNull(graphene.String)
        employee_email = graphene.NonNull(graphene.String)

    success = graphene.String()

    def mutate(root, info, company_email, employee_email):
        try:
            company = CompanyModel.objects.get(email=company_email)
            employee = EmployeeModel.objects.get(email=employee_email)
            if employee.id not in company.employees and employee.id not\
             in company.pending_requests:
                company.pending_requests.append(employee.id)
                employee.pending_requests.append(company.id)
                company.save()
                employee.save()
                return RequestEmployee(success="Success")
            else:
                return GraphQLError(f"Employee already working for company")
        except DoesNotExist:
            return GraphQLError(f"No employee with email {employee_email}")


class AcceptRequest(graphene.Mutation):
    class Arguments:
        employee_email = graphene.NonNull(graphene.String)
        company_id = graphene.NonNull(graphene.String)

    success = graphene.String()

    def mutate(root, info, company_id, employee_email):
        try:
            employee = EmployeeModel.objects.get(email=employee_email)
            company = CompanyModel.objects.get(id=ObjectId(company_id))
            employee.companies.append(ObjectId(company_id))
            employee.pending_requests.remove(ObjectId(company_id))
            company.pending_requests.remove(employee.id)
            company.employees.append(employee.id)
            employee.save()
            company.save()
            return RequestEmployee(success="Success")
        except DoesNotExist:
            return GraphQLError(f"No employee with email {employee_email}")


class DeclineRequest(graphene.Mutation):
    class Arguments:
        employee_email = graphene.NonNull(graphene.String)
        company_id = graphene.NonNull(graphene.String)

    success = graphene.String()

    def mutate(root, info, company_id, employee_email):
        try:
            employee = EmployeeModel.objects.get(email=employee_email)
            company = CompanyModel.objects.get(id=ObjectId(company_id))
            employee.pending_requests.remove(ObjectId(company_id))
            company.pending_requests.remove(employee.id)
            employee.save()
            company.save()
            return RequestEmployee(success="Success")
        except DoesNotExist:
            return GraphQLError(f"No employee with email {employee_email}")


class DeleteEmployee(graphene.Mutation):
    class Arguments:
        email = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)
    
    employee = graphene.Field(lambda: Employee)

    def mutate(root, info, email, password):
        try:
            employee = EmployeeModel.objects.get(email=email)
            if check_pwd(password,
             EmployeeModel.objects.get(email=email).password):
                companies_e = CompanyModel.objects.filter( # employees_list
                    employees__contains=employee.id)
                companies_p = CompanyModel.objects.filter(
                    pending_requests__contains=employee.id) # pending_list
                if companies_e:
                    for company in companies_e:
                        company.employees.remove(employee.id)
                        company.save()
                if companies_p:
                    for company in companies_p:
                        company.pending_requests.remove(employee.id)
                        company.save()
                employee.delete()
                return DeleteEmployee(employee=employee)
            else:
                raise GraphQLError("Wrong [ password ]")
        except DoesNotExist:
            return None


class DeleteCompany(graphene.Mutation):
    class Arguments:
        email = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)
    
    company = graphene.Field(lambda: Company)

    def mutate(root, info, email, password):
        try:
            company = CompanyModel.objects.get(email=email)

            if check_pwd(password,
             CompanyModel.objects.get(email=email).password):
                employees = EmployeeModel.objects.filter(
                    companies__contains=company.id)
                if employees:
                    for employee in employees:
                        employee.companies.remove(company.id)
                        employee.save()
                company.delete()
                return company
            else:
                raise GraphQLError("Wrong [ password ]")
        except DoesNotExist:
            return None


class DeleteEmployeeFromCompany(graphene.Mutation):
    class Arguments:
        company_email = graphene.NonNull(graphene.String)
        employee_id = graphene.NonNull(graphene.String)
    
    company = graphene.Field(lambda: Company)

    def mutate(root, info, company_email, employee_id):
        try:
            company = CompanyModel.objects.get(email=company_email)
            employee = EmployeeModel.objects.get(id=ObjectId(employee_id))
            if employee.id in company.employees:
                company.employees.remove(employee.id)
                employee.companies.remove(company.id)
                employee.save()
                company.save()
                return company
            else:
                raise GraphQLError(f"{employee_id} is not your employee")
        except DoesNotExist:
            raise GraphQLError("A company with that email doesn't exist")


class Mutation(graphene.ObjectType):
    create_company = CreateCompany.Field()
    create_employee = CreateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
    delete_company = DeleteCompany.Field()
    request_employee = RequestEmployee.Field()
    accept_request = AcceptRequest.Field()
    decline_request = DeclineRequest.Field()
    delete_employee_from_compnay = DeleteEmployeeFromCompany.Field()
