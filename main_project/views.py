# razorpay/views.py

from contextlib import nullcontext
from django.contrib.auth.decorators import login_required
from django.forms import DateField
from django.shortcuts import render, redirect
from logi.models import Cart, User
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))



# views.py

from django.contrib import messages

from logi.models import Cart, CartItem, Prescription,PrescriptionVerification
from logi.forms import PrescriptionUploadForm

@login_required
def view_cart(request):
    cart = None
    cart_items = []
    cart_requires_prescription = False
    prescription_form = None
    prescription = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, active=True).first()
        cart_items = cart.cartitem_set.all() if cart else []
        verification = PrescriptionVerification(prescription=prescription, verified_by=request.user)

        cart_requires_prescription = any(cart_item.requires_prescription for cart_item in cart_items)
        prescription_form = PrescriptionUploadForm()
        if cart:
            prescription = Prescription.objects.filter(cart=cart).first()  # Fetch the associated prescription
    return render(request, 'view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'verification' : verification,
        'cart_requires_prescription': cart_requires_prescription,
        'prescription_form': prescription_form,
        'prescription': prescription,  # Include prescription in the context
    })
# views.py
from .models import PurchaseOrder, Sales

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, active=True).first()

    if not cart:
        return redirect('view_cart')

    cart_items = cart.cartitem_set.all()
    cart_requires_prescription = any(cart_item.requires_prescription for cart_item in cart_items)

    if cart_requires_prescription:
        prescription = Prescription.objects.filter(cart=cart).first()

        if prescription:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                total_amount=cart.get_total_price(),
                prescription=prescription,
                # Add other fields as needed
            )

            razorpay_order = razorpay_client.order.create({
                'amount': int(cart.get_total_price() * 100),  # Amount in paise
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': 1 
            })

            order.razorpay_order_id = razorpay_order['id']
            order.save()

            # Save OrderItems
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    medicine=cart_item.medicine,
                    quantity=cart_item.quantity,
                    cart=cart,
                    # Add other fields as needed
                )

            cart.active = False
            cart.save()

            

            return render(request, 'checkout.html', {
                'cart': cart,
                'cart_items': cart_items,
                'razorpay_order_id': razorpay_order['id'],
                'cart_requires_prescription': cart_requires_prescription,
                'prescription': prescription,
            })

    else:
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_amount=cart.get_total_price(),
            prescription=None,
            # Add other fields as needed
        )

        razorpay_order = razorpay_client.order.create({
            'amount': int(cart.get_total_price() * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': f'order_{order.id}',
            'payment_capture': 1 
        })

        order.razorpay_order_id = razorpay_order['id']
        order.save()

        # Save OrderItems
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                medicine=cart_item.medicine,
                quantity=cart_item.quantity,
                cart=cart,
                # Add other fields as needed
            )
            cart.active = False
            cart.save()

      

        return render(request, 'checkout.html', {
            'cart': cart,
            'cart_items': cart_items,
            'razorpay_order_id': razorpay_order['id'],
            'cart_requires_prescription': cart_requires_prescription,
            'prescription': None,
        })
from datetime import datetime, timedelta
from .models import Sales, MonthlyStats

@csrf_exempt
@login_required
def razorpay_payment_handler(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })

            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_status = 'PAID'
            order.delivery_date = order.order_date + timedelta(days=5)
            order.save()

            # Calculate revenue and profit
            total_amount = order.total_amount
            revenue = total_amount  # Revenue is the total order amount
            profit = 0

            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                profit += (order_item.medicine.mrp - order_item.medicine.wholesale_price) * order_item.quantity

            # Create a Sales instance
            sales = Sales.objects.create(
                order=order,
                order_date=order.order_date,
                total_amount=total_amount,
                revenue=revenue,
                profit=profit
            )

            # Decrease stock for each medicine associated with the order
            for order_item in order_items:
                medicine = order_item.medicine
                medicine.in_stock -= order_item.quantity
                medicine.save()



            # Fetch related medicines for the order
            return redirect('paymentsuccess', order_id=order.id)
        except Exception as e:
            print(f"Payment failed: {e}")
            # Render the payment failed template
            return render(request, 'payment_failed.html')

    return HttpResponseBadRequest("Invalid request")


# views.py
from django.shortcuts import render
from .models import Order

from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from reportlab.pdfgen import canvas
from io import BytesIO
from .utils import send_invoice_email,generate_invoice_pdf  # Assume you have a function for generating PDFs

# ... (your other imports)
@login_required
def paymentsuccess(request, order_id):
    try:
        # Fetch the Order instance first
        order = Order.objects.get(id=order_id)

        # Now, filter OrderItem instances related to the order
        order_items = order.orderitem_set.all()
        # Fetch related Medicines for the order using the OrderItem instances
        medicines = [order_item.medicine for order_item in order_items]

        # Generate PDF invoice
        pdf_content = generate_invoice_pdf(order)

        # Send email with the PDF attached
        send_invoice_email(order.user.email, pdf_content, order.id)

    except Order.DoesNotExist:
        # Handle the case where the order is not found
        return render(request, 'payment_fail.html')  # You can create a payment_fail.html template

    return render(request, 'payment_success.html', {'order': order, 'medicines': medicines})




from django.http import HttpResponse
from django.template.loader import render_to_string
from .utils import generate_invoice_pdf  # Assume you have a function for generating PDFs
@login_required
def download_invoice(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        pdf_content = generate_invoice_pdf(order)

        # Create a response with PDF content
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_order_{order_id}.pdf'
        response.write(pdf_content.getvalue())

        return response

    except Order.DoesNotExist:
        return HttpResponse("Order not found.", status=404)

from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest
from .models import Order
from logi.models import PrescriptionVerification
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, Delivery

@login_required
def customer_order_history(request):
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    if start_date_param and end_date_param:
        try:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            # Handle invalid date format
            return HttpResponseBadRequest("Invalid date format. Please use 'YYYY-MM-DD'.")

        orders = Order.objects.filter(
            user=request.user,
            order_date__range=(start_date, end_date)
        ).order_by('-id')
    else:
        orders = Order.objects.filter(
            user=request.user
        ).order_by('-id')
    
    # Fetch delivery information for each order
    for order in orders:
        deliveries = Delivery.objects.filter(order_id=order.id)
        order.deliveries = deliveries  # Assign deliveries to the order object
    
    return render(request, 'customer_order_history.html', {
        'orders': orders,
        'start_date_param': start_date_param,
        'end_date_param': end_date_param,
    })

from django.shortcuts import render
from main_project.models import Order

def pharmacist_order_view(request):
    # Retrieve all orders initially
    orders = Order.objects.all()

    
    return render(request, 'pharmacist_order_view.html', orders)


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Fetch related order items
    order_items = OrderItem.objects.filter(order=order)

    # Additional information needed for tracking, such as shipment details, can be added here

    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})


from django.shortcuts import render, redirect
from .forms import  PurchaseOrderForm
from logi.models import Medicine

@login_required
def place_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_orders')
    else:
        form = PurchaseOrderForm()
    
    medicines = Medicine.objects.all()
    return render(request, 'place_order_admin.html', {'form': form, 'medicines': medicines})



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from logi.models import  Medicine, MedicineStockAlert

# razorpay/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from logi.models import Cart
import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))


@login_required
def pharmacist_order_details(request):
    # Retrieve all orders placed today for the pharmacist
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    orders = Order.objects.filter(order_date__range=(start_of_day, end_of_day)).order_by('-id')
    return render(request, 'pharmacist_order_details.html', {'orders': orders})

# views.py
# views.py

from django.http import HttpResponseBadRequest
from .models import Order, OrderItem
from datetime import datetime

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Fetch related order items
    order_items = OrderItem.objects.filter(order=order)

    # Initialize delivery_status
    delivery_status = None

    # Check if order has a prescription and it is verified
    if order.prescription and order.prescription.is_verified:
        if order.delivery_date:
            current_date = datetime.now().date()
            if current_date <= order.delivery_date:
                delivery_status = "In Transit"
            else:
                delivery_status = "Delivered"
        else:
            delivery_status = "Pending Delivery Date"
    # Check if order has a prescription but it is not verified
    elif not order.prescription:
        delivery_status = "Prescription Not Verified"
    # Handle the case where order does not have a prescription
    else:
        delivery_status = "No Prescription"

    return render(request, 'order_details.html', {'order': order, 'order_items': order_items, 'delivery_status': delivery_status})




# main_project/views.py
from django.shortcuts import render
from .models import Order, OrderItem

@login_required
def latest_orders(request):
    latest_orders = Order.objects.all().order_by('-order_date')[:10]  # Change the number as per your requirement

    return render(request, 'home/latest_orders.html', {'latest_orders': latest_orders})

# main_project/views.py
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'home/order_details.html', {'order': order, 'order_items': order_items})

# views.py
from django.http import HttpResponse
from .models import Order
from .utils import generate_invoice_pdf  # Import your utility function for generating PDFs

@login_required
def download_invoice(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        pdf_content = generate_invoice_pdf(order)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_order_{order_id}.pdf'
        response.write(pdf_content.getvalue())

        return response

    except Order.DoesNotExist:
        return HttpResponse("Order not found.", status=404)

from django.views.generic import View
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import DateField
from .models import Sales
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class SalesAnalysisView(View):
    def get(self, request):
        # Fetch monthly sales data
        monthly_sales_data = Sales.objects.annotate(
            month=TruncMonth('order__order_date', output_field=DateField())
        ).values('month').annotate(
            total_sales=Sum('total_amount'),
            total_profit=Sum('profit')  # Calculate total profit
        ).order_by('month')

        # Extract labels and values for monthly sales
        monthly_labels = [entry['month'].strftime('%b %Y') for entry in monthly_sales_data]
        total_sales_values = [float(entry['total_sales']) for entry in monthly_sales_data]
        total_profit_values = [float(entry['total_profit']) for entry in monthly_sales_data]

        # Calculate total revenue and profit
        total_revenue = sum(total_sales_values)
        total_profit = sum(total_profit_values)

        # Calculate average sales per month
        average_sales_per_month = total_revenue / len(monthly_labels)

        return render(request, 'home/sales_analysis.html', {
            'monthly_labels': monthly_labels,
            'total_sales_values': total_sales_values,
            'total_profit_values': total_profit_values,
            'total_revenue': total_revenue,
            'total_profit': total_profit,
            'average_sales_per_month': average_sales_per_month,
        })

from django.shortcuts import render
from .models import Medicine
from collections import Counter

@login_required
def manufacturer_pie_chart(request):
    # Retrieve all medicines from the database
    all_medicines = Medicine.objects.all()

    # Extract the manufacturers from the medicines
    manufacturers = [medicine.manufacturer for medicine in all_medicines]

    # Count the occurrences of each manufacturer
    manufacturer_counts = Counter(manufacturers)

    # Convert the Counter object to lists for labels and data
    labels = list(manufacturer_counts.keys())
    data = list(manufacturer_counts.values())

    # Pass data to the template for rendering
    return render(request, 'home/manufactouru.html', {'labels': labels, 'data': data})

from django.shortcuts import render
from logi.models import Medicine
from django.shortcuts import render
from .models import Medicine
@login_required
def manufacturer_products_view(request):
    unique_manufacturers = Medicine.objects.values_list('manufacturer', flat=True).distinct()
    selected_manufacturer = request.GET.get('manufacturer')
    manufacturer_products = None
    
    if selected_manufacturer:
        manufacturer_products = Medicine.objects.filter(manufacturer=selected_manufacturer)
    
    context = {
        'unique_manufacturers': unique_manufacturers,
        'selected_manufacturer': selected_manufacturer,
        'manufacturer_products': manufacturer_products,
    }
    
    
    return render(request, 'home/view_manufactour.html', context)

from django.shortcuts import redirect

def save_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        try:
            medicine = Medicine.objects.get(medicine_id=product_id)
            PurchaseOrder.objects.create(
                medicine_id=medicine.medicine_id,
                company_name=medicine.manufacturer,
                timestamp=timezone.now(),
                quantity=10
            )
        except Medicine.DoesNotExist:
            print('Medicine not found')
    return redirect('purchase_orders')  # Redirect to the product listing page


from django.shortcuts import render
from .models import PurchaseOrder

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import PurchaseOrder

def purchase_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        if action == 'update_quantity':
            # Update the quantity by incrementing by 10
            order = get_object_or_404(PurchaseOrder, id=order_id)
            order.quantity += 10
            order.save()
        elif action == 'cancel_order':
             # Delete the order from the database
            order = get_object_or_404(PurchaseOrder, id=order_id)
            order.delete() 
        return redirect('purchase_orders')
    else:
        orders = PurchaseOrder.objects.filter(active=True)
        return render(request, 'home/purchase_order.html', {'orders': orders})
from django.shortcuts import render, get_object_or_404, redirect
from logi.models import DeliveryPerson
from .forms import DeliveryPersonForm

def delivery_person_list(request):
    # Fetch all delivery personnel from the database
    delivery_personnel = DeliveryPerson.objects.all()

    # Render the delivery personnel list template with the queryset
    return render(request, 'home/delivery_list.html', {'delivery_personnel': delivery_personnel})
def edit_delivery_person(request, delivery_person_id):
    # Retrieve the delivery person object
    delivery_person = get_object_or_404(DeliveryPerson, pk=delivery_person_id)

    # Check if the form is submitted
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST, instance=delivery_person)
        if form.is_valid():
            form.save()
            return redirect('delivery_person_list')
    else:
        form = DeliveryPersonForm(instance=delivery_person)

    return render(request, 'home/edit_delivery_person.html', {'form': form})





def delete_delivery_person(request, delivery_person_id):
    # Fetch the delivery person object from the database
    delivery_person = get_object_or_404(DeliveryPerson, pk=delivery_person_id)

    if request.method == 'POST':
        # If the request method is POST, delete the delivery person and associated user
        user_id = delivery_person.user_id  # Get the associated user ID
        delivery_person.delete()  # Delete the delivery person
        User.objects.filter(pk=user_id).delete()  # Delete the associated user
        return redirect('delivery_person_list')
    else:
        # If the request method is not POST, render a confirmation page
        return render(request, 'home/delete_delivery_person.html', {'delivery_person': delivery_person})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Delivery
from logi.models import DeliveryPerson

def delivery_dashboard(request, delivery_person_id):
    delivery_person = get_object_or_404(DeliveryPerson, pk=delivery_person_id)
    assigned_deliveries = Delivery.objects.filter(delivery_person=delivery_person)

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        delivery.status = 'delivered'
        delivery.save()
        return redirect('delivery_dashboard', delivery_person_id=delivery_person_id)

    return render(request, 'delivery/delivery_dashboard.html', {'delivery_person': delivery_person, 'assigned_deliveries': assigned_deliveries})

# views.py
from django.shortcuts import render, redirect
from .forms import DeliveryAssignmentForm
from .models import Order

from django.shortcuts import render, redirect
from .forms import DeliveryAssignmentForm
from .models import Order, Delivery


def assign_delivery(request):
    # Filter undelivered orders that have payment status other than "PENDING"
    undelivered_orders = Order.objects.filter(is_delivery_person=False, payment_status__in=['PAID', 'FAILED'])

    if request.method == 'POST':
        form = DeliveryAssignmentForm(request.POST, undelivered_orders=undelivered_orders)
        if form.is_valid():
            order = form.cleaned_data['order']
            delivery_person = form.cleaned_data['delivery_person']
            order.assigned_delivery_person = delivery_person
            order.save()

            # Update the delivery status to "assigned"
            delivery = Delivery.objects.create(order_id=order.id, status="assigned", delivery_person=delivery_person)
            
            return redirect('assigned_deliveries_list')  # Redirect to the same page after assignment
    else:
        form = DeliveryAssignmentForm(undelivered_orders=undelivered_orders)
    return render(request, 'home/assign_delivery.html', {'form': form})

from django.shortcuts import render
from .models import Delivery

def assigned_orders_list(request):
    assigned_deliveries = Delivery.objects.all()
    return render(request, 'delivery/assigned_deliveries_list.html', {'assigned_deliveries': assigned_deliveries})

from django.urls import reverse

def mark_delivered(request, delivery_id):
    if request.method == 'POST':
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        delivery.status = 'delivered'
        delivery.save()
        # Redirect to the same page with the delivery person ID in the URL
        return redirect(reverse('delivery_dashboard', kwargs={'delivery_person_id': delivery.delivery_person.id}))
    # Handle other cases if needed
