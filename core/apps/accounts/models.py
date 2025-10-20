from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _

# _______________________________________________________

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_kwargs):
        if not email:
            raise ValueError(_("The email field cannot be empty."))
        
        user = self.model(email=self.normalize_email(email),**extra_kwargs)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**extra_kwargs):
        extra_kwargs.setdefault("is_active",True)
        extra_kwargs.setdefault("is_admin",True)
        extra_kwargs.setdefault("is_superuser",True)
        
        if extra_kwargs.get("is_active") is not True:
            raise ValueError(_("The is_active field must be enabled"))
        if extra_kwargs.get("is_admin") is not True:
            raise ValueError(_("The is_admin field must be enabled"))
        if extra_kwargs.get("is_superuser") is not True:
            raise ValueError(_("The is_superuser field must be enabled"))
        
        return self.create_user(email,password,**extra_kwargs)
# _______________________________________________________

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.CharField(max_length=128,unique=True,verbose_name=_('ایمیل'))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_('تاریخ ایجاد'))
    updated_date = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ ایجاد'))
    is_active = models.BooleanField(default=False,verbose_name=_('فعال/غیرفعال'))
    is_admin = models.BooleanField(default=False,verbose_name=_('کاربر/ادمین'))
    is_verified = models.BooleanField(default=False,verbose_name=_('تاییدشده/تایید نشده'))
    
    def __str__(self):
        return self.email
    
    def is_staff(self):
        return self.is_admin
    
    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربران")
# _______________________________________________________

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name=_("کاربر"), on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,verbose_name=_("نام"))
    family = models.CharField(max_length=70,null=True,verbose_name=_("فامیلی"))
    mobile_number = models.CharField(max_length=11,null=True,blank=True,unique=True,verbose_name=_("شماره موبایل"))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_('تاریخ ایجاد'))
    updated_date = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ ایجاد'))
    image_name = models.ImageField(upload_to="images/profiles/", null=True,blank=True,verbose_name=_("عکس پروفایل"))
    GENDER_CHOICES = [
        ("man","مرد"),
        ("women","زن")
    ]
    gender = models.CharField(choices=GENDER_CHOICES,default="Unknown", max_length=50,verbose_name=_("جنسیت"))
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"
# _______________________________________________________
