
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SaleOrders.as_view(), name='list'),
    url(r'^by_date/$', views.SaleByDate.as_view(), name='sale_by_date'),
    url(r'^by_customer/$', views.SaleByCustomer.as_view(), name='sale_by_customer'),
    url(r'^create_order/(?P<id>\d+)/$', views.create_order, name='create_order'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^test_form/$', views.test_form, name='test_form'),
    url(r'^invoice/$', views.invoice, name='invoice'),
    url(r'^invoice/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.invoice, name='invoice'),
    url(r'^gatepass/$', views.gatepass, name='gatepass'),
    url(r'^gatepass/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.gatepass, name='gatepass'),
    url(r'^testgatepass/$', views.testgatepass, name='testgatepass'),
]
