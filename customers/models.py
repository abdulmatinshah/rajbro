from django.conf import settings
from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13, null=True, blank=True)
    address = models.CharField(max_length=180, null=True, blank=True, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Supplier(Vendor):
    pass


class Customer(Vendor):
    sales_rep = models.ForeignKey(settings.AUTH_USER_MODEL)
    route_tag = models.CharField(max_length=10, null=False, unique=True)
