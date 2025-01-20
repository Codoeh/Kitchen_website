from django.urls import path
from .views import (
    index,
    CookListView,
    CookDetailView,
    CookCreateView,
    CookExperienceUpdateView,
    CookDeleteView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishTypeListView,
    toggle_assign_to_dish,
)


urlpatterns = [
    path("", index, name="index"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cook/create/", CookCreateView.as_view(), name="cook-create"),
    path("cook/<int:pk>/update/", CookExperienceUpdateView.as_view(), name="cook-update"),
    path("cook/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish/<int:pk>/toggle-assign/", toggle_assign_to_dish, name="toggle-dish-assign",
    ),
]

app_name = "catalog"
