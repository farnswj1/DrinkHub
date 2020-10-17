from django.urls import path
from .views import(
    register,
    profile,
    UserLoginView,
    UserLogoutView,
    UserListView,
    UserDetailView,
    UserDeleteView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView
)

urlpatterns = [
    path('register/', register, name="register"),
    path('profile/', profile, name="profile"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('users/', UserListView.as_view(), name="users-list"),
    path('users/<int:pk>/', UserDetailView.as_view(), name="user-detail"),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name="user-delete"),
    path('password/reset/', UserPasswordResetView.as_view(), name="password_reset"),
    path(
        'password/reset/done/', 
        UserPasswordResetDoneView.as_view(), 
        name="password_reset_done"
    ),
    path(
        'password/reset/confirm/<uidb64>/<token>/', 
        UserPasswordResetConfirmView.as_view(), 
        name="password_reset_confirm"
    ),
    path(
        'password/reset/complete/', 
        UserPasswordResetCompleteView.as_view(), 
        name="password_reset_complete"
    ),
]