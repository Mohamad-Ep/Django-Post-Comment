from django.shortcuts import render
from django.views.generic.base import TemplateView
# _______________________________________________________

class IndexView(TemplateView):
    template_name = 'blog/index.html'
# _______________________________________________________
