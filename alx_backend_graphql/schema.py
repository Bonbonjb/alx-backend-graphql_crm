import graphene
from crm.schema isport Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    hello graphene.String()

    def resolve hello(root, info):
        return "Hello, GraphQL!"

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
