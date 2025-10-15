import os
import uuid
import requests
import json
import random

from pathlib import Path
from django.conf import settings
from django.contrib import admin
from django.urls import path,include,re_path,reverse,resolve
from urllib.parse import urlencode
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.shortcuts import render,redirect,get_object_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMultiAlternatives
from mail_templated import EmailMessage,send_mail
from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory,formset_factory
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.apps import AppConfig
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q,Count,Min,Max,Avg,Sum,F,ExpressionWrapper,IntegerField,Value,Case,When
from django.db.models.functions import Coalesce
from django.http import (Http404,HttpRequest,HttpResponse,HttpResponseBadRequest,JsonResponse,
                         HttpResponseForbidden,HttpResponseNotFound,HttpResponseRedirect,HttpResponsePermanentRedirect,
                         HttpResponseServerError)
from django.core.paginator import Paginator
from datetime import datetime
import django_filters
from django.utils.translation import gettext_lazy as _

# jwt - token
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer,TokenVerifySerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views as auth_view
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

# signals
from django.dispatch import receiver
from django.db.models.signals import post_migrate,post_save,pre_save,pre_delete

# Tests
from django.test import TestCase,SimpleTestCase,Client
import pytest
from rest_framework.test import APIClient

# Class Base View
from django.views import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView,TemplateView
from django.utils.html import html_safe,mark_safe

from django_extensions.db.fields import AutoSlugField
from django.utils.text import slugify
from django.contrib.admin import SimpleListFilter
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core import validators

# Permissions
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

# DRF
from rest_framework import serializers
from django.core import serializers as serializers_core
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.permissions import BasePermission,SAFE_METHODS

from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.generics import (GenericAPIView,ListAPIView,ListCreateAPIView,RetrieveAPIView,
                                     RetrieveDestroyAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters import rest_framework as filters
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import pagination


# Feke data
from faker import Faker
from django.core.management.base import BaseCommand

# Load Testing
from locust import HttpUser, task, between

# Background Process
from celery import Celery,shared_task
from celery.schedules import crontab

# Redis - Caching
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# drf_yasg - swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
