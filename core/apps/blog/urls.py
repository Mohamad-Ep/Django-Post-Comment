from django.urls import path,include
from apps.blog import views as views
# _______________________________________________________

app_name = 'blog'

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),

]

# _______________________________________________________