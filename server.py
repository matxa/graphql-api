""" ✅ Server/App Config """
from flask import Flask, redirect
from flask_graphql import GraphQLView
from flask_mongoengine import MongoEngine
import graphene
from schema.queries import Query
from mongoengine import connect
from schema.mutations import Mutation
import os


"""Flask App"""
app = Flask(__name__)

"""DATABASE CONNECTION"""
DB_URI = f"mongodb+srv://root:root@cluster0.qgdv3.mongodb.net/\
ConTime?retryWrites=true&w=majority"

app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine(app)


@app.route('/')
def redirect_to_gql():
    return redirect('/graphql')


"""GraphQL Server"""
schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))


if __name__ == '__main__':
    app.run()
