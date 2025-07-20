from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_counter += 1
        if obj.views_counter == 20 and not obj.notified:
            send_mail(
                subject='Поздравляем! Статья просмотрена 20 раз',
                message=f'Ваша статья "{obj.title}" была просмотрена 20 раз!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            obj.notified = True
        obj.save(update_fields=['views_counter', 'notified'])
        return obj


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:posts_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:posts_list')
