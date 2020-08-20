from rest_framework import serializers

from apps.guides.serializers import TourGuideProfileSerializer
from apps.users.serializers import UserSerializer
from apps.utils.models import Language, Address
from apps.utils.serializers import (
    LanguageSerializer,
    AddressSerializer
)

from .models import (
    TourType,
    Tour,
    Attendee,
    PersonalTour,
)


class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = (
            'name',
            'slug',
        )


class TourSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    name = serializers.CharField(max_length=30)
    type = TourTypeSerializer(read_only=True)
    type_slug = serializers.SlugField(
        max_length=100, write_only=True, required=False)
    time = serializers.DateTimeField()
    guide = TourGuideProfileSerializer(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    languages_slugs = serializers.ListField(
        child=serializers.SlugField(max_length=100),
        required=False, write_only=True
    )
    description = serializers.CharField(max_length=1024, required=False)
    duration = serializers.DecimalField(
        max_digits=2, decimal_places=1, required=False)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=4, required=False)
    meeting_point = AddressSerializer(required=False)
    max_attendees = serializers.IntegerField(required=False)
    is_free = serializers.BooleanField(read_only=True)
    num_of_attendees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tour
        fields = (
            'uuid',
            'name',
            'type',
            'type_slug',
            'time',
            'guide',
            'languages',
            'languages_slugs',
            'description',
            'duration',
            'price',
            'meeting_point',
            'max_attendees',
            'num_of_attendees',
            'is_free',
        )

    def get_fields(self):
        fields = super(self.__class__, self).get_fields()

        if self.instance is None:
            fields['type_slug'] = serializers.SlugField(
                max_length=100, write_only=True, required=True)
            fields['languages_slugs'] = serializers.ListField(
                child=serializers.SlugField(max_length=100), write_only=True
            )

        return fields

    def validate_type_slug(self, ts):
        tour_type = TourType.objects.filter(slug=ts)

        if not tour_type.exists():
            raise serializers.ValidationError(
                'Tour type {} does not exist'.format(ts))

        return tour_type.first()

    def validate_languages_slugs(self, ls):
        languages = Language.objects.none()

        for langslug in ls:
            lang = Language.objects.filter(slug=langslug)

            if not lang.exists():
                raise serializers.ValidationError(
                    'Language {} does not exist'.format(langslug))

            languages |= lang

        return languages

    def create(self, validated_data):
        languages = validated_data.pop('languages_slugs', [])
        validated_data.update({'type': validated_data.pop('type_slug', None)})

        instance = self.Meta.model.objects.create(
            guide=self.context['guide'], **validated_data)

        for lang in languages:
            instance.languages.add(lang)

        return instance

    def update(self, instance, validated_data):
        languages = validated_data.pop('languages_slugs', [])
        validated_data.update({'type': validated_data.pop('type_slug', None)})

        update_fields = []

        for key in validated_data:
            setattr(instance, key, validated_data[key])
            update_fields.append(key)

        if len(update_fields) != 0:
            instance.save(update_fields=update_fields)

        if len(languages) != 0:
            instance.languages.clear()
            for lang in languages:
                instance.languages.add(lang)

        return instance


class AttendeeSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    tour = TourSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    paid = serializers.DateTimeField(read_only=True)
    refunded = serializers.DateTimeField(read_only=True)
    kicked_off = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Attendee
        fields = (
            'uuid',
            'paid',
            'refunded',
            'kicked_off',
            'tour',
            'user',
        )

    def to_representation(self, instance):
        rep = super(self.__class__, self).to_representation(instance)

        if 'payment_id' in self.context:
            rep['payment_id'] = self.context['payment_id']

        return rep
