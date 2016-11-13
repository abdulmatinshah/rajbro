
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SaleOrder.as_view(), name='list'),
    url(r'^create_order/(?P<id>\d+)/$', views.create_order, name='create_order'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^test_form/$', views.test_form, name='test_form'),
    url(r'^gatepass/$', views.gatepass, name='gatepass'),
    url(r'^gatepass/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.gatepass, name='gatepass'),
]
