import graphene
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from crm.schema import Query as CrmQuery

# --------------------
# GraphQL Object Types
# --------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")
        interfaces = (graphene.relay.Node,)

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price")
        interfaces = (graphene.relay.Node,)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "product", "quantity", "status")
        interfaces = (graphene.relay.Node,)

# --------------------
# GraphQL Input Types
# --------------------
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

# --------------------
# Queries (merged into a single class)
# --------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    filtered_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
    filtered_products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
    filtered_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()
# --------------------
# Mutations
# --------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)

    def mutate(self, info, name, email, phone=None):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []

        for i, item in enumerate(input):
            try:
                if Customer.objects.filter(email=item.email).exists():
                    raise ValidationError("Email already exists")

                phone = item.phone or ""
                if phone:
                    RegexValidator(
                        regex=r'^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$',
                        message="Invalid phone format"
                    )(phone)

                customer = Customer(name=item.name, email=item.email, phone=phone)
                customer.save()
                created.append(customer)

            except Exception as e:
                errors.append(f"Entry {i + 1}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()

# --------------------
# Schema
# --------------------
schema = graphene.Schema(query=Query, mutation=Mutation)
