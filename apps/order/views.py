from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from apps.website.models import Preference
from .models import Products, Service, OrderLead, Order, OrderLine
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.http import FileResponse
from io import BytesIO
import os
from weasyprint import HTML
import json
from apps.website.models import Branch

# Create your views here.
def post_order(request):
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        address = request.POST.get('address')
        branch = request.POST.get('branch')
        quantity = request.POST.get('quantity')
        service_date = request.POST.get('service_date')
        product_id = request.POST.get('product')
        service_id = request.POST.get('service')
        branch = Branch.objects.get(id=branch)
        
        # Validate the data (you can add your validation logic here)
        if not name or not telephone or not product_id or not service_id:
            messages.error(request, 'All fields are required')
        else:
            # Create and save the order
            order = OrderLead.objects.create(
                full_name=name,
                phone=telephone,
                address = address,
                branch = branch,
                service_date = service_date,
                product_id=product_id,
                service_id=service_id,
                quantity = quantity
                # Add other fields as needed
            )
            # order.save()
            messages.success(request, 'Service request placed successfully.')
    else:
        # If request method is not POST, display an error message
        messages.error(request, 'Method not allowed')
    return redirect('/')


def get_services(request):
    if 'product_id' in request.GET:
        product_id = request.GET['product_id']
        services = Service.objects.filter(product_id=product_id)
        data = [{'id': service.id, 'title': service.title, 'discount_price':service.discount_price} for service in services]
        return JsonResponse(data, safe=False)
    
    elif 'service_id' in request.GET:
        service_id = request.GET['service_id']
        service = Service.objects.get(id=service_id)
        try:
            product_image = service.product.image.url
            print(product_image)
        except:
            product_image = False
        
        data = {'id': service.id, 
                 'title': service.title, 
                 'product_image': product_image,
                 'regular_price': service.regular_price, 
                 'discount_price':service.discount_price,
                 'service_warranty':service.service_warranty,
                 'damage_coverage': service.damage_coverage}
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Product ID is required'}, status=400)
    
def confirm_order(request, pk):
    try:
        order_lead = get_object_or_404(OrderLead, pk=pk)

        if order_lead.status=='Booking':
            order_lead.status = 'Confirmed'
            order_lead.save()

        order = Order.objects.filter(order_lead=order_lead).first()
        

        if not order:
            new_order = Order.objects.create(
                full_name=order_lead.full_name,
                phone=order_lead.phone,
                address=order_lead.address,
                service_date=order_lead.service_date,
                order_lead=order_lead
            )
            order_line = OrderLine.objects.create(
                order=new_order,
                product = order_lead.product,
                service = order_lead.service,
                quantity=order_lead.quantity,
                amount=order_lead.service.discount_price,
                subtotal=order_lead.service.discount_price*order_lead.quantity
            )
            order = new_order


        order_lines = OrderLine.objects.filter(order=order)

        preference = Preference.objects.filter(is_active=True).first()
        products = Products.objects.all()
        services = Service.objects.all()

        return render(request, 'order_confirmation.html', {'order': order, 'order_lines':order_lines, 'preference': preference, 'products': products, 'services': services,})
    except Exception as e:
        return HttpResponse(f"There is an error: {str(e)}", status=404)

def process_order(request, order_id):
    if request.method == 'POST':
        # Get form data
        data = json.loads(request.body)
        
        full_name = data.get('fullName')
        phone = data.get('phone')
        address = data.get('address')
        service_date = data.get('serviceDate')
        note = data.get('note')
        bill_amount = data.get('billAmount')

        # Retrieve or create the Order object
        order, create = Order.objects.get_or_create(id=order_id)
        
        # Update order details
        order.full_name = full_name
        order.phone = phone
        order.address = address
        order.service_date = service_date
        order.note = note
        order.bill_amount = bill_amount
        order.status = 'succeed'
        order.save()

        # Get order lines data
        order_lines = data.get('orderLines', [])

        # Create or update order lines
        for line_data in order_lines:
            OrderLine.objects.update_or_create(
                id= line_data.get('line_id'),
                order=order,
                product_id=line_data.get('product'),
                service_id=line_data.get('service'),
                defaults={
                    'quantity': line_data.get('quantity'),
                    'amount': line_data.get('amount'),
                    'subtotal': line_data.get('subtotal')
                }
            )
        # Optionally, you can return a success response
        return JsonResponse({'messages': 'Order processed successfully'}, status=200)

    else:
        # Handle GET request
        return JsonResponse({'error': 'Method not allowed'}, status=405)     

    

def generate_invoice(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist.", status=404)
    
    order_lines = OrderLine.objects.filter(order=pk)
    preference = Preference.objects.filter(is_active=True).first()

    # Render invoice template with order details
    template_path = 'invoice.html'
    context = {
        'order': order,
        'order_lines': order_lines,
        'preference': preference,
        'domain': request.META.get('HTTP_HOST')
    }
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    pdf_file = BytesIO()
    HTML(string=html).write_pdf(pdf_file)

    # Return PDF as response
    pdf_file.seek(0)
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response



def cancel_order(request, pk):
    try:
        order = Order.objects.get(id=pk)
        order.status = 'canceled'
        order.save()
        messages.warning(request, 'Service canceled successfully.')

    except Order.DoesNotExist:
        return HttpResponse("Order does not exist.", status=404)

    # Assuming that 'confirm_order' is a view name defined in your URLconf
    return redirect(reverse('order:confirm_order', kwargs={'pk': order.order_lead.pk}))




