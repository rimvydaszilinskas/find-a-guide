from rest_framework import serializers

from django.db.models import Q

from apps.tours.models import TourType, Tour, PersonalTour
from apps.users.serializers import UserSerializer
from apps.utils.models import Language
from apps.utils.serializers import LanguageSerializer

from .models import (
    TourGuideProfile,
    TourGuideRating,
    PersonalGuideRequest
)


class TourGuideProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    user = UserSerializer(read_only=True)
    tour_types = serializers.SerializerMethodField()
    tour_types_slugs = serializers.ListField(
        child=serializers.SlugField(max_length=100),
        required=False, write_only=True
    )
    languages = LanguageSerializer(many=True, read_only=True)
    languages_slugs = serializers.ListField(
        child=serializers.SlugField(max_length=100),
        required=False, write_only=True
    )
    price = serializers.DecimalField(
        max_digits=7, decimal_places=4, required=False)
    active = serializers.BooleanField(required=False)
    country = serializers.CharField(max_length=50, required=False)
    town = serializers.CharField(max_length=100, required=False)
    intro = serializers.CharField(max_length=1024, required=False)
    is_approved = serializers.BooleanField(read_only=True)
    total_ratings = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = TourGuideProfile
        fields = (
            'uuid',
            'user',
            'tour_types',
            'tour_types_slugs',
            'languages',
            'languages_slugs',
            'price',
            'active',
            'country',
            'town',
            'intro',
            'is_approved',
            'total_ratings',
            'rating',
        )

    def get_tour_types(self, obj):
        from apps.tours.serializers import TourTypeSerializer
        return TourTypeSerializer(obj.tour_types.all(), many=True).data

    def get_fields(self):
        fields = super(self.__class__, self).get_fields()

        if self.instance is None:
            fields['tour_types_slugs'] = serializers.ListField(
                child=serializers.SlugField(max_length=100),
                required=True, write_only=True
            )
            fields['languages_slugs'] = serializers.ListField(
                child=serializers.SlugField(max_length=100), write_only=True
            )
            fields['price'] = serializers.DecimalField(
                max_digits=7, decimal_places=4, required=True, write_only=True
            )

        return fields

    def validate_languages_slugs(self, slugs):
        languages = Language.objects.none()

        for slug in slugs:
            lang = Language.objects.filter(slug=slug)

            if not lang.exists():
                raise serializers.ValidationError(
                    'Language {} does not exist'.format(slug))

            languages |= lang

        return languages

    def validate_tour_types_slugs(self, slugs):
        tps = Language.objects.none()

        for slug in slugs:
            tp = TourType.objects.filter(slug=slug)

            if not tp.exists():
                raise serializers.ValidationError(
                    'Language {} does not exist'.format(slug))

            tps |= tp

        return tps

    def validate_price(self, price):
        if self.context['user'].currency:
            return price / self.context['user'].currency.exchange_rate
        return price

    def create(self, validated_data):
        tour_types = validated_data.pop('tour_types_slugs', [])
        langs = validated_data.pop(['languages_slugs', []])

        instance = self.Meta.model.objects.create(
            **validated_data, **self.context)

        for tp in tour_types:
            instance.tour_types.add(tp)

        for lang in langs:
            instance.languages.add(lang)

        return langs

    def update(self, instance, validated_data):
        tour_types = validated_data.pop('tour_types_slugs', None)
        langs = validated_data.pop('languages_slugs', None)

        update_fields = []

        for key in validated_data:
            setattr(instance, key, validated_data[key])
            update_fields.append(key)

        if len(update_fields) != 0:
            instance.save(update_fields=update_fields)

        if tour_types is not None:
            instance.tour_types.clear()

            for tp in tour_types:
                instance.tour_types.add(tp)

        if langs is not None:
            instance.languages.clear()

            for lang in langs:
                instance.languages.add(lang)

        return instance


class TourGuideRatingSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    guide = TourGuideProfileSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=True)
    review = serializers.CharField(max_length=1024, required=False)
    personal_tour_uuid = serializers.UUIDField(
        format='hex', write_only=True, required=False)
    tour_uuid = serializers.UUIDField(
        format='hex', write_only=True, required=False)

    class Meta:
        model = TourGuideRating
        fields = (
            'uuid',
            'guide',
            'created_at',
            'user',
            'rating',
            'review',
            'personal_tour_uuid',
            'tour_uuid',
        )

    def get_fields(self):
        fields = super(self.__class__, self).get_fields()

        if self.instance is not None:
            del fields['personal_tour_uuid']
            del fields['tour_uuid']

        return fields

    def validate_personal_tour_uuid(self, uuid):
        tour = PersonalTour.objects.filter(guide=self.context['guide']).filter(
            Q(purchaser=self.context['user']) | Q(users=self.context['user']))

        if not tour.exists():
            raise serializers.ValidationError(
                'Personal tour({}) does not exist'.format(uuid.hex))
        return tour.first()

    def validate_tour_uuid(self, uuid):
        tour = Tour.objects.filter(
            guide=self.context['guide'], attendees__user=self.context['user'], attendees__paid=True, attendees__refunded__isnull=True)

        if not tour.exists():
            raise serializers.ValidationError(
                'Personal tour({}) does not exist'.format(uuid.hex))
        return tour.first()

    def validate(self, attrs):
        if TourGuideRating.objects.filter(user=self.context['user'], guide=self.context['guide'], personal_tour=self.validated_data.get('personal_tour_uuid', None), tour=self.validated_data.get('tour_uuid', None)).exists():
            raise serializers.ValidationError(
                'A rating from the user already exists')

        attrs.update({
            'personal_tour': self.validated_data.pop('personal_tour_uuid', None),
            'tour': self.validated_data.pop('tour_uuid', None)
        })

        return attrs

    def create(self, validated_data):
        return TourGuideProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        update_fields = []

        for key in validated_data:
            setattr(instance, key, validated_data[key])
            update_fields.append(key)

        if len(update_fields) != 0:
            instance.save(update_fields=update_fields)
        return instance
