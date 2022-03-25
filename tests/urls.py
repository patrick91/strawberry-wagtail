from strawberry_wagtail.views import GraphQLView

from django.urls import path


urlpatterns = [
    path("graphql", GraphQLView.as_view()),
]
