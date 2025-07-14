import graphene
from graphene_django import DjangoObjectType
from crm.models import Product

# GraphQL Type for Product
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

# Mutation: Update low-stock products
class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated.append(product)

        return UpdateLowStockProducts(
            updated_products=updated,
            message=f"{len(updated)} products restocked successfully."
        )

# Root Query
class Query(graphene.ObjectType):
    products = graphene.List(ProductType)

class mutation(graphene.ObjectType):

    def resolve_products(self, info):
        return Product.objects.all()

# Root Mutation
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Final schema
schema = graphene.Schema(query=Query, mutation=Mutation)
