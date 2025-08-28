
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from catalog.forms import StyleFormMixin
from .models import CustomUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Ваш пароль"
        self.fields["password2"].label = "Повторите пароль"

        self.fields["password1"].help_text = (
            "- Ваш пароль не должен быть слишком похож на другую личную информацию.<br>"
            "- Ваш пароль должен содержать как минимум 8 символов.<br>"
            "- Ваш пароль не должен быть распространённым.<br>"
            "- Ваш пароль не должен состоять только из цифр.")

        self.fields["password2"].help_text = "Введите тот же пароль для подтверждения."


class CustomUserUpdateForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["avatar", "country"]
