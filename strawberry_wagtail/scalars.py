from typing import NewType

import strawberry


HTML = strawberry.scalar(NewType("HTML", str), serialize=str)
