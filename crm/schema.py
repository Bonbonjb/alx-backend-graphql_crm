import graphene
from graphene_django import DjangoObjectType
from crm.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_list = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_list.append(product)

        return UpdateLowStockProducts(
            updated_products=updated_list,
            message=f"{len(updated_list)} products restocked successfully"
        )

# ✅ Fix: Define a basic Query class
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

class mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# ✅ Final schema declaration
schema = graphene.schema(query=Query, mutation=Mutation)
