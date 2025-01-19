from django.urls import path
from .models import Cook, Dish, DishType
from .views import (
    index,
    CookListView,
    DishListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("dish/", DishListView.as_view(), name="dish-list"),
]

app_name = "catalog"
