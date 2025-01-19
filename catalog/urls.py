from django.urls import path
from .models import Cook, Dish, DishType
from .views import (
    index,
    CookListView,
    CookDetailView,
    DishListView,
    DishDetailView,
    DishTypeListView,
    toggle_assign_to_dish,
)


urlpatterns = [
    path("", index, name="index"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish/<int:pk>/toggle-assign/", toggle_assign_to_dish, name="toggle-dish-assign",
    ),
]

app_name = "catalog"
