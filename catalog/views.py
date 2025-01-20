from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from catalog.models import Cook, Dish, DishType


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class CookListView(LoginRequiredMixin, ListView):
    model = Cook
    paginate_by = 5
    template_name = "catalog/cook_list.html"


class CookDetailView(LoginRequiredMixin, DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")
    template_name = "catalog/cook_detail.html"

class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 5
    template_name = "catalog/dish_list.html"


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = "catalog/dish_detail.html"


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    paginate_by = 5
    template_name = "catalog/dish_type_list.html"


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    if (
        Dish.objects.get(id=pk) in cook.dishes.all()
    ):
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("catalog:dish-detail", args=[pk]))
