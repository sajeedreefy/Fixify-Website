from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.website.models import BaseModel, Branch
from django.utils import timezone

# Create your models here.
class Products(BaseModel):

    title = models.CharField(max_length = 200, verbose_name=_('Title'))
    description = models.TextField(max_length = 200, verbose_name=_('Description'), blank=True)
    image = models.ImageField(upload_to='product_image', verbose_name=_('Image'), blank=True)
    available_branches = models.ManyToManyField(Branch, verbose_name=_('Available Branches'), blank=True)

    def __str__(self):
        return self.title
    

class Service(BaseModel):

    title = models.CharField(max_length = 200, verbose_name=_('Title'))
    description = models.TextField(max_length = 200, verbose_name=_('Description'), blank=True)
    product = models.ForeignKey(Products, on_delete= models.CASCADE, blank=True, null=True)

    regular_price = models.FloatField(default=0, verbose_name=_('Regular Price'))
    discount_price = models.FloatField(default=0, verbose_name=_('Discount Price'))
    service_warranty = models.CharField(max_length = 200, verbose_name=_('Service Warranty'), blank=True)
    damage_coverage = models.CharField(max_length = 200, verbose_name=_('Damage Coverage'), blank=True)

    def __str__(self):
        return self.title

class OrderLead(BaseModel):
    full_name = models.CharField(max_length = 200, verbose_name=_('Fullname'))
    phone = models.CharField(max_length = 200, verbose_name=_('Phone Number'))
    address = models.CharField(max_length = 200, verbose_name=_('Address'))
    branch = models.ForeignKey(Branch, on_delete= models.CASCADE, verbose_name=_('Branch'))
    service_date = models.DateField(blank=True, null=True, verbose_name=_('Service Date'))


    product = models.ForeignKey(Products, on_delete= models.CASCADE, blank=True, null=True, verbose_name=_('Product'))
    service = models.ForeignKey(Service, on_delete= models.CASCADE, blank=True, null=True, verbose_name=_('Service'))
    quantity = models.IntegerField(default=0)

    TYPE_CHOICES = (
        ('House Hold', 'House Hold'),
        ('Corporate', 'Corporate')
    )
    customer_type = models.CharField(choices=TYPE_CHOICES, max_length=12, default='House Hold', verbose_name=_('Customer Type'))


    STATUS_CHOICES = (
        ('Booking', 'Booking'),
        ('Confirmed', 'Confirmed'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='Booking', verbose_name=_('Lead Status'))

    def __str__(self):
        return str(self.status+' - '+ self.full_name+' - '+self.phone)


class Order(BaseModel):
    order_lead = models.ForeignKey(OrderLead, on_delete= models.CASCADE, related_name='lead_order', blank=True, null= True)

    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name=_('Invoice Number'))

    full_name = models.CharField(max_length = 200, verbose_name=_('Fullname'))
    phone = models.CharField(max_length = 200, verbose_name=_('Phone Number'))
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE, verbose_name=_('Branch'), related_name='branch_orders',null=True, blank=True)
    address = models.CharField(max_length = 200, verbose_name=_('Address'), blank=True)

    service_date = models.DateField(blank=True, null=True, verbose_name=_('Service Date'))
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('succeed', 'Succeed'),
        ('canceled', 'Canceled')
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='ongoing', verbose_name=_('Order Status'))
    created_time = models.DateTimeField(auto_now_add = True)
    bill_amount = models.FloatField(default=0, verbose_name=_('Bill Amount'))
    discount_amount =  models.FloatField(default=0, verbose_name=_('Discount Amount'))
    total_amount = models.FloatField(default=0, verbose_name=_('Total Amount'))
    note = models.TextField(max_length = 500, verbose_name=_('Note'), blank=True)

    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            today_date = timezone.now().strftime('%Y%m%d')
            last_invoice = Order.objects.filter(invoice_number__startswith=f'INV-{today_date}-').order_by('-invoice_number').first()
            if last_invoice:
                last_serial = int(last_invoice.invoice_number.split('-')[-1])
                serial = last_serial + 1
            else:
                serial = 1
            self.invoice_number = f'INV-{today_date}-{serial:04}'
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.status+' - '+ self.full_name+' - '+self.phone)


class OrderLine(BaseModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines', verbose_name=_('Order'))
    product = models.ForeignKey(Products, on_delete= models.CASCADE, blank=True, null=True, verbose_name=_('Product'))
    service = models.ForeignKey(Service, on_delete= models.CASCADE, blank=True, null=True, verbose_name=_('Service'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    amount = models.FloatField(default=0, verbose_name=_('Amount'))
    subtotal = models.FloatField(default=0, verbose_name=_('Subtotal'))

    def __str__(self):
        return str(self.order)







    


