SECRET_KEY = "12345"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "wagtail.users",
    "wagtail.admin",
    "wagtail.images",
    "wagtail.core",
    "tests.my_app",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 2,
        },
    }
]


ROOT_URLCONF = "tests.urls"
