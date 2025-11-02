from django.urls import path, include
from apps.blog.api.v1 import views as views

# _______________________________________________________

app_name = 'api-v1'

urlpatterns = [
    path("posts/", views.PostListApiView.as_view(), name='posts'),
    path("posts/<str:slug>/", views.PostDetailsApiView.as_view(), name='post_details'),
]
# _______________________________________________________
