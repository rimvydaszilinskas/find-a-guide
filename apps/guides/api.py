from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response

from apps.api.permissions import ReadOnlyPermission

from .models import TourGuideProfile, TourGuideRating
from .permissions import PublicPreviewPrivateEditPermission
from .serializers import TourGuideProfileSerializer, TourGuideRatingSerializer


class TourGuidesProfilesView(generics.ListCreateAPIView):
    permission_classes = [ReadOnlyPermission]
    serializer_class = TourGuideProfileSerializer

    def get_queryset(self):
        return TourGuideProfile.objects.filter(approved__isnull=False, active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class TourGuideProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [PublicPreviewPrivateEditPermission]
    serializer_class = TourGuideProfileSerializer

    def get_object(self):
        return get_object_or_404(TourGuideProfile,
                                 approved__isnull=False, uuid=self.kwargs['uuid'])

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        self.check_object_permissions(request, profile)

        serializer = self.serializer_class(
            instance=profile, data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        self.check_object_permissions(request, profile)

        profile.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TourGuideRatingsView(generics.ListCreateAPIView):
    serializer_class = TourGuideRatingSerializer
    permission_classes = [ReadOnlyPermission]

    def get_tour_guide(self):
        return get_object_or_404(TourGuideProfile, uuid=self.kwargs['uuid'], approved__isnull=False)

    def get_serializer_context(self):
        return {
            'user': self.request.user,
            'guide': self.get_tour_guide()
        }

    def get_queryset(self):
        return self.get_tour_guide().ratings.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class TourGuideRatingView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [PublicPreviewPrivateEditPermission]
    serializer_class = TourGuideRatingSerializer

    def get_object(self):
        return get_object_or_404(TourGuideRating, uuid=self.kwargs['uuid'])

    def update(self, request, *args, **kwargs):
        rating = self.get_object()
        self.check_object_permissions(request, rating)

        serializer = self.serializer_class(
            instance=rating, data=request.data, context={
                'user': request.user,
                'guide': rating.guide
            })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        rating = self.get_object()
        self.check_object_permissions(request, rating)
        rating.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
