import json

import pytest

from wagtail.core.models import Locale

from tests.my_app.models import BlogPage


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _locale():
    Locale.objects.create(language_code="en")


def test_view_with_no_data(client):
    response = client.post(
        "/graphql",
        data=json.dumps({"query": "{ blogPages { id } }"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert json.loads(response.content.decode()) == {
        "data": {"blogPages": []},
    }


def test_view_with_data(client):
    blog_page = BlogPage.objects.create(
        title="Test",
        path="0000",
        depth=0,
        body="Demo",
    )

    response = client.post(
        "/graphql",
        data=json.dumps({"query": "{ blogPages { id } }"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert json.loads(response.content.decode()) == {
        "data": {
            "blogPages": [
                {
                    "id": str(blog_page.id),
                }
            ]
        },
    }
