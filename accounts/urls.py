from django.urls import path
from . import views

app_name = "accounts"  # Namespace for this app

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>/", views.ActivateView.as_view(), name="activate"),
    path(
        "change-password/",
        views.CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
    # Default Django names for password reset URLs
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path("password_reset/done/", views.password_reset_done, name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("reset/done/", views.password_reset_complete, name="password_reset_complete"),
    path(
        "email-confirmation/",
        views.EmailConfirmationPageView.as_view(),
        name="email_confirmation_page",
    ),
    path(
        "resend-activation-email/",
        views.ResendActivationEmailView.as_view(),
        name="resend_activation_email",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
