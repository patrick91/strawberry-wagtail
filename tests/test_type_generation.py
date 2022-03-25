import textwrap

from strawberry_wagtail.schema import get_schema_from_models

from tests.my_app.models import BlogPage, CMSPage


def test_convert_type():
    schema = get_schema_from_models([BlogPage])

    assert (
        str(schema)
        == textwrap.dedent(
            """
        type BlogPage {
          id: ID!
          title: String!
          body: HTML!
        }

        scalar HTML

        type Query {
          blogPage(pk: ID): BlogPage
          blogPages: [BlogPage!]!
        }
        """
        ).strip()
    )


def test_convert_type_with_streamfield():
    schema = get_schema_from_models([CMSPage])

    assert (
        str(schema)
        == textwrap.dedent(
            """
        type CMSPage {
          id: ID!
          title: String!
          body: [CMSPageBody!]!
        }

        union CMSPageBody = CMSPageBodyHeading | CMSPageBodyParagraph | CMSPageBodyTwoColumns

        type CMSPageBodyHeading {
          id: ID!
          value: String!
        }

        type CMSPageBodyParagraph {
          id: ID!
          html: HTML!
        }

        type CMSPageBodyTwoColumns {
          id: ID!
          values: [CMSPageBodyTwoColumnsValues!]!
        }

        type CMSPageBodyTwoColumnsText {
          id: ID!
          html: HTML!
        }

        union CMSPageBodyTwoColumnsValues = CMSPageBodyTwoColumnsText

        scalar HTML

        type Query {
          cmsPage(pk: ID): CMSPage
          cmsPages: [CMSPage!]!
        }
        """
        ).strip()
    )
