from rest_framework import serializers

from apps.utils.serializers import LanguageSerializer

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    username = serializers.CharField(required=False, max_length=30)
    email = serializers.EmailField(required=True)
    timezone = serializers.CharField(max_length=50, required=False)
    currency = serializers.SlugField(source='currency.slug', required=False)

    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'email',
            'timezone',
            'currency',
        )
