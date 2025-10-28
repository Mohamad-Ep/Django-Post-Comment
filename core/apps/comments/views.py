from django.shortcuts import render,get_object_or_404,redirect
from .forms import BlogCommentForm
from apps.blog.models import Article
from apps.accounts.models import Profile
from django.contrib import messages
from .models import BlogComment
# _______________________________________________________

def blog_comment_partial(request,slug):
    article = get_object_or_404(Article,slug=slug)
    profile = get_object_or_404(Profile,user=request.user)
    
    if request.method == "GET":
        initial_form = {
            "fullname":"".join([f'{profile.name} {profile.family}' if profile.name and profile.family else '']),
            "email":profile.user.email
            }        
        form = BlogCommentForm(initial=initial_form)
        context = {
            "form":form,
            "article_slug":article.slug
        }
        return render(request,'comments/partials/blog_comment_partial.html',context)
    
    if request.method == "POST":
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            BlogComment.objects.create(
                fullname = data['fullname'],
                comment_text = data['text'],
                commenting_user = profile,
                article = article
            )
            messages.success(request,'نظر شما برای این مقاله ثبت شد')
            return redirect('blog:posts')
        else:
            for errros in form.errors.values():
                for error in errros:
                    messages.error(request,error)
            return redirect('blog:post-details',slug=article.slug)
# _______________________________________________________
