from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .serializers import (
    RegisterationSerializer,
    ResendActivationSerializer,
    CustomTokenObtainPairSerializer,
    CustomAuthTokenSerializer,
    ChangePasswordSerilalizer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
    ProfileDetailsSerializer,
)
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from mail_templated import EmailMessage
from ...models import CustomUser, Profile
from rest_framework import generics
from rest_framework import status
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from rest_framework.views import APIView
from .permissions import IsAnonymousUser
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# _______________________________________________________


def get_tokens_for_user(user):
    """get jwt token for user by refresh token"""
    if not user.is_active:
        raise AuthenticationFailed("User is not active")
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


# _______________________________________________________


class RegisterationApiView(generics.GenericAPIView):
    """
    Register the user and send the account confirmation code to the email with api
    """

    permission_classes = [IsAnonymousUser]
    serializer_class = RegisterationSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.save()

            email = ser_data.validated_data["email"]
            user = get_object_or_404(CustomUser, email=email)
            token = get_tokens_for_user(user)

            message = EmailMessage(
                "email/activation_register.tpl",
                {"token": token, "user": user},
                "admin@gmail.com",
                to=[email],
            )

            message.send()

            data = {
                "email": email,
                "message": "registeration is successfully",
                "verificate_email": "link verify send to your email; checkuot",
            }

            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# _______________________________________________________


class ActivationApiView(APIView):
    """
    Receive the account confirmation link and extract the user from it and confirm the user's account
    """

    def get(self, request, token):
        try:
            token_obj = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token_obj.get("user_id")
            user = get_object_or_404(CustomUser, pk=user_id)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    data={
                        "details": "User activation has been successfully completed."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={"details": "The user has already been confirmed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ExpiredSignatureError:
            return Response({"details": "token is Expired"})

        except ExpiredSignatureError:
            return Response({"details": "token is not valid"})


# _______________________________________________________


class ResendActivationApiView(generics.GenericAPIView):
    """
    Resend the account confirmation code to email
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ResendActivationSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)

        user = ser_data.validated_data["user"]
        token = get_tokens_for_user(user)
        message = EmailMessage(
            "email/activation_register.tpl",
            {"token": token},
            "admin@gmail.com",
            to=[user.email],
        )
        message.send()

        return Response(data={"details": "User activation resend successfully."})


# _______________________________________________________


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# _______________________________________________________

# Basic Auth Token
# =================


class CustomAuthToken(ObtainAuthToken):
    """
    Get base auth token for the user
    """

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


# _______________________________________________________


class CustomDicardAthToken(APIView):
    """
    Deleting the base token user
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={"Logout: Token is Removed"}, status=status.HTTP_204_NO_CONTENT
        )


# _______________________________________________________


class ChangePasswordApiView(generics.GenericAPIView):
    """
    Change the user password when the user is inside the site profile
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerilalizer

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        if user.check_password(ser_data.validated_data['old_password']):
            user.set_password(ser_data.validated_data['new_password'])
            user.save()
            return Response(
                data={"details": "The new user password has been successfully changed"},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"details": "The current / previous password is incorrect"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# _______________________________________________________


class ResetPasswordApiView(generics.GenericAPIView):
    """
    Send the password reset link and recover the user's password
    """

    permission_classes = [IsAnonymousUser]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user = ser_data.validated_data["user"]
        token = get_tokens_for_user(user)
        message = EmailMessage(
            "email/resetpassword_user.tpl",
            {"token": token},
            "admin@gmail.com",
            to=[user.email],
        )
        message.send()

        return Response(
            data={"details": "The password reset link was sent to the email."}
        )


# _______________________________________________________


class ResetPasswordConfirmApiView(generics.GenericAPIView):
    """
    Logging into the user's password reset link and changing the password
    """

    serializer_class = ResetPasswordConfirmSerializer

    def put(self, request, token):
        try:
            token_obj = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token_obj.get("user_id")
            user = get_object_or_404(CustomUser, pk=user_id)
            ser_data = self.get_serializer(data=request.data)
            ser_data.is_valid(raise_exception=True)
            pass1 = ser_data.validated_data['new_password']
            if not user.check_password(pass1):
                user.set_password(pass1)
                user.save()
                return Response(
                    data={
                        "details": "The new password for the user has been successfully changed."
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={
                    "details": "This password has already been used for the user, select another password"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ExpiredSignatureError:
            return Response({"details": "The password reset link has expired."})

        except ExpiredSignatureError:
            return Response({"details": "The password reset link is invalid."})


# _______________________________________________________


class ProfileApiView(generics.RetrieveAPIView):
    """
    User profile and view information and fields
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileDetailsSerializer

    def get_object(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return profile


# _______________________________________________________
