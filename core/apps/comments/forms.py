from django import forms
from django.utils.translation import gettext_lazy as _

# _______________________________________________________


class BlogCommentForm(forms.Form):
    fullname = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        max_length=128,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    text = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
    )

    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if fullname == "":
            raise forms.ValidationError(_("نام کامل نمیتواند خالی باشد"))
        if len(fullname) < 5:
            raise forms.ValidationError(_("نام کامل نمیتواند کوچکتر از 5 کاراکتر باشد"))
        return fullname

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == "":
            raise forms.ValidationError(_("متن نمیتواند خالی باشد"))
        if len(text) < 8:
            raise forms.ValidationError(_("متن نمیتواند کوچکتر از 8 کاراکتر باشد"))
        return text


# _______________________________________________________
