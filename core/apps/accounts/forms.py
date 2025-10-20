from django import forms
import re
# ________________________________________________

class RegisterUserForm(forms.Form):
    email = forms.EmailField(
        label='',
        required=True,
        max_length=128,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل"}
        ),
    )
    password1 = forms.CharField(
        label='',
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور"}
        ),
    )
    password2 = forms.CharField(
        label='',
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "تکرار رمز عبور"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email) < 10:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل کمتر از حد مجاز است')
        return email

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('رمز عبور و تکرار آن برابر نمی باشد')

        if len(pass2) < 8:
            raise forms.ValidationError('رمز عبور نباید کمتر از 8 کاراکتر باشد')

        if not re.findall(r'[a-z]', pass2):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')

        if not re.findall(r'[A-Z]', pass2):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد')

        if not re.findall(r'[@#$%!^&*]', pass2):
            raise forms.ValidationError(
                'رمز عبور باید حداقل یک کاراکتر خاص داشته باشد (@#$%!^&*)'
            )

        return pass2
# ________________________________________________

class LoginUserForm(forms.Form):
    email = forms.EmailField(
        label='',
        required=True,
        max_length=128,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل"}
        ),
    )
    password = forms.CharField(
        label='',
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email) < 10:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل کمتر از حد مجاز است')
        return email

    def clean_password(self):
        pass1 = self.cleaned_data.get("password")

        if len(pass1) < 8:
            raise forms.ValidationError('رمز عبور نباید کمتر از 8 کاراکتر باشد')

        return pass1
# ________________________________________________
