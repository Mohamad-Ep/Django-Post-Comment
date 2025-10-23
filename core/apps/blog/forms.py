from django import forms
from .models import Article,Category
# _______________________________________________________

class ArticleForm(forms.ModelForm):
    article_title = forms.CharField(max_length=100, required=True,
                                    widget=forms.TextInput(attrs={'class':'form-control'}))
    
    article_text = forms.CharField(max_length=1000, required=True,
                                    widget=forms.Textarea(attrs={'class':'form-control',"rows":"5"}))
    
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_active=True), required=True,
                                 widget=forms.Select(attrs={"class":"form-control"}))
    
    image_name = forms.ImageField(required=True,widget=forms.FileInput(attrs={"accept":".jpg,.jpeg,.png,.webp"}))
    
    slug = forms.SlugField(allow_unicode=True, required=True,
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Article
        fields = ['article_title','article_text','image_name','category','slug']
# _______________________________________________________