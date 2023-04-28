import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get('DB_NAME'),
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DEV_DB_PASSWORD'),
        "HOST": 'localhost',
        "PORT": os.environ.get('DB_PORT'),

    }
}
