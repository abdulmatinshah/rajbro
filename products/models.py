from django.db import models
from rajbro.mixins import ConvertUnitMixin
from customers.models import Supplier


class Product(ConvertUnitMixin, models.Model):
    supplier = models.ForeignKey(Supplier, related_name='products', default=1)
    name = models.CharField(max_length=20)
    weight = models.PositiveIntegerField(default=0, help_text='gram')
    purchase_rate = models.DecimalField(max_digits=100, decimal_places=2, help_text='Rs.')
    sale_rate = models.DecimalField(max_digits=100, decimal_places=2, help_text='Rs.')
    quantity_per_unit = models.PositiveIntegerField(default=1, help_text='No.')
    units_in_stock = models.IntegerField(default=0, help_text='No.')
    discontinued = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def box_units(self):
        boxes, pieces = divmod(self.units_in_stock, self.quantity_per_unit)
        return '%s,%s (%s)' %(boxes, pieces, self.units_in_stock)


from purchases.models import PurchaseOrder
from sales.models import Sale
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=PurchaseOrder)
def update_purchase_product_quantity(sender, instance, **kwargs):
    if instance.post_items:
        items = instance.line_items.all()
        for item in items:
            if not item.posted:
                item.posted = True
                item.save()
                item.product.units_in_stock += item.quantity
                item.product.save()
    else:
        items = instance.line_items.all()
        for item in items:
            if item.posted:
                item.posted = False
                item.save()
                item.product.units_in_stock -= item.quantity
                item.product.save()


@receiver(post_save, sender=Sale)
def update_sale_product_quantity(sender, instance, created=False, **kwargs):
    # print('prodct tick... %s---created: %s', sender, created)
    # from django.db.models import Sum
    # total = instance.sale_line_items.aggregate(Sum('quantity'))
    # print(total['quantity__sum'])

    items = instance.sale_line_items.all()
    if instance.post_items:
        for item in items:
            if not item.posted:
                item.posted = True
                item.save()
                net_quantity = (item.quantity + item.free_pieces) - item.quantity_returned
                item.product.units_in_stock -= net_quantity

                item.product.save()
    else:
        for item in items:
            if item.posted:
                item.posted = False
                item.save()
                item.product.units_in_stock += item.quantity
                item.product.save()

