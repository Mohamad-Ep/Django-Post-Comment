from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
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
# _______________________________________________________

def media_admin(request):
    return {"media_url":settings.MEDIA_URL}
# _______________________________________________________

class IndexView(TemplateView):
    template_name = 'blog/index.html'
# _______________________________________________________

class ArticleListView(LoginRequiredMixin,ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = '-published_date'
    
    def get_queryset(self):
        profile = get_object_or_404(Profile,user=self.request.user)
        return Article.objects.filter(is_active=True,author=profile)
    
# _______________________________________________________

class CreateArticleView(LoginRequiredMixin,CreateView):
    template_name = 'blog/create_post.html'
    form_class = ArticleForm
    success_url = reverse_lazy('blog:post-list')
    model = Article
    
    def form_valid(self, form):
        profile = get_object_or_404(Profile,user=self.request.user)
        form.instance.author = profile
        form.save()
        return super().form_valid(form)
    
# _______________________________________________________

class UpdatePostView(LoginRequiredMixin,UpdateView):
    template_name = 'blog/update_post.html'
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blog:post-list')

    def get_queryset(self):
        profile = get_object_or_404(Profile,user=self.request.user)
        return Article.objects.filter(is_active=True,author=profile)
# _______________________________________________________

class DeletePostView(LoginRequiredMixin,DeleteView):
    template_name = 'blog/delete_post.html'
    model = Article
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post-list')

    def get_queryset(self):
        profile = get_object_or_404(Profile,user=self.request.user)
        return Article.objects.filter(is_active=True,author=profile)      
# _______________________________________________________

class PostDetailsView(DetailView):
    template_name = 'blog/blog_details.html'
    model = Article
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article,slug=self.kwargs['slug'])
        comments = BlogComment.objects.filter(is_active=True,article=article)\
            .order_by("-published_date")
        
        context["comments"] = comments
        return context    
# _______________________________________________________

class BlogView(View):
    template_name = 'blog/blog_list.html'
    def get(self,request,*args, **kwargs):
        posts = Article.objects.filter(is_active=True).order_by('-published_date')
        return render(request,self.template_name,{"posts":posts})
# _______________________________________________________
