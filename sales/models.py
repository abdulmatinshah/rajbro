from django.db import models
from customers.models import Customer
from products.models import Product
from django.conf import settings
from django.urls import reverse
from rajbro.mixins import ToBoxMixin


class Sale(models.Model):
    customer = models.ForeignKey(Customer, related_name='sales')
    sales_rep = models.ForeignKey(settings.AUTH_USER_MODEL)
    sale_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    post_items = models.BooleanField(default=False)

    class Meta:
        ordering = ['customer']

    def save(self):
        self.amount = self.sale_line_items.aggregate(linetotal=models.Sum('linetotal'))['linetotal']
        if not self.amount:
            self.amount = 0
        super().save()

    def __str__(self):
        return 'Order No. {} (Amount Rs.{})'.format(self.id, self.amount)

    def get_absolute_url(self):
        return reverse('sales:create_order', kwargs={'id': self.id})


class SaleLineItem(ToBoxMixin, models.Model):
    sale_order = models.ForeignKey(Sale, related_name='sale_line_items')
    product = models.ForeignKey(Product, related_name='sale_line_items')
    quantity = models.PositiveIntegerField()
    linetotal = models.DecimalField(max_digits=100, decimal_places=2, help_text='Rs.', default=0)
    quantity_returned = models.PositiveIntegerField(null=True, blank=True)
    posted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.id:
            prev_qty = SaleLineItem.objects.get(id=self.id).quantity
            if prev_qty != self.quantity:
                diff = prev_qty - self.quantity
                self.product.units_in_stock += diff
                self.product.save()
        # else:
            # print('def save LineItem  no id of line item')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.sale_order.customer)


    # def _get_calculated_linetotal(self):
    #     return self.quantity * self.product.sale_rate
    #
    # calculated_linetotal = property(_get_calculated_linetotal)


from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=SaleLineItem)
def update_linetotal(sender, instance, *args, **kwargs):
    instance.linetotal = instance.quantity * instance.product.sale_rate


# @receiver(post_save, sender=Sale)
# def update_product_quantity(sender, instance, **kwargs):
#     if instance.post_items:
#         items = instance.sale_line_items.all()
#         for item in items:
#             if not item.posted:
#                 item.posted = True
#                 item.save()
#                 item.product.units_in_stock -= item.quantity
#                 item.product.save()
#     else:
#         items = instance.sale_line_items.all()
#         for item in items:
#             if item.posted:
#                 item.posting_status = False
#                 item.save()
#                 item.product.units_in_stock += item.quantity
#                 item.product.save()
