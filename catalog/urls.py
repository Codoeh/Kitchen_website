from django.urls import path
from .models import Cook, Dish, DishType
from .views import (
    index,
    CookListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("cook/", CookListView.as_view(), name="cook-list"),
]

app_name = "catalog"
