from django.contrib import admin
from .models import BlogComment

# _______________________________________________________


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = (
        "fullname",
        "is_active",
        "published_date",
        "commenting_user",
        "article",
    )
    list_filter = ("commenting_user", "article")
    ordering = ("-published_date",)
    list_editable = ("is_active",)


# _______________________________________________________
