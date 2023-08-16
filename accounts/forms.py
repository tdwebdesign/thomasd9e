# Django imports
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate

# Local imports
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Username"})
    )

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username.lower(), password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"username": self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
