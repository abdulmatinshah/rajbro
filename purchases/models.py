from django.db import models
from django.shortcuts import reverse
from products.models import Product


class PurchaseOrder(models.Model):
    purchase_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, help_text='Rs.', default=0)
    post_items = models.BooleanField(default=False)

    class Meta:
        ordering = ['post_items', 'purchase_date']

    def save(self):
        self.amount = self.line_items.aggregate(subtotal=models.Sum('subtotal'))['subtotal']
        if not self.amount:
            self.amount = 0
        super().save()

    def __str__(self):
        return str(self.purchase_date)

    def get_absolute_url(self):
        return reverse('purchases:edit_order', kwargs={'id': self.id})


    @property
    def order_total(self):
        return 'Rs. %.2f' % self.amount


# ============= LINEITEM ===================
class LineItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='line_items')
    product = models.ForeignKey(Product, related_name='line_items')
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=100, decimal_places=2, help_text='Rs.', blank=True)
    # quantity_returned = models.PositiveIntegerField(null=True, blank=True)
    posted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.purchase_order.purchase_date)

    @property
    def to_box(self):
        boxes, pieces = divmod(self.quantity, self.product.quantity_per_unit)
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



    # def _get_calculated_linetotal(self):
    #     return self.quantity * self.product.sale_rate
    #
    # calculated_subtotal = property(_get_calculated_linetotal)

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=LineItem)
def update_subtotal(sender, instance, *args, **kwargs):
    instance.subtotal = instance.quantity * instance.product.sale_rate
#
#
# @receiver(pre_save, sender=PurchaseOrder)
# def populate_amount(sender, instance, *args, **kwargs):
#     if not instance.amount:
#         instance.amount = 0