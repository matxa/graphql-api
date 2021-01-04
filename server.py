""" ✅ Server/App Config """
from flask import Flask
from flask_graphql import GraphQLView
from flask_mongoengine import MongoEngine
import graphene
from schema.queries import Query
from mongoengine import connect
from schema.mutations import Mutation


"""Flask App"""
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {"db": "ConTime"}
db = MongoEngine(app)


"""GraphQL Server"""
schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))


if __name__ == '__main__':
    app.run(
        debug=True
    )
