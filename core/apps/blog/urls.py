from django.urls import path,include
from apps.blog import views as views
# _______________________________________________________

app_name = 'blog'

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("post-list/", views.ArticleListView.as_view(), name='post-list'),
    path("create-post/", views.CreateArticleView.as_view(), name='create-post'),
    path("update-post/<str:slug>/", views.UpdatePostView.as_view(), name='update-post'),
    path("delete-post/<str:slug>/", views.DeletePostView.as_view(), name='delete-post'),
    path("blog/", views.BlogView.as_view(), name='posts'),
    path("blog/<str:slug>/", views.PostDetailsView.as_view(), name='post-details'),
    # api-v1
    path("blog/api/v1/", include("apps.blog.api.v1.urls"), name='api-v1'),
]

# _______________________________________________________