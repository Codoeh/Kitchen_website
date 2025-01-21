from django.contrib.auth import get_user_model
from django.test import TestCase, Client



class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_superuser(
            username="cook",
            password="testpassword",
            years_of_experience="1",
        )