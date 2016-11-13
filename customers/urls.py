
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Customer.as_view(), name='list'),
]
