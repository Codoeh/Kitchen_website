from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="testpassword",
            years_of_experience="1",
        )

    def test_years_of_experience_listed(self):
        url = reverse("catalog:cook-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.cook.years_of_experience)

    def test_years_of_experience_update(self):
        url = reverse("catalog:cook-update", args=[self.cook.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.cook.years_of_experience)
