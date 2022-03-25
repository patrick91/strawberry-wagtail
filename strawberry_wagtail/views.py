from functools import cached_property

from wagtail.core.models import Page

from django.apps import apps

from strawberry import Schema
from strawberry.django.views import GraphQLView as BaseGraphQLView

from .schema import get_schema_from_models


def get_schema() -> Schema:
    all_models = apps.get_models()

    page_models = (
        model for model in all_models if issubclass(model, Page) and model is not Page
    )

    return get_schema_from_models(page_models)


class GraphQLView(BaseGraphQLView):
    def __init__(
        self,
        graphiql=True,
        subscriptions_enabled=False,
    ):
        self.graphiql = graphiql
        self.subscriptions_enabled = subscriptions_enabled

    @cached_property
    def schema(self) -> Schema:
        return get_schema()
