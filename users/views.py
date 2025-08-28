import secrets
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from config.settings import DEFAULT_FROM_EMAIL
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Приветствуем вас на нашем сайте Перейдите по ссылке для подтверждения эл. почты {url}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserChangeView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "registration/edit_profile.html"

    context_object_name = "form"

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Ваш профиль был успешно обновлён")
        return redirect("users:edit-profile")

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка при обновлении профиля")
        return self.render_to_response(self.get_context_data(form=form))


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
