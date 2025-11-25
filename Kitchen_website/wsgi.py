"""
WSGI config for Kitchen_website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Kitchen_website.settings")

application = get_wsgi_application()


import os
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

TEST_USER = os.environ.get("TEST_USER_NAME")
TEST_PASS = os.environ.get("TEST_USER_PASSWORD")
TEST_EMAIL = os.environ.get("TEST_USER_EMAIL")

if TEST_USER and TEST_PASS:
    try:
        User = get_user_model()

        if not User.objects.filter(username=TEST_USER).exists():
            User.objects.create_user(
                username=TEST_USER,
                email=TEST_EMAIL or "",
                password=TEST_PASS,
            )
            print(">>> [Render] Created test user:", TEST_USER)
        else:
            print(">>> [Render] Test user already exists.")
    except OperationalError:
        print(">>> [Render] Database not ready. Skipping test user creation.")
