
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Purchases.as_view(), name='list'),
    url(r'^order/(?P<pk>\d+)$', views.PurchaseDetail.as_view(), name='detail'),
    url(r'^order/(?P<pk>\d+)/delete/$', views.PurchaseDelete.as_view(), name='delete_order'),
    url(r'^order/$', views.purchase_order, name='order'),
    url(r'^order/(?P<id>\d+)/$', views.edit_purchase_order, name='edit_order'),
    url(r'^order/(?P<id>\d+)/post_items/$', views.post_items, name='post_items'),
    url(r'^order/(?P<id>\d+)/unpost_items/$', views.unpost_items, name='unpost_items'),
    url(r'^(?P<posting_type>post|unpost)/$', views.posting, name='posting'),
]
