from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, DeleteView
from .models import User
from .filters import UserFilter
from django.core.paginator import Paginator

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Registration for {username} was successful!")
            return redirect("drinks-home")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", { "form": form, "title": "Register" })


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your account has been successfully updated!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = { "user_form": user_form, "profile_form": profile_form, "title": "Profile" }

    return render(request, "users/profile.html", context)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users/users.html"
    context_object_name = 'user_profiles'
    ordering = ['username']
    paginate_by = 30
    filterset_class = UserFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.user_profiles = self.filterset_class(self.request.GET, queryset=queryset)
        return self.user_profiles.qs.distinct()

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List of Users"
        context['form'] = self.user_profiles.form
        context['paginator'] = Paginator(self.user_profiles.qs, self.paginate_by)
        context['page_obj'] = context['paginator'].get_page(self.request.GET.get("page"))
        return context


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = 'user_profile'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        return context


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    context_object_name = 'user_profile'
    template_name = "users/user_confirm_delete.html"
    success_url = "/users/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        if self.request.user.id == self.object.id:
            messages.success(self.request, f"Your account has been deleted!")
            return redirect("drinks-home")
        else:
            messages.success(self.request, f"User has been deleted!")
            return redirect(self.get_success_url())
    
    def test_func(self):
        return self.request.user.id == self.get_object().id or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete User"
        context['user_id'] = self.get_object().id
        return context


class UserLoginView(LoginView):
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Logout"
        return context


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reset Password"
        return context


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reset Password Done"
        return context


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reset Password Confirmation"
        return context


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reset Password Complete"
        return context
