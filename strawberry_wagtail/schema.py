import re
import types
from typing import Iterable, List, Optional, Type

from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from django.db.models.fields import Field

import strawberry
import strawberry.django
from strawberry.django import auto
from strawberry.utils.str_converters import capitalize_first, to_camel_case

from .scalars import HTML
from .stream_field import get_resolver_for_stream_field, get_type_for_stream_block


def to_snake_case(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _register_fields():
    from strawberry_django.fields.types import field_type_map
    from wagtail.core.fields import RichTextField

    field_type_map[RichTextField] = HTML


_register_fields()

body_fields = ["id", "title"]


def _get_field_type(field: Field, model_class: Type[Page]) -> Type:
    if isinstance(field, StreamField):
        name = model_class.__name__ + capitalize_first(to_camel_case(field.name))
        stream_block_type = get_type_for_stream_block(field.stream_block, name)
        return stream_block_type

    return auto


def _create_type(model_class: Type[Page]) -> Type:
    namespace = {}
    annotations = {}

    name = model_class.__name__

    excluded_fields = [field.name for field in Page._meta.get_fields()] + ["page_ptr"]

    for field in model_class._meta.get_fields():
        if field.name in body_fields or field.name not in excluded_fields:

            annotations[field.name] = _get_field_type(field, model_class)  # type: ignore

            if isinstance(field, StreamField):
                resolver = get_resolver_for_stream_field(
                    field, type=annotations[field.name]
                )
                annotations[field.name] = List[annotations[field.name]]
                namespace[field.name] = strawberry.field(resolver=resolver)

    namespace["__annotations__"] = annotations  # type: ignore

    cls = types.new_class(name, (), {}, lambda ns: ns.update(namespace))

    return strawberry.django.type(model_class, name=name)(cls)


def get_schema_from_models(models: Iterable[Type[Page]]) -> strawberry.Schema:
    fields = []
    namespace = {}
    annotations = {}

    for model_class in models:

        model_type = _create_type(model_class)

        name = to_snake_case(model_class.__name__)

        fields += [
            (name, Optional[model_type], strawberry.django.field()),
            (f"{name}s", List[model_type], strawberry.django.field()),
        ]

        for field_name, type_, value in fields:
            namespace[field_name] = value
            annotations[field_name] = type_

        namespace["__annotations__"] = annotations  # type: ignore

    cls = types.new_class("Query", (), {}, lambda ns: ns.update(namespace))
    Query = strawberry.type(name="Query")(cls)

    return strawberry.Schema(query=Query)
