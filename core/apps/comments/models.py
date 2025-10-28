from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
# _______________________________________________________

class BlogComment(models.Model):
    fullname = models.CharField(max_length=50,verbose_name=_("نام کامل"))
    comment_text = models.TextField(verbose_name=_("متن کامنت"))
    is_active = models.BooleanField(default=False,verbose_name=_("فعال/غیرفعال"))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_("تاریخ ایجاد"))
    published_date = models.DateTimeField(default=datetime.now,verbose_name=_("تاریخ انتشار"))
    commenting_user = models.ForeignKey("accounts.Profile", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    article = models.ForeignKey("blog.Article", verbose_name=_("مقاله"), on_delete=models.CASCADE)
        
    def __str__(self):
        return self.fullname
    
    class Meta:
        verbose_name = "کامنت مقاله"
        verbose_name_plural = "کامنت های مقالات"
# _______________________________________________________
