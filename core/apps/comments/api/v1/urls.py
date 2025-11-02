from django.urls import path, include
from apps.comments.api.v1 import views as views
from rest_framework.routers import DefaultRouter

# _______________________________________________________

app_name = 'api-v1'

router = DefaultRouter()
router.register("comment-list", views.CommentBlogListApiView, basename="comment-list")
urlpatterns = router.urls

# _______________________________________________________
