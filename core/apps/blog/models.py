from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import os
from utils import get_random_code
from django.dispatch import receiver
from django.db.models.signals import pre_delete
# _______________________________________________________

class Category(models.Model):
    category_title = models.CharField(max_length=100,verbose_name=_("عنوان دسته"))
    summary_description = models.CharField(max_length=200,null=True,blank=True,verbose_name=_("توضیحات"))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_("تاریخ ایجاد"))
    is_active = models.BooleanField(default=True,verbose_name=_("فعال/غیرفعال"))
    
    def __str__(self):
        return self.category_title
    
    class Meta:
        verbose_name = "دسته بندی مقاله"
        verbose_name_plural = "دسته بندی مقاله ها"
# _______________________________________________________

def upload_image_article(instance,filename):
    file,exe = os.path.splitext(filename)
    file_name = f'images/blog/article/{file}{get_random_code(5)}{exe}'
    return file_name

class Article(models.Model):
    article_title = models.CharField(max_length=100,verbose_name=_("عنوان مقاله"))
    article_text = models.TextField(null=True,blank=True,verbose_name=_("متن مقاله"))
    is_active = models.BooleanField(default=True,verbose_name=_("فعال/غیرفعال"))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_("تاریخ ایجاد"))
    updated_date = models.DateTimeField(auto_now=True,verbose_name=_("تاریخ ویرایش"))
    published_date = models.DateTimeField(default=datetime.now,verbose_name=_("تاریخ انتشار"))
    slug = models.SlugField(max_length=500,null=True,blank=True,allow_unicode=True) 
    image_name = models.ImageField(upload_to=upload_image_article, verbose_name=_("عکس مقاله"))
    author = models.ForeignKey("accounts.Profile", verbose_name=_("نویسنده"), on_delete=models.CASCADE,related_name="articles")
    category = models.ForeignKey(Category, verbose_name=_("دسته بندی"), on_delete=models.CASCADE,related_name="articles")
        
    def __str__(self):
        return self.article_title
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"
# _______________________________________________________

@receiver(pre_delete, sender=Article)
def delete_article_images(sender, instance, **kwargs):
    """ Remove image_name field before delete article object"""
    if instance.image_name and os.path.isfile(instance.image_name.path):
        os.remove(instance.image_name.path)
# _______________________________________________________
