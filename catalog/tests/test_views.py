from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import Cook, Dish, DishType


class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User",
            years_of_experience=5,
        )
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Test description",
            price=50.00,
            dish_type=self.dish_type,
        )
        self.dish.cooks.add(self.user)

    def test_index_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("catalog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/index.html")

    def test_cook_list_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("catalog:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/cook_list.html")
        self.assertContains(response, self.user.username)

    def test_cook_detail_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse(
            "catalog:cook-detail",
            args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/cook_detail.html")
        self.assertContains(response, self.user.first_name)

    def test_cook_create_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("catalog:cook-create"),
            {
                "username": "newcook",
                "password": "password123",  # Dodano hasło
                "first_name": "New",
                "last_name": "Cook",
                "years_of_experience": 3,
                "date_joined": datetime.now().isoformat(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cook.objects.filter(username="newcook").exists())

    def test_dish_list_view(self):
        self.client.login(username="testuser",
                          password="password123")
        response = self.client.get(reverse("catalog:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "catalog/dish_list.html")
        self.assertContains(response, self.dish.name)

    def test_dish_detail_view(self):
        self.client.login(username="testuser", password="password123")
        response = (self.client.
                    get(reverse("catalog:dish-detail",
                                args=[self.dish.id])))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "catalog/dish_detail.html")
        self.assertContains(response, self.dish.description)

    def test_dish_create_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("catalog:dish-create"),
            {
                "name": "New Dish",
                "description": "New description",
                "price": 75.00,
                "dish_type": self.dish_type.id,
                "cooks": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="New Dish").exists())

    def test_dish_type_list_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("catalog:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/dish_type_list.html")
        self.assertContains(response, self.dish_type.name)

    def test_dishes_by_type_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            reverse("catalog:dishes-by-type", args=[self.dish_type.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/dishes_by_type.html")
        self.assertContains(response, self.dish.name)

    def test_toggle_assign_to_dish(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("catalog:toggle-dish-assign", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.dish, self.user.dishes.all())

    def test_dish_create_view_with_negative_price(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("catalog:dish-create"),
            {
                "name": "Invalid Dish",
                "description": "Invalid description",
                "price": -75.00,
                "dish_type": self.dish_type.id,
                "cooks": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Dish.objects.filter(name="Invalid Dish").exists())
        form = response.context["form"]
        self.assertIn("price", form.errors)
        self.assertEqual(form.errors["price"], ["Price cannot be less than zero."])


    def test_cook_create_view_with_negative_experience(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("catalog:cook-create"),
            {
                "username": "Invalid",
                "password": "password123",
                "first_name": "New",
                "last_name": "Cook",
                "years_of_experience": -3,
                "date_joined": datetime.now().isoformat(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cook.objects.filter(username="Invalid").exists())
        form = response.context["form"]
        self.assertIn("years_of_experience", form.errors)
        self.assertEqual(form.errors["years_of_experience"], ["Years cannot be negative"])
