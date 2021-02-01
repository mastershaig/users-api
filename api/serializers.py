from abc import ABC

from django.core.exceptions import ValidationError

from users.models import Users
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', 'iso-8601'], required=True)

    class Meta:
        model = Users
        fields = (
            'first_name',
            'last_name',
            'email',
            'birthday',
        )


