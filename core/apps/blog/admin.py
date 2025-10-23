from django.contrib import admin
from .models import Article,Category
from django.db.models import Q,Count
# _______________________________________________________

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title','is_active','created_date','published_date','slug','author','category')
    ordering = ('published_date',)
    list_filter = ('article_title',)
    list_editable = ('is_active',)
    search_fields = ('article_title',)
    
admin.site.register(Article,ArticleAdmin)
# _______________________________________________________

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title','created_date','is_active','count_articles')
    list_editable = ('is_active',)
    list_filter = ('category_title',)
    search_fields = ('category_title',)
    
    def get_queryset(self,*args, **kwargs):
        queryset = super(CategoryAdmin, self).get_queryset(*args, **kwargs)
        queryset = queryset.annotate(count_articles=Count('articles'))
        return queryset
    
    def count_articles(self,obj):
        return obj.count_articles
    
admin.site.register(Category,CategoryAdmin)
# _______________________________________________________

