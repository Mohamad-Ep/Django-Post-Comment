from django.urls import path, include
from apps.comments import views as views

# _______________________________________________________

app_name = 'comments'

urlpatterns = [
    path("blog_comment/<str:slug>/", views.blog_comment_partial, name='blog-comment'),
    # api-v1
    path("comments/api/v1/", include("apps.comments.api.v1.urls"), name='api-v1'),
]

# _______________________________________________________
