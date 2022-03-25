# Strawberry Wagtail 🐦

A plug and play GraphQL API for Wagtail, powered by
[Strawberry](https://strawberry.rocks) 🍓

> ⚠️ Strawberry wagtail is currently experimental, please report any bugs or
> missing features

## Quick start

1. Install Strawberry Wagtail

```bash
pip install strawberry-wagtail
```

2. Add `strawberry-wagtail` to your `INSTALLED_APPS`:

```python

INSTALLED_APPS = [
    "home",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    ...,
    "strawberry_wagtail",
]
```

3. Add the GraphQL view to your urls:

```python
from strawberry_wagtail.views import GraphQLView

from django.urls import path


urlpatterns = [
    path("graphql", GraphQLView.as_view()),
]
```

4. Done! You can now try your GraphQL API by going to
   [http://localhost:8000/graphql](http://localhost:8000/graphql)
