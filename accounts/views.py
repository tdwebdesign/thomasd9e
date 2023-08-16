# Python imports
import logging

# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views import View

# Local imports
from .models import CustomUser
from .forms import CustomUserCreationForm
from .tokens import account_activation_token

logger = logging.getLogger(__name__)


class RegisterView(View):
    """Handles user registration and sends an activation email."""

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Email confirmation logic
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "registration/activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return redirect(
                "email_confirmation_page"
            )  # Redirect to a page instructing the user to check their email

        return render(request, "registration/register.html", {"form": form})


class ActivateView(View):
    """Handles user account activation via email link."""

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
            logger.error(f"Error during account activation: {e}")
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("index")
        else:
            return render(request, "registration/activation_invalid.html")


class EmailConfirmationPageView(View):
    """Renders a page instructing the user to check their email for an activation link."""

    def get(self, request):
        return render(request, "registration/email_confirmation_page.html")


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("index")


# You can use the built-in views for password reset, just override the templates as needed
password_reset_done = PasswordResetDoneView.as_view()
password_reset_complete = PasswordResetCompleteView.as_view()


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy("index")


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy("index")
