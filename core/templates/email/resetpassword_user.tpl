{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.email }}
{% endblock %}

{% block body %}
Reset Password Email
{% endblock %}

{% block html %}
    This is Reset Password Link: 

    <a href="http://127.0.0.1:8000/accounts/api/v1/reset-password/confirm/{{token}}/">بازیابی رمز عبور</a>
{% endblock %}