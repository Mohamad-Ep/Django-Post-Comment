import pytest
from rest_framework.test import APIClient
from apps.accounts.models import CustomUser,Profile
from django.urls import reverse
from apps.blog.models import Category,Article
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
import shutil
from django.test import override_settings
from unittest.mock import patch
# _______________________________________________________

@pytest.fixture
def api_client():
    client = APIClient()
    return client
# ----------------------------------
@pytest.fixture(autouse=True) # این autouse=True برای همه توابع تست فعال
def temp_media_root(tmp_path):
    temp_dir = tmp_path / "media"
    temp_dir.mkdir()
    with override_settings(MEDIA_ROOT=temp_dir):
        yield
    shutil.rmtree(temp_dir, ignore_errors=True)
# ----------------------------------
@pytest.fixture
def fake_image():
    with open("media/images/test/test_image.jpg", "rb") as f:
        fake_file = SimpleUploadedFile("test_image.jpg", f.read(), content_type="image/jpeg")
    return fake_file
# ----------------------------------
@pytest.fixture
def user_client():
    user = CustomUser.objects.create_user(
        email = "testmail@gmail.com",
        password = "Aa123456789@",
        is_active = True,
        is_verified = True,
    )
    return user

# ----------------------------------
@pytest.fixture
def article(user_client,fake_image):
    category = Category.objects.create(category_title="test category")
    profile = get_object_or_404(Profile,user=user_client)
    article = Article.objects.create(
        article_title = "test article",
        article_text = "test text",
        category = category,
        is_active = True,
        slug = "slug-article",
        image_name = fake_image,
        author = profile
    )
    
    return article
# ----------------------------------

@pytest.mark.django_db
class TestBlogApiView:
    def test_get_posts_api_response_200(self,api_client):
        url = reverse("blog:api-v1:posts")
        response = api_client.get(url)
        assert response.status_code == 200
    
    def test_create_post_api_response_201(self,api_client,user_client,fake_image):
        url = reverse("blog:api-v1:posts")
        api_client.force_authenticate(user=user_client)
        category = Category.objects.create(category_title="test category")
        
        data = {
            "article_title":"test article",
            "article_text":"test text",
            "image_name":fake_image,
            "category":category.pk,
            "is_active":True,
            "slug":"slug-article"
        }
        response = api_client.post(url,data,format='multipart')
        print(response.data)
        assert response.status_code == 201
        
    def test_get_post_details_api_response_200(self,api_client,user_client,article):
        url = reverse("blog:api-v1:post_details",kwargs={"slug":article.slug})
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_partial_update_post_details_api_response_ok(self,api_client,article,user_client):
        url = reverse("blog:api-v1:post_details",kwargs={"slug":article.slug})
        api_client.force_authenticate(user_client)
        data ={
            "article_title":"article7",
        }
        response = api_client.patch(url,data)
        assert response.status_code == 200
# _______________________________________________________