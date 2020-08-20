import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from apps.guides.models import TourGuideProfile

from .models import Tour, Attendee
from .serializers import TourSerializer, AttendeeSerializer


class ToursView(generics.ListAPIView):
    serializer_class = TourSerializer

    def get_queryset(self):
        return Tour.objects.filter(time__gte=timezone.now())


class GuideToursView(generics.ListCreateAPIView):
    serializer_class = TourSerializer

    def get_queryset(self):
        guide = get_object_or_404(TourGuideProfile, uuid=self.kwargs['uuid'])
        return guide.tours.filter(time__gte=timezone.now())


class TourAttendeesView(generics.ListCreateAPIView):
    serializer_class = AttendeeSerializer

    def get_queryset(self):
        tour = get_object_or_404(Tour, uuid=self.kwargs['uuid'])
        return tour.attendees.filter(kicked_off__isnull=True)

    def create(self, request, *args, **kwargs):
        tour = get_object_or_404(
            Tour, uuid=self.kwargs['uuid'], time__gt=timezone.now())

        if tour.attendees.filter(user=request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'User is already attending'})

        attendee = Attendee.objects.create(user=request.user, tour=tour)

        if tour.is_free:
            return Response(status=status.HTTP_201_CREATED, data=self.serializer_class(attendee).data)

        intent = stripe.PaymentIntent.create(
            api_key=settings.STRIPE_SECRET_KEY,
            amount=int(tour.price),
            currency='eur'
        )

        return Response(status=status.HTTP_201_CREATED, data=self.serializer_class(attendee, context={'payment_id': intent['client_secret']}).data)
