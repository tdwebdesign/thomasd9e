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

from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
)  # Assuming you'll create a custom form for registration
from .tokens import (
    account_activation_token,
)  # You'll need to create this for email confirmation


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User will be inactive until email confirmation
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

            # Log the user in
            login(request, user)
            return redirect("home")  # Redirect to home or any other page

        return render(request, "registration/register.html", {"form": form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("home")
        else:
            return render(request, "registration/activation_invalid.html")


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("home")


# You can use the built-in views for password reset, just override the templates as needed
password_reset_done = PasswordResetDoneView.as_view()
password_reset_complete = PasswordResetCompleteView.as_view()
login = LoginView.as_view()
logout = LogoutView.as_view()

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
