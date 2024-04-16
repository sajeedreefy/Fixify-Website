from django.contrib import admin
from .models import Products, Service, OrderLead, Order, OrderLine
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html

# Register your models here.
admin.site.register(Products)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderLine)

class OrderLeadModelAdmin(admin.ModelAdmin):
    # Define your model admin here
    list_display = ['full_name', 'phone', 'status', 'create_time', 'confirm_button']

    def confirm_button(self, obj):
        return format_html('<a class="button" href="{}">Proccess Order</a>', reverse('order:confirm_order', args=[obj.pk]))

    confirm_button.short_description = 'Proccess Order'



admin.site.register(OrderLead, OrderLeadModelAdmin)



