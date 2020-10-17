from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Drink, Ingredient, Recipe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import date, timedelta
from .filters import DrinkFilter, IngredientFilter
from django.core.paginator import Paginator

# Returns a drink using modular exponentation on today's date.
# Then the number is divided again so that it can access an item in the keys list.
# The value obtained from the list is used to retrieve the drink.
def getDrinkOfTheDay(drink_keys):
    # Perform modular exponentation on today's date, then reduce it to number_of_drinks
    index = pow(
        int(date.today().strftime("%Y%m%d")), 
        3540034045828155908745054744418277834243309928115463377391493476491109069681,
        72437346919515671440505456097276374932311092479844125795754094155925023764307
    ) % drink_keys.count()

    # Return the drink with the key at the calculated index
    return Drink.objects.get(pk=drink_keys[index])


# The home page generates a drink's data as long from a list of drinks made
# prior to today. If none are available, then no drink data is displayed.
def home(request):
    # Get the range of dates from October 1, 2020 to the day before today.
    # No drinks were saved prior to October 1, 2020
    start_date = date(2020, 1, 1).strftime("%Y-%m-%d")
    end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Using the date range, filter out the drinks made today and save the total
    drink_keys = Drink.objects.filter(
        Datestamp__range=[start_date, end_date]
    ).order_by("pk").values_list("pk", flat=True)

    # If the number of drinks made before today is over 1, then pick a drink
    if drink_keys:
        # Users that are logged in will get a "drink of the day" displayed.
        # Those that aren't logged in will receive the first drink in the list
        if request.user.is_authenticated:
            drink = getDrinkOfTheDay(drink_keys)
        else:
            drink = Drink.objects.first()

        # Save the page title as well as the drink and recipe data
        context = { 
          "title": "Home" , 
          "drink": drink,
          "recipe": Recipe.objects.filter(Drink=drink).order_by("Ingredient")
        }
    else:
        # Save only the title of the page
        context = { "title": "Home" }
    return render(request, "drinks/home.html", context)


def about(request):
    return render(request, "drinks/about.html", { "title": "About" })


class DrinkListView(LoginRequiredMixin, ListView):
    model = Drink
    template_name = "drinks/drinks.html"
    context_object_name = 'drinks'
    ordering = ['Name']
    paginate_by = 30
    filterset_class = DrinkFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.drinks = self.filterset_class(self.request.GET, queryset=queryset)
        return self.drinks.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List of Drinks"
        context['form'] = self.drinks.form
        context['paginator'] = Paginator(self.drinks.qs, self.paginate_by)
        context['page_obj'] = context['paginator'].get_page(self.request.GET.get("page"))
        return context


class DrinkDetailView(LoginRequiredMixin, DetailView):
    model = Drink
    context_object_name = 'drink'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        context["recipe"] = Recipe.objects.filter(Drink=self.object).order_by("Ingredient")
        return context


class DrinkCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Drink
    fields = ["Name", "Type"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, f"Drink has been created!")
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Drink"
        return context    


class DrinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Drink
    fields = ["Name", "Type"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, f"Drink has been updated!")
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Drink"
        return context


class DrinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Drink
    context_object_name = 'drink'
    success_url = "/drinks/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, f"Drink has been deleted!")
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Drink"
        return context


class IngredientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ingredient
    template_name = "drinks/ingredients.html"
    context_object_name = 'ingredients'
    ordering = ['Name']
    paginate_by = 30
    filterset_class = IngredientFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.ingredients = self.filterset_class(self.request.GET, queryset=queryset)
        return self.ingredients.qs.distinct()

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List of Ingredients"
        context['form'] = self.ingredients.form
        context['paginator'] = Paginator(self.ingredients.qs, self.paginate_by)
        context['page_obj'] = context['paginator'].get_page(self.request.GET.get("page"))
        return context


class IngredientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ingredient
    context_object_name = 'ingredient'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        return context


class IngredientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ingredient
    fields =  ["Name", "Alcohol"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, f"Ingredient has been created!")
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Ingredient"
        return context


class IngredientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ingredient
    fields = ["Name", "Alcohol"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        drinks = list(set([item.Drink for item in Recipe.objects.filter(Ingredient=self.object)]))
        if self.object.Alcohol:
            for drink in drinks:
                drink.Alcohol = True
                drink.save()
        else:
            for drink in drinks:
                has_alcohol = any(
                    [item.Ingredient.Alcohol for item in Recipe.objects.filter(Drink=drink)]
                )
                drink.Alcohol = has_alcohol
                drink.save()
        messages.success(self.request, f"Ingredient has been updated!")
        return redirect(self.get_success_url())
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Ingredient"
        return context


class IngredientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ingredient
    context_object_name = 'ingredient'
    success_url = "/ingredients/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        drinks = list(set([item.Drink for item in Recipe.objects.filter(Ingredient=self.object)]))
        self.object.delete()
        for drink in drinks:
            has_alcohol = any(
                [item.Ingredient.Alcohol for item in Recipe.objects.filter(Drink=drink)]
            )
            drink.Alcohol = has_alcohol
            drink.save()
        messages.success(self.request, f"Ingredient has been deleted!")
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Ingredient"
        return context


class RecipeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Recipe
    fields =  ["Ingredient", "Quantity", "Measurement"]
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.Drink = Drink.objects.get(pk=self.kwargs['drink_id'])
        self.object.save()
        if self.object.Ingredient.Alcohol:
            drink = self.object.Drink
            drink.Alcohol = True
            drink.save()
        messages.success(self.request, f"Recipe item has been created!")
        return redirect(self.get_success_url())
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Recipe"
        context['drink'] = Drink.objects.get(pk=self.kwargs['drink_id'])
        return context


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields =  ["Ingredient", "Quantity", "Measurement"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        drink = self.object.Drink
        drink.Alcohol = any(
            [item.Ingredient.Alcohol for item in Recipe.objects.filter(Drink=drink)]
        )
        drink.save()
        messages.success(self.request, f"Recipe item has been updated!")
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Recipe"
        context['drink'] = Drink.objects.get(pk=self.kwargs['drink_id'])
        return context


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    context_object_name = 'recipe'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        drink = self.object.Drink
        success_url = f"/drinks/{drink.pk}/"
        self.object.delete()
        has_alcohol = any(
            [item.Ingredient.Alcohol for item in Recipe.objects.filter(Drink=drink)]
        )
        drink.Alcohol = has_alcohol
        drink.save()
        messages.success(self.request, f"Recipe item has been deleted!")
        return redirect(success_url)

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Recipe"
        return context
