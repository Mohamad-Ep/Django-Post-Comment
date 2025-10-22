from django.urls import path,include
from apps.accounts.api.v1 import views as views
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView
# _______________________________________________________

app_name = 'api-v1'

urlpatterns = [
    # registeration
    path('register/', views.RegisterationApiView.as_view(), name='register'),
    # verification
    path('activation/confirm/<str:token>/',views.ActivationApiView.as_view(),name='activation'),
    path('activation/resend/',views.ResendActivationApiView.as_view(),name='activation-resend'),
    # jwt-token
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    # base token
    path('token/login/', views.CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDicardAthToken.as_view(), name='token-logout'),
    # change-password
    path('change-password/',views.ChangePasswordApiView.as_view(),name='change-password'),
    # reset-password
    path('reset-password/', views.ResetPasswordApiView.as_view(), name='reset-password'),
    path('reset-password/confirm/<str:token>/',views.ResetPasswordConfirmApiView.as_view(),name='reset-password-confirm'),
    # profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    
]

# _______________________________________________________