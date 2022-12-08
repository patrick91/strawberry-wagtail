from typing import Callable, List, Optional, Type

from wagtail.core.models import Page


def get_resolver_for_single_model(model_class: Type[Page]) -> Callable:
    def resolve_model(id: int) -> Optional[Page]:
        return model_class.objects.get(id=id)

    return resolve_model


def get_resolver_for_multiple_models(model_class: Type[Page]) -> Callable:
    # TODO: make this configurable ?
    # for example we can use headers for locale instead of a parameter

    def resolve_models(locale: Optional[str] = None) -> List[Page]:
        qs = model_class.objects.all()

        if locale is not None:
            qs = qs.filter(locale__language_code=locale)

        return qs

    return resolve_models
