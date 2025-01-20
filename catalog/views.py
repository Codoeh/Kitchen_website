from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from catalog.forms import CookSearchForm, DishSearchForm, DishTypeSearchForm, CookExperienceUpdateForm, DishForm
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

    def get_context_data(self, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.
                                   cleaned_data["username"])
        return queryset


class CookDetailView(LoginRequiredMixin, DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")
    template_name = "catalog/cook_detail.html"


class CookCreateView(LoginRequiredMixin, CreateView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("catalog:cook-list")


class CookExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("catalog:cook-list")


class CookDeleteView(LoginRequiredMixin, DeleteView):
    model = Cook
    success_url = reverse_lazy("catalog:cook-list")


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.
                                   cleaned_data["name"])
        return queryset


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = "catalog/dish_detail.html"


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("catalog:dish-list")


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("catalog:dish-list")


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy("catalog:dish-list")


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.
                                   cleaned_data["name"])
        return queryset


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("catalog:dish-type-list")
    template_name = "catalog/dish_type_form.html"


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
