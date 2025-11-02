{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.email }}
{% endblock %}

{% block body %}
Activation Register Email
{% endblock %}

{% block html %}
    This is verification Link: 
    {% comment %} <a style="text-align:center;" target="_blank" href="{% url 'accounts:api-v1:activation' token %}">تایید حساب کاربری<a/> {% endcomment %}

    <a href="http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}/">تایید حساب</a>
{% endblock %}