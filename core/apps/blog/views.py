from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article
from apps.accounts.models import Profile
from .forms import ArticleForm
from django.urls import reverse_lazy
from django.conf import settings
from django.views import View
from apps.comments.models import BlogComment
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# _______________________________________________________


def media_admin(request):
    """
    Function to receive media files inside templates
    """
    return {"media_url": settings.MEDIA_URL}


# _______________________________________________________


class IndexView(TemplateView):
    template_name = 'blog/index.html'


# _______________________________________________________


class ArticleListView(LoginRequiredMixin, ListView):
    """
    List of active posts by an author
    """

    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = '-published_date'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Article.objects.filter(is_active=True, author=profile)


# _______________________________________________________


class CreateArticleView(LoginRequiredMixin, CreateView):
    """
    Creating a post by the author logged in
    """

    template_name = 'blog/create_post.html'
    form_class = ArticleForm
    success_url = reverse_lazy('blog:post-list')
    model = Article

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        form.save()
        return super().form_valid(form)


# _______________________________________________________


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """
    Current post updated by logged in author
    """

    template_name = 'blog/update_post.html'
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blog:post-list')

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Article.objects.filter(is_active=True, author=profile)


# _______________________________________________________


class DeletePostView(LoginRequiredMixin, DeleteView):
    """
    Deleting the post by the author entered
    """

    template_name = 'blog/delete_post.html'
    model = Article
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post-list')

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Article.objects.filter(is_active=True, author=profile)


# _______________________________________________________


class PostDetailsView(DetailView):
    """
    Displaying the details of a post and registering comments for it, as well as displaying user comments
    """

    template_name = 'blog/blog_details.html'
    model = Article
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        comments = BlogComment.objects.filter(is_active=True, article=article).order_by(
            "-published_date"
        )

        context["comments"] = comments
        return context


# _______________________________________________________


class BlogView(View):
    """
    View List of active articles and sort by last article
    """

    template_name = 'blog/blog_list.html'

    def get(self, request, *args, **kwargs):
        """
        Caching the article data for 10 minutes
        """
        cache_key = "articles"
        data = cache.get(cache_key)
        if not data:
            posts = Article.objects.filter(is_active=True).order_by('-published_date')
            cache.set(cache_key, posts, timeout=10 * 60)
            data = posts
        return render(request, self.template_name, {"posts": data})


# _______________________________________________________


@receiver([post_save, post_delete], sender=Article)
def clear_product_cache(sender, **kwargs):
    """
    Deleting the cache of articles when it is created or deleted
    """
    cache.delete("articles")


# _______________________________________________________
