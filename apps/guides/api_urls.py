from django.conf.urls import url

from . import api as views


urlpatterns = [
    url(r'^$', views.TourGuidesProfilesView.as_view(), name='profiles'),
    url(r'^(?P<uuid>[0-9a-f]{32})/$',
        views.TourGuideProfileView.as_view(), name='profile'),
    url(r'^(?P<uuid>[0-9a-f]{32})/ratings/$',
        views.TourGuideRatingsView.as_view(), name='profile-ratings'),
    url(r'^ratings/(?P<uuid>[0-9a-f]{32})/$',
        views.TourGuideRatingView.as_view(), name='rating')
]
