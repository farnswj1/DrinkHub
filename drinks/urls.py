from django.urls import path
from .views import (
    home,
    about,
    DrinkListView, 
    DrinkDetailView, 
    DrinkCreateView, 
    DrinkUpdateView,
    DrinkDeleteView,
    IngredientListView,
    IngredientDetailView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView
)

urlpatterns = [
    path('', home, name="drinks-home"),
    path('about/', about, name="drinks-about"),
    path('drinks/', DrinkListView.as_view(), name="drinks-list"),
    path('drinks/new/', DrinkCreateView.as_view(), name="drink-create"),
    path('drinks/<int:pk>/', DrinkDetailView.as_view(), name="drink-detail"),
    path('drinks/<int:pk>/update/', DrinkUpdateView.as_view(), name="drink-update"),
    path('drinks/<int:pk>/delete/', DrinkDeleteView.as_view(), name="drink-delete"),
    path('ingredients/', IngredientListView.as_view(), name="ingredients-list"),
    path('ingredients/new/', IngredientCreateView.as_view(), name="ingredient-create"),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name="ingredient-detail"),
    path('ingredients/<int:pk>/update', IngredientUpdateView.as_view(), name="ingredient-update"),
    path('ingredients/<int:pk>/delete', IngredientDeleteView.as_view(), name="ingredient-delete"),
    path('drinks/<int:drink_id>/recipes/new/', RecipeCreateView.as_view(), name="recipe-create"),
    path(
        'drinks/<int:drink_id>/recipes/<int:pk>/update/',
        RecipeUpdateView.as_view(),
        name="recipe-update"
    ),
    path(
        'drinks/<int:drink_id>/recipes/<int:pk>/delete/',
        RecipeDeleteView.as_view(),
        name="recipe-delete"
    ),
]