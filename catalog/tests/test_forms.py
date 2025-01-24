from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.forms import (
    CookExperienceUpdateForm,
    CookSearchForm,
    DishForm,
    DishSearchForm,
    DishTypeSearchForm,
)
from catalog.models import DishType


class CookExperienceUpdateFormTest(TestCase):
    def test_valid_experience(self):
        form = CookExperienceUpdateForm(data={"years_of_experience": 5})
        self.assertTrue(form.is_valid())

    def test_negative_experience(self):
        form = CookExperienceUpdateForm(data={"years_of_experience": -3})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["years_of_experience"], ["Years cannot be negative"]
        )

    def test_zero_experience(self):
        form = CookExperienceUpdateForm(data={"years_of_experience": 0})
        self.assertTrue(form.is_valid())

    def test_empty_experience(self):
        form = CookExperienceUpdateForm(data={"years_of_experience": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["years_of_experience"], ["This field is required."]
        )


class CookSearchFormTest(TestCase):
    def test_empty_search(self):
        form = CookSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_valid_search(self):
        form = CookSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")


class DishFormTest(TestCase):
    def setUp(self):
        self.cook1 = get_user_model().objects.create_user(username="cook1")
        self.cook2 = get_user_model().objects.create_user(username="cook2")
        self.dish_type = DishType.objects.create(name="Test Type")

    def test_valid_dish_form(self):
        form = DishForm(
            data={
                "name": "Test Dish",
                "description": "Delicious dish",
                "price": 25.0,
                "dish_type": self.dish_type.id,
                "cooks": [self.cook1.id, self.cook2.id],
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_dish_form_missing_name(self):
        form = DishForm(
            data={
                "description": "Delicious dish",
                "price": 25.0,
                "dish_type": self.dish_type.id,
                "cooks": [self.cook1.id],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_price_less_than_zero(self):
        form = DishForm(
            data={
                "name": "Test Dish",
                "description": "Delicious dish",
                "price": -25.0,
                "dish_type": self.dish_type.id,
                "cooks": [self.cook1.id, self.cook2.id],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["price"], ["Price cannot be less than zero."]
        )

    def test_invalid_dish_form_missing_description(self):
        form = DishForm(
            data={
                "name": "Test Dish",
                "price": 25.0,
                "dish_type": self.dish_type.id,
                "cooks": [self.cook1.id, self.cook2.id],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_invalid_dish_form_missing_dish_type(self):
        form = DishForm(
            data={
                "name": "Test Dish",
                "description": "Delicious dish",
                "price": 25.0,
                "cooks": [self.cook1.id, self.cook2.id],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("dish_type", form.errors)


class DishSearchFormTest(TestCase):
    def test_empty_search(self):
        form = DishSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_valid_search(self):
        form = DishSearchForm(data={"name": "Pasta"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Pasta")


class DishTypeSearchFormTest(TestCase):
    def test_empty_search(self):
        form = DishTypeSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_valid_search(self):
        form = DishTypeSearchForm(data={"name": "Vegetarian"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Vegetarian")
