from django.urls import path
from graphene_django.views import GraphQLView
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from crm.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))),
]
