from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.ToursView.as_view(), name='tours'),
    url(r'^(?P<uuid>[0-9a-f]{32})/attendees/$',
        views.TourAttendeesView.as_view(), name='tour-attendees'),
]
