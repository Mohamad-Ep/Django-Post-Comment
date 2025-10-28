from rest_framework import serializers
from ...models import CustomUser, Profile
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer

# _______________________________________________________


class RegisterationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "re_password"]

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password != re_password:
            raise serializers.ValidationError(
                'The password is not the same as the re_password'
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                'The password should not be less than 8 characters'
            )

        if not re.findall(r'[a-z]', password):
            raise serializers.ValidationError(
                'The password must have at least one small letter'
            )

        if not re.findall(r'[A-Z]', password):
            raise serializers.ValidationError(
                'The password must have at least one capital letter'
            )

        if not re.findall(r'[@#$%!^&*]', password):
            raise serializers.ValidationError(
                'Password must have at least one specific character (@#$%!^&*)'
            )
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("re_password", None)
        return CustomUser.objects.create_user(**validated_data)


# _______________________________________________________


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = CustomUser.objects.get(email=email)
            if user_obj.is_verified:
                raise serializers.ValidationError(
                    {"details": "The user has already been confirmed"}
                )

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "email dos not exits"})

        attrs["user"] = user_obj

        return super().validate(attrs)


# _______________________________________________________


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not Verficated"})
        data["email"] = self.user.email
        data["user_id"] = self.user.id
        return data


# _______________________________________________________


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                msg = _('User is not Verified')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


# _______________________________________________________


class ChangePasswordSerilalizer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, label=_("old_password"))
    new_password = serializers.CharField(write_only=True, label=_("new_password"))
    re_password = serializers.CharField(write_only=True, label=_("re_password"))

    def validate(self, attrs):
        password = attrs.get("new_password")
        re_password = attrs.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(
                'The password is not the same as the re_password'
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                'The password should not be less than 8 characters'
            )

        if not re.findall(r'[a-z]', password):
            raise serializers.ValidationError(
                'The password must have at least one small letter'
            )

        if not re.findall(r'[A-Z]', password):
            raise serializers.ValidationError(
                'The password must have at least one capital letter'
            )

        if not re.findall(r'[@#$%!^&*]', password):
            raise serializers.ValidationError(
                'Password must have at least one specific character (@#$%!^&*)'
            )

        return super().validate(attrs)


# _______________________________________________________


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = CustomUser.objects.get(email=email)
            if not user_obj.is_active or not user_obj.is_verified:
                raise serializers.ValidationError(
                    {"details": "The user is not active or verified"}
                )

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "There is no user with this email."}
            )

        attrs["user"] = user_obj

        return super().validate(attrs)


# _______________________________________________________


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, label=_("new_password"))
    re_password = serializers.CharField(write_only=True, label=_("re_password"))

    def validate(self, attrs):
        password = attrs.get("new_password")
        re_password = attrs.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(
                'The password is not the same as the re_password'
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                'The password should not be less than 8 characters'
            )

        if not re.findall(r'[a-z]', password):
            raise serializers.ValidationError(
                'The password must have at least one small letter'
            )

        if not re.findall(r'[A-Z]', password):
            raise serializers.ValidationError(
                'The password must have at least one capital letter'
            )

        if not re.findall(r'[@#$%!^&*]', password):
            raise serializers.ValidationError(
                'Password must have at least one specific character (@#$%!^&*)'
            )

        return super().validate(attrs)


# _______________________________________________________


class ProfileDetailsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True, source='user.email')

    class Meta:
        model = Profile
        fields = '__all__'


# _______________________________________________________
