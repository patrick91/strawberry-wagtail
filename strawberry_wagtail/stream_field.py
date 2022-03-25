import dataclasses
from typing import Any, Callable, List, Optional, Type

from wagtail.core.blocks.field_block import CharBlock, FieldBlock, RichTextBlock
from wagtail.core.blocks.stream_block import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

import strawberry
import strawberry.django
from strawberry.union import StrawberryUnion
from strawberry.utils.str_converters import capitalize_first, to_camel_case

from .scalars import HTML


def _make_type(
    class_name: str, value_field_name: str, value_type: Type, from_data: Callable
) -> Type:
    # TODO: don't use dataclasses
    x = dataclasses.make_dataclass(
        class_name, [("id", strawberry.ID), (value_field_name, value_type)]
    )
    x.from_data = classmethod(from_data)

    return strawberry.type(x)


def get_type_for_stream_block(
    block: StreamBlock,
    class_name: str,
) -> Type:
    types = set()

    block_map = {}

    for field_block in block.child_blocks.values():
        name = class_name + capitalize_first(to_camel_case(field_block.name))
        type_ = _get_type_for_field_block(field_block, name)

        if isinstance(type_, StrawberryUnion):
            assert type_.graphql_name
            type_.graphql_name += "Values"
            type_ = _make_type(name, "values", List[type_], None)

        block_map[field_block.name] = type_

        types.add(type_)

    union_type = strawberry.union(
        class_name, types=tuple(sorted(types, key=lambda x: str(x)))
    )
    union_type._block_map = block_map

    return union_type


def _get_type_for_field_block(field_block: FieldBlock, name: str) -> Optional[Type]:
    type_ = None

    if isinstance(field_block, CharBlock):

        def from_data(cls, data: dict) -> str:
            return cls(id=data["id"], value=data["value"])

        type_ = _make_type(name, "value", str, from_data)

    elif isinstance(field_block, RichTextBlock):

        def from_data(cls, data: dict) -> str:
            return cls(id=data["id"], html=data["value"])

        type_ = _make_type(name, "html", HTML, from_data)

    elif isinstance(field_block, ImageChooserBlock):

        def from_data(cls, data: dict) -> str:
            return cls(id=data["id"], image=data["value"])

        type_ = _make_type(name, "image", str, from_data)

    elif isinstance(field_block, StreamBlock):
        type_ = get_type_for_stream_block(field_block, name)

    if type_ is None:
        raise ValueError(f"Unknown type for {field_block}")

    type_._origin_field_block = field_block  # type: ignore

    return type_


def _get_block(block: dict, parent_type: Type) -> Any:
    block_type = parent_type._block_map.get(block["type"])

    if not block_type:
        return None

    block_data = block.copy()
    block_data.pop("type")

    if type(block["value"]) is list:
        # mmm

        print("🌼🌼🌼")
        print(block_type._type_definition.fields[1].__dict__)
        block_value_type = block_type._type_definition.fields[1].type.of_type
        value = [
            _get_block(sub_block, block_value_type) for sub_block in block["value"]
        ]

        print(block_type)
        print(block_value_type)
        print(value)

        return block_type(id=block_data["id"], values=value)

    return block_type.from_data(block_data)


def get_resolver_for_stream_field(field: StreamField, type: Type) -> Callable:
    def _resolver(root: Any) -> List[type]:
        raw_data = getattr(root, field.name)._raw_data

        data = []

        for block in raw_data:
            block_data = _get_block(block, type)

            if block_data:
                data.append(block_data)

        return data

    return _resolver
