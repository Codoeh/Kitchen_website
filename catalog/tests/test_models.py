from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.models import Dish, DishType


class ModelTests(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create(
            username="testuser",
            first_name="first",
            last_name="last",
            years_of_experience=5,
        )
        self.dish_type = DishType.objects.create(
            name="testdish_type",
        )
        self.dish = Dish.objects.create(
            name="testdish",
            description="test_description",
            price=100,
            dish_type=self.dish_type,
        )
        self.dish.cooks.add(self.cook)

    def test_cook_str(self):
        self.assertEqual(str(self.cook), "testuser (first last)")

    def test_dish_str(self):
        self.assertEqual(str(self.dish), "testdish")

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), "testdish_type")

    def test_years_of_experience_default_value(self):
        self.cook = get_user_model().objects.create(
            username="testuser2",
            first_name="first",
            last_name="last",
        )
        self.assertEqual(str(self.cook.years_of_experience), "0")

    def test_price_less_than_zero(self):
        self.dish = Dish.objects.create(
            name="testdish2",
            description="test_description",
            price=-100,
            dish_type=self.dish_type,
        )
        with self.assertRaises(ValidationError):
            self.dish.full_clean()

    def test_create_dish_with_missing_name(self):
        self.dish = Dish.objects.create(
            description="test_description",
            price=100,
            dish_type=self.dish_type,
        )
        with self.assertRaises(ValidationError):
            self.dish.full_clean()

    def test_create_dish_with_missing_description(self):
        self.dish = Dish.objects.create(
            name="testdish3",
            price=100,
            dish_type=self.dish_type,
        )
        with self.assertRaises(ValidationError):
            self.dish.full_clean()

    def test_create_dish_with_missing_dish_type(self):
        self.dish = Dish(
            name="testdish4",
            description="test_description",
            price=100,
            dish_type=None,
        )
        with self.assertRaises(ValidationError):
            self.dish.full_clean()

    def test_create_dish_with_missing_dish_price(self):
        self.dish = Dish(
            name="testdish5",
            description="test_description",
            dish_type=self.dish_type,
        )
        with self.assertRaises(ValidationError):
            self.dish.full_clean()
