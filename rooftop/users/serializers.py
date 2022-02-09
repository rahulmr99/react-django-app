import re

from rest_framework import serializers
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    ValidationError,
    Serializer,
    ImageField,
)
from rest_framework.serializers import ModelSerializer

from users.models import User

from users.utils import get_tokens_for_user


class UserCreateSerializer(ModelSerializer):
    """
    User Register serializer
    """
    email = EmailField(label='Email Address')
    password = CharField(write_only=True)
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
        ]

    def validate_email(self, value):
        email = value.lower().strip()

        user_qs = User.objects.filter(email=email)

        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_password(self, value):
        data = self.get_initial()
        password1 = value
        password2 = data.get('confirm_password')
        if password1 != password2:
            raise ValidationError('Passwords Must Match')
        if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*()_+\.])[\w\d~!@#$%^&*()_+\.]{6,}$", password1):
            raise ValidationError(
                'Your password has to be at least 6 characters long.'
                ' Must contain at least one lower case letter, '
                'one upper case letter, one digit. at least one special character'
                ' ~!@#$%^&*()_+.')
        return value

    def create(self, validated_data):
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        email = validated_data.get('email', None)
        user_obj = User(
            first_name=first_name,
            last_name=last_name,
            email=email.lower().strip(),
            username=email.lower().strip(),
            is_active=True,
            type=2
        )
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    """
    User Login Serializer
    """
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {"password": {"write_only": True},
                        }

    def to_representation(self, instance):
        data = super(UserLoginSerializer, self).to_representation(instance)
        user = User.objects.get(id=instance.get('id'))
        data.update({"first_name": user.first_name, "last_name": user.last_name, 'type': user.type})
        return data


    def validate(self, data):
        email = data.get("email", None)
        password = data["password"]
        if not email or not password:
            raise ValidationError("Email and password required")
        email = email.lower().strip()
        user = User.objects.filter(email=email).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('There is no user registered with %s' % email)
        if user_obj:
            if user_obj.password == '':
                raise ValidationError('You have not verified your account. Please verify it before login')
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credentials. Please try again')

        response_token = get_tokens_for_user(user_obj)
        data['token'] = response_token.get('access', None)
        data['id'] = user_obj.id
        return data