from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.PingView.as_view(), name='ping'),
    url(r'^auth/$', views.AuthenticationPingView.as_view(), name='auth-ping'),

    url(r'^stripe/key/$', views.StripePublicKeyView.as_view(), name='stripe-key'),

    url(r'^currencies/$', views.CurrenciesView.as_view(), name='currencies'),
    url(r'^languages/$', views.LanguagesView.as_view(), name='languages'),
    url(r'^hashtags/$', views.HashTagsView.as_view(), name='hashtags'),
    url(r'^tourtypes/$', views.TourTypesView.as_view(), name='tourtypes'),

]
