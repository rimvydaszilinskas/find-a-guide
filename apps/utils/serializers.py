from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict

from .models import Currency, Language, HashTag, Address


class UncachedModelSerializer(serializers.ModelSerializer):
    @property
    def fields(self):
        # override fields here without caching to return objects after creation instead of uuids
        fields = BindingDict(self)
        for key, value in self.get_fields().items():
            if value is None:
                continue
            fields[key] = value

        return fields


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'name',
            'slug',
            'sign',
            'exchange_rate',
            'updated_at',
        )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'name',
            'slug',
        )


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = (
            'slug',
        )

    def validate_slug(self, slug):
        hashtag = HashTag.objects.filter(slug=slug)

        if hashtag.exists():
            raise serializers.ValidationError('Hashtag already exists')

        return slug

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
