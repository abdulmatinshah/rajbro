"""rajbro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from dashboard import views
from accounts.views import login_view, logout_view

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='home'),
    # url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^purchases/', include('purchases.urls', namespace='purchases')),
    url(r'^sales/', include('sales.urls', namespace='sales')),
    url(r'^customers/', include('customers.urls', namespace='customers')),
    url(r'^admin/', admin.site.urls),
    # url(r'^login/$', login_view, name='login'),
    # url(r'^logout/$', logout_view, name='logout'),
    # url(r'^$', home)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)