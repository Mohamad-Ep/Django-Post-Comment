import pytest
from apps.accounts.models import CustomUser,Profile
from apps.blog.models import Category,Article
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
import shutil
from django.test import override_settings
# _______________________________________________________

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
@pytest.mark.django_db
class TestBlogModel:
    def test_create_article_response_ok(self,user_client,fake_image):
        profile = get_object_or_404(Profile,user=user_client)
        category = Category.objects.create(category_title='category1')
        article = Article.objects.create(
            article_title = "article1",
            article_text = "article text",
            slug = "artcile-slug",
            author = profile,
            category =category,
            image_name = fake_image            
        )
        
        assert article.article_title == "article1"
        assert article.is_active
# _______________________________________________________