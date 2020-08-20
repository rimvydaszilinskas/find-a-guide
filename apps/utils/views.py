from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tours.models import TourType
from apps.tours.serializers import TourTypeSerializer
from apps.users.serializers import UserSerializer
from apps.utils.models import Currency, Language, HashTag
from apps.utils.serializers import (
    CurrencySerializer,
    LanguageSerializer,
    HashTagSerializer,
)

from .permissions import ReadOnlyPermission


class PingView(APIView):
    permission_classes = [ReadOnlyPermission]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthenticationPingView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CurrenciesView(generics.ListAPIView):
    serializer_class = CurrencySerializer
    permission_classes = [ReadOnlyPermission]

    def get_queryset(self):
        return Currency.objects.all()


class LanguagesView(generics.ListAPIView):
    serializer_class = LanguageSerializer
    permission_classes = [ReadOnlyPermission]

    def get_queryset(self):
        return Language.objects.all()


class HashTagsView(generics.ListCreateAPIView):
    serializer_class = HashTagSerializer
    permission_classes = [ReadOnlyPermission]

    def filter_queryset(self, queryset):
        slug = self.request.GET.get('slug', '')

        return queryset.filter(slug__icontains=slug)

    def get_queryset(self):
        return HashTag.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class TourTypesView(generics.ListAPIView):
    serializer_class = TourTypeSerializer
    permission_classes = [ReadOnlyPermission]

    def get_queryset(self):
        return TourType.objects.all()


class StripePublicKeyView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response({
            'publickKey': settings.STRIPE_PUBLISHABLE_KEY
        })
