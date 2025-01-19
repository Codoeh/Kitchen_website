from django.urls import path
from .models import Cook, Dish, DishType
from .views import (
    index,
    CookListView,
    CookDetailView,
    DishListView,
    DishTypeListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
]

app_name = "catalog"
