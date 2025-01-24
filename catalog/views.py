from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)

from catalog.forms import (
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
    CookExperienceUpdateForm,
    DishForm,
)
from catalog.models import Cook, Dish, DishType


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.only("id").count()
    num_dishes = Dish.objects.only("id").count()
    num_dish_types = DishType.objects.only("id").count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)

@method_decorator(login_required, name="dispatch")
class CookListView(ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = Cook.objects.only(
            "id", "username", "first_name", "last_name", "years_of_experience"
        )
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return (queryset.
                    filter(username__icontains=form.
                           cleaned_data["username"]))
        return queryset


@method_decorator(login_required, name="dispatch")
class CookDetailView(DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")
    template_name = "catalog/cook_detail.html"


@method_decorator(login_required, name="dispatch")
class CookCreateView(CreateView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("catalog:cook-list")


@method_decorator(login_required, name="dispatch")
class CookExperienceUpdateView(UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("catalog:cook-list")


@method_decorator(login_required, name="dispatch")
class CookDeleteView(DeleteView):
    model = Cook
    success_url = reverse_lazy("catalog:cook-list")


@method_decorator(login_required, name="dispatch")
class DishListView(ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type").all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


@method_decorator(login_required, name="dispatch")
class DishDetailView(DetailView):
    model = Dish
    template_name = "catalog/dish_detail.html"

    def get_queryset(self):
        return (Dish.objects.
                prefetch_related("cooks").select_related("dish_type"))


@method_decorator(login_required, name="dispatch")
class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("catalog:dish-list")


@method_decorator(login_required, name="dispatch")
class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("catalog:dish-list")


@method_decorator(login_required, name="dispatch")
class DishDeleteView(DeleteView):
    model = Dish
    success_url = reverse_lazy("catalog:dish-list")


@method_decorator(login_required, name="dispatch")
class DishTypeListView(ListView):
    model = DishType
    paginate_by = 5
    template_name = "catalog/dish_type_list.html"

    def get_context_data(self, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = DishType.objects.only("name")
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


@method_decorator(login_required, name="dispatch")
class DishTypeCreateView(CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("catalog:dish-type-list")
    template_name = "catalog/dish_type_form.html"


class DishesByTypeView(ListView):
    model = Dish
    template_name = "catalog/dishes_by_type.html"
    context_object_name = "dishes"

    def get_queryset(self):
        self.dish_type = get_object_or_404(DishType, pk=self.kwargs["pk"])
        return Dish.objects.filter(dish_type=self.dish_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish_type"] = self.dish_type
        return context


@method_decorator(login_required, name="dispatch")
class DishTypeUpdateView(UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("catalog:dish-type-list")
    template_name = "catalog/dish_type_form.html"


@method_decorator(login_required, name="dispatch")
class DishTypeDeleteView(DeleteView):
    model = DishType
    success_url = reverse_lazy("catalog:dish-type-list")
    template_name = "catalog/dish_type_confirm_delete.html"


@login_required
def toggle_assign_to_dish(request, pk):
    cook = request.user
    dish = get_object_or_404(Dish, pk=pk)

    if cook.dishes.filter(id=dish.id).exists():
        cook.dishes.remove(dish)
        messages.success(request, "Cook removed from dish.")
    else:
        cook.dishes.add(dish)
        messages.success(request, "Cook assigned to dish.")
    return redirect("catalog:dish-detail", pk=pk)


def logout_view(request):
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)
