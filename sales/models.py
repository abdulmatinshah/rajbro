from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from customers.models import Customer
from products.models import Product
from django.conf import settings
from django.urls import reverse
from rajbro.mixins import ToBoxMixin

from django.db.models import F



class Sale(models.Model):
    customer = models.ForeignKey(Customer)
    # sales_rep = models.ForeignKey(settings.AUTH_USER_MODEL)
    sales_rep = models.ForeignKey(User)
    sale_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    # post_items = models.BooleanField(default=False)

    def save(self):
        self.amount = self.sale_line_items.aggregate(linetotal=models.Sum('linetotal'))['linetotal']
        if not self.amount:
            self.amount = 0
        super().save()

    def __str__(self):
        return 'Sale No. {} (Amount Rs.{})'.format(self.id, self.amount)

    def get_absolute_url(self):
        return reverse('sales:create_order', kwargs={'id': self.id})


class SaleLineItem(models.Model):
    sale_order = models.ForeignKey(Sale, related_name='sale_line_items')
    product = models.ForeignKey(Product, related_name='sale_line_items')
    quantity = models.PositiveIntegerField()
    free_pieces = models.PositiveIntegerField(null=True, blank=True)
    quantity_returned = models.PositiveIntegerField(null=True, blank=True)
    linetotal = models.DecimalField(max_digits=100, decimal_places=2, help_text='Rs.', blank=True)
    stale = models.PositiveIntegerField(null=True, blank=True)
    posted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.quantity is None:
            self.quantity = 0
        if self.free_pieces is None:
            self.free_pieces = 0
        if self.quantity_returned is None:
            self.quantity_returned = 0
        print(self.quantity_returned,'qrtnd')
        diff = 0
        if self.id:
            obj = SaleLineItem.objects.get(id=self.id)

            if obj.quantity is None:
                obj.quantity = 0
            if obj.free_pieces is None:
                obj.free_pieces = 0
            if obj.quantity_returned is None:
                obj.quantity_returned = 0

            prev_line_item_qty = (obj.quantity + obj.free_pieces) - obj.quantity_returned
            current_line_item_qty = (self.quantity + self.free_pieces) - self.quantity_returned

            if prev_line_item_qty != current_line_item_qty:
                diff = current_line_item_qty - prev_line_item_qty
        else:
            diff = (self.quantity + self.free_pieces) - self.quantity_returned
        super().save(*args, **kwargs)
        self.product.units_in_stock = F('units_in_stock') - diff
        self.product.save()

    def __str__(self):
        return 'SaleLineItem {}'.format(self.id)

    @property
    def to_box(self):
        boxes, pieces = divmod(self.quantity, self.product.quantity_per_unit)
        return '{},{}'.format(boxes, pieces)

    @property
    def returned_to_box(self):
        boxes, pieces = divmod(self.quantity_returned, self.product.quantity_per_unit)
        return '{},{}'.format(boxes, pieces)

    def to_quantity_from_box(self, value, prod):
        # value=(2,3), prod=1

        if hasattr(self, 'product'):
            self._multiplier = self.product.quantity_per_unit
        else:
            from products.models import Product
            product = Product.objects.get(id=prod)
            self._multiplier = product.quantity_per_unit

        p, b = 0, 0
        new_list = value.split(',')
        try:
            b = int(new_list[0])
            p = int(new_list[1])
        except ValueError:
            pass
        except IndexError:
            pass
        total_pieces = b * self._multiplier + p

        self.quantity = total_pieces

    @property
    def returned(self):
        boxes, pieces = divmod(self.quantity_returned, self.product.quantity_per_unit)
        return '{},{}'.format(boxes, pieces)

    def to_quantity_returned_from_box(self, value, prod):
        # value=(2,3), prod=1

        if hasattr(self, 'product'):
            self._multiplier = self.product.quantity_per_unit
        else:
            from products.models import Product
            product = Product.objects.get(id=prod)
            self._multiplier = product.quantity_per_unit

        p, b = 0, 0
        new_list = value.split(',')
        try:
            b = int(new_list[0])
            p = int(new_list[1])
        except ValueError:
            pass
        except IndexError:
            pass
        total_pieces = b * self._multiplier + p

        self.quantity_returned = total_pieces


from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=SaleLineItem)
def update_linetotal(sender, instance, *args, **kwargs):
    if instance.quantity_returned:
        instance.linetotal = (instance.quantity - instance.quantity_returned) * instance.product.sale_rate
    else:
        instance.linetotal = instance.quantity * instance.product.sale_rate
