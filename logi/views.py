import math
from operator import countOf
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from .forms import (
    CustomerProfileForm, CustomerSignupForm, EmployeeSignupForm, LoginForm, MedicineForm,
)
from .models import DeliveryPerson, User, Customer, Employee, Medicine, Cart, CartItem, Prescription, PrescriptionVerification

class CustomerRegisterView(View):
    def get(self, request):
        form = CustomerSignupForm()
        return render(request, 'customer_registers.html', {'form': form})

    def post(self, request):
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            # Create a User instance
            user = form.save()

            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            # Create a Customer instance and associate it with the user0
            customer = Customer(user=user, phone_number=phone_number, address=address)
            customer.save()

            messages.success(request, 'Customer registration successful!')
            return redirect('/')
        else:
            return render(request, 'customer_registers.html', {'form': form})

class EmployeeRegisterView(View):
    def get(self, request):
        form = EmployeeSignupForm()
        return render(request, 'home/registerpharmacist.html', {'form': form})
    
    def post(self, request):
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            # Create a User instance
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            designation = form.cleaned_data['designation']
            # Create an Employee instance and associate it with the user
            employee = Employee(user=user,phone_number=phone_number,designation=designation)
            employee.save()
            messages.success(request, 'Employee registration successful!')
            return redirect('admin_dashboard')
        else:
            return render(request, 'home/registerpharmacist.html', {'form': form})
   
from django.shortcuts import render, redirect
from .forms import DeliveryPersonSignupForm

class DeliveryPersonRegisterView(View):
    def get(self, request):
        form = DeliveryPersonSignupForm()
        return render(request, 'home/delivery_register.html', {'form': form})

    def post(self, request):
        form = DeliveryPersonSignupForm(request.POST)
        if form.is_valid():
            # Create a User instance
            user = form.save()

            # Additional fields specific to delivery person
            phone_number = form.cleaned_data['phone_number']
            vehicle_number = form.cleaned_data['vehicle_number']
            # Create a DeliveryPerson instance and associate it with the user
            delivery_person = DeliveryPerson(user=user, phone_number=phone_number, vehicle_number=vehicle_number)
            delivery_person.save()

            messages.success(request, 'Delivery person registration successful!')
            return redirect('/')
        else:
            return render(request, 'home/delivery_register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def userlo(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember:
                    request.session.set_expiry(60)
                    print("Session will expire after 60 seconds.") 

                if user.is_superuser:
                    return redirect('admin_dashboard')  # Redirect superuser to admin_dashboard
                elif hasattr(user, 'deliveryperson'):  # Check if the user is a delivery person
                    return redirect('delivery_dashboard', delivery_person_id=user.deliveryperson.pk)
                else:
                    return redirect('/')  # Redirect to your desired page upon successful login
            else:
                # Add an error message for incorrect username or password
                form.add_error(None, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
# elif user.is_delivery:
#                     return redirect('delivery_person_dashboard') 

@login_required
def customer_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        customer = user.customer  # Assuming you have a OneToOneField between User and Customer
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return HttpResponse('User not found', status=404)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
    else:
        form = CustomerProfileForm(instance=customer)

    return render(request, 'profile.html', {'form': form, 'user': user})
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the user's session to keep them logged in
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customer_profile')  # Redirect to the profile page or another appropriate URL
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'password_change.html', {'form': form})


# View for changing the user's password
class ChangePasswordView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')  # URL to redirect after successful password change




@login_required
def update_customer_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)

        # Ensure that the user is a customer
        if user.is_customer:
            customer = user.customer

            if request.method == 'POST':
                # Create a form instance and populate it with data from the request
                form = CustomerProfileForm(request.POST, instance=customer)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile updated successfully!')
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                # Create an initial form with existing data
                form = CustomerProfileForm(instance=customer)

            return render(request, 'profile.html', {'form': form})

    except User.DoesNotExist:
        # Handle the case where the user does not exist
        pass

    return redirect('/')  # Redirect to the homepage or an appropriate URL


#pagenation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# views.py


from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db import models  # Import models module

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Medicine
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import Medicine

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Medicine
from django.shortcuts import render
from django.core.paginator import Paginator
from logi.models import Medicine

from django.core.paginator import Paginator
from .models import Medicine

def medicine_list(request):
    # Sorting logic
    sort_by = request.GET.get('sort_by', 'mrp')  # Default sort by price

    # Retrieve active medicines from the database and apply sorting
    all_medicines = Medicine.objects.filter(active_status=True).order_by(sort_by)

    # Get distinct values for type_of_sell
    type_of_sell_options = Medicine.objects.values_list('type_of_sell', flat=True).distinct()

    # Filtering logic
    selected_type_of_sell = request.GET.get('type_of_sell', '')
    if selected_type_of_sell:
        all_medicines = all_medicines.filter(type_of_sell=selected_type_of_sell)

    # Pagination logic
    items_per_page = int(request.GET.get('items', 6))
    page = request.GET.get('page')
    paginator = Paginator(all_medicines, items_per_page)
    medicines = paginator.get_page(page)

    return render(request, 'medicine_catalogue.html', {
        'medicines': medicines,
        'items_per_page': items_per_page,
        'type_of_sell_options': type_of_sell_options,
        'selected_type_of_sell': selected_type_of_sell,
    })




# views.py
from django.http import JsonResponse
from django.db.models import Q
from .models import Medicine

# views.py
from django.http import JsonResponse
from django.db.models import Q
from .models import Medicine

from django.http import JsonResponse
from django.db.models import Q
from .models import Medicine

def search_medicines(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        medicines = Medicine.objects.filter(
            Q(medicine_name__icontains=search_query) | Q(salt__icontains=search_query),
            active_status=True  # Filter out inactive medicines
        )
        results = [{'medicine_id': medicine.medicine_id, 'name': medicine.medicine_name} for medicine in medicines]
        return JsonResponse({'results': results})






@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            # Debugging: Print to check if the view is reached
            print("Form is valid. Data is ready to save.")
            # Save the data
            form.save()
            return redirect('medicine_list')
        else:
            # Debugging: Print form errors to check for validation issues
            print("Form is not valid. Errors:", form.errors)
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})
@login_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = MedicineForm(instance=medicine)  # Initialize form with instance data

    return render(request, 'edit_medicine.html', {'form': form, 'medicine': medicine})



@login_required
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'delete_medicine.html', {'medicine': medicine})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, Cart, CartItem
from .forms import CartItemForm  # You'll need to create this form

# 
## Redirect back to the medicine catalog or wherever you want
#new code

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)

    # Check if the user has an active cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
        cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)

        if not cart_item_created:
            cart_item.quantity += 1
            cart_item.save()


    return redirect('medicine_list')

from .models import Cart, CartItem, Prescription
from .forms import PrescriptionUploadForm
@login_required
def view_cart(request):
    cart = None
    cart_items = []
    cart_requires_prescription = False
    prescription_form = None
    prescription = None  # Initialize prescription to None

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, active=True).first()
        cart_items = cart.cartitem_set.all() if cart else []
        cart_requires_prescription = any(cart_item.requires_prescription for cart_item in cart_items)
        prescription_form = PrescriptionUploadForm()
        if cart:
            prescription = Prescription.objects.filter(cart=cart).first()  # Fetch the associated prescription

    return render(request, 'view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_requires_prescription': cart_requires_prescription,
        'prescription_form': prescription_form,
        'prescription': prescription,  # Include prescription in the context
    })





# You'll need to create views for updating and checking out the cart as well.

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


@login_required
def update_cart(request, medicine_id):
    # Find the CartItem based on the medicine and the user's active cart
    cart_item = get_object_or_404(CartItem, cart__user=request.user, cart__active=True, medicine_id=medicine_id)

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']

            # Ensure the new quantity is a positive integer
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()

                # Calculate the updated total for the specific medicine item
                item_total = cart_item.get_total_price()

                # Calculate the updated overall total and grand total
                cart = cart_item.cart
                total = cart.get_total_price()
                grand_total = total  # You can update this if you have additional costs

                # Return the updated totals as JSON response
                data = {
                    'item_total': item_total,
                    'total': total,
                    'grand_total': grand_total,
                }
                return JsonResponse(data)

    # Handle other cases if needed
    return HttpResponseBadRequest('Invalid request')



from django.shortcuts import redirect
@login_required
def reset_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, active=True).first()
        if cart:
            # Reset the cart items
            cart.cartitem_set.all().delete()

            # Reset the prescription (if it exists)
            prescription = Prescription.objects.filter(cart=cart).first()
            if prescription:
                prescription.delete()

            # Optionally, you can display a success message to inform the user
            messages.success(request, 'Cart and prescription reset successfully.')

    return redirect('view_cart')



# views.py

from django.shortcuts import redirect, get_object_or_404
from .models import CartItem

@login_required
def remove_from_cart(request, medicine_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, cart__active=True, medicine_id=medicine_id)

    # Increase the quantity of the product in stoc

    cart_item.delete()

    # Optionally, you can display a success message to inform the user
    messages.success(request, 'Item removed from cart.')

    return redirect('view_cart')


# views.py

@login_required
def check_medicine_name_availability(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')

        # Check if the medicine name is available (replace this with your logic)
        is_available = not Medicine.objects.filter(medicine_name=medicine_name).exists()

        # Return a JSON response
        data = {'is_available': is_available}
        return JsonResponse(data)
    
    from django.shortcuts import render, get_object_or_404
from .models import Medicine

def medicine_details(request, medicine_id):
    # Retrieve the medicine object based on medicine_id or return a 404 error
    medicine = get_object_or_404(Medicine, medicine_id=medicine_id)

    # Pass the medicine object to the template for rendering
    return render(request, 'medicine_details.html', {'medicine': medicine})


# Your other import statements
from .models import Cart, Prescription
from .forms import PrescriptionUploadForm
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import redirect

@login_required
def upload_prescription(request):
    if request.method == 'POST':
        prescription_form = PrescriptionUploadForm(request.POST, request.FILES)

        if prescription_form.is_valid():
            cart = Cart.objects.filter(user=request.user, active=True).first()

            if cart:
                # Fetch the existing prescription or create a new one
                prescription, created = Prescription.objects.get_or_create(cart=cart)
                prescription.prescription_file = prescription_form.cleaned_data['prescription']
                prescription.save()

                # Verify the prescription if the user is an employee
                if request.user.is_employee:
                    verification = PrescriptionVerification(prescription=prescription, verified_by=request.user)
                    verification.save()
                    prescription.is_verified = True
                    prescription.save()

                    messages.success(request, 'Prescription uploaded and verified successfully.')
                else:
                    messages.success(request, 'Prescription uploaded successfully, pending verification.')

            return redirect('view_cart')

        print(prescription_form.errors)

    return redirect('view_cart')

from django.http import JsonResponse
from django.utils import timezone
from django.utils import timezone  # Import the timezone module

@login_required
def verify_prescription(request, prescription_id):
    if request.user.is_employee:
        prescription = get_object_or_404(Prescription, pk=prescription_id)
        print("n")
        if not prescription.is_verified:
            # Verify the prescription
            verification = PrescriptionVerification(prescription=prescription, verified_by=request.user)
            verification.verified_at = timezone.now()  # Record the verification timestamp
            verification.is_verified=True
            verification.save()
            prescription.is_verified = True
            prescription.save()

        # Handle successful verification (you can add a success message or redirect)
        # For example, you can add a success message
        messages.success(request, 'Prescription verified successfully.')

        return redirect('your_success_url')  # Replace 'your_success_url' with the actual URL

    else:
        # Handle non-employee access
        # You can return a 403 Forbidden response or redirect to another page
        return render(request, 'access_denied.html')
    
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDay
from django.shortcuts import render
from django.views import View
from .models import User, Medicine
from main_project.models import Sales
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
import math

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@method_decorator(user_passes_test(is_admin, login_url='index'), name='dispatch')
class AdminDashboardView(View):

    def get(self, request):
        # Fetch user details, excluding the superuser
        users = User.objects.filter(is_superuser=False)

        # Query for low stock medicines

        low_stock_medicines = Medicine.objects.filter(in_stock__lt=5)
        print(low_stock_medicines)
        # Fetch daily revenue data for the current month
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        daily_revenue_data = Sales.objects.annotate(
            day=TruncDay('order__order_date')
        ).filter(order__order_date__gte=current_month_start).values('day').annotate(
            total_revenue=Sum('revenue')
        ).order_by('day')

        # Extract labels and values for day-wise revenue
        day_labels = [entry['day'].strftime('%b %d') for entry in daily_revenue_data]
        day_revenue_values = [math.ceil(entry['total_revenue']) for entry in daily_revenue_data]

        # Create dictionaries for day-wise chart data
        day_revenue_data = {'labels': day_labels, 'values': day_revenue_values}

        # Fetch monthly revenue data
        monthly_revenue_data = Sales.objects.annotate(
            month=TruncMonth('order__order_date')
        ).values('month').annotate(
            total_revenue=Sum('revenue')
        ).order_by('month')

        # Extract labels and values for monthly revenue
        monthly_labels = [entry['month'].strftime('%b %Y') for entry in monthly_revenue_data]
        monthly_revenue_values = [math.ceil(entry['total_revenue']) for entry in monthly_revenue_data]

        # Create dictionaries for monthly chart data
        monthly_revenue_data = {'labels': monthly_labels, 'values': monthly_revenue_values}

        # Fetch the latest sales details for the table
        latest_sales = Sales.objects.select_related('order').order_by('-order__order_date')[:10]

        # Extract relevant information for the table
        sales_data = []
        for sale in latest_sales:
            data = {
                'order_id': sale.order.id,
                'order_date': sale.order_date,
                'total_amount': sale.total_amount,
                'revenue': sale.revenue,
                'profit': sale.profit,
            }
            sales_data.append(data)

        # Rename the headings
        table_headings = {
            'order_id': 'Order ID',
            'order_date': 'Order Date',
            'total_amount': 'Total Amount',
            'revenue': 'Revenue',
            'profit': 'Profit',
        }

        # Count the total number of users, customers, pharmacists, and medicines
        total_users = User.objects.count()
        total_customers = User.objects.filter(is_customer=True).count()
        total_pharmacists = User.objects.filter(is_employee=True).count()
        total_medicines = Medicine.objects.count()
        delivery_personnel = User.objects.filter(is_delivery_person=True).count()

        return render(request, 'home/index.html', {
            'delivery_personnel': delivery_personnel, 
            'users': users,
            'day_revenue_data': day_revenue_data,
            'monthly_revenue_data': monthly_revenue_data,
            'low_stock_medicines': low_stock_medicines,
            'low_stock_medicines_count': low_stock_medicines.count(),  # Include the count of low stock medicines
            'sales_data': sales_data,
            'table_headings': table_headings,
            'total_users': total_users,
            'total_customers': total_customers,
            'total_pharmacists': total_pharmacists,
            'total_medicines': total_medicines,
        })




from django.shortcuts import render, get_object_or_404, redirect
from .models import Prescription, PrescriptionVerification
from django.contrib.auth.decorators import login_required

@login_required  # Requires login
def verify_prescription(request, prescription_id):
    if request.user.is_employee:
        prescription = get_object_or_404(Prescription, pk=prescription_id)

        if not prescription.is_verified:
            # Verify the prescription
            verification = PrescriptionVerification(prescription=prescription, verified_by=request.user)
            verification.is_verified=True
            verification.save()
            prescription.is_verified = True
            prescription.save()

        return redirect('prescription_verification_dashboard')  # Redirect to an employee dashboard page
    else:
        # Handle non-employee access
        # You can return a 403 Forbidden response or redirect to another page
        # based on your project's requirements.
        return render(request, 'access_denied.html')
@login_required
def prescription_verification_dashboard(request):
    if request.user.is_employee:
        # Get a list of verified prescriptions
        verified_prescriptions = Prescription.objects.filter(is_verified=True)

        # Get a list of unverified prescriptions
        unverified_prescriptions = Prescription.objects.filter(is_verified=False)
        return render(request, 'prescription_verification_dashboard.html', {
            'verified_prescriptions': verified_prescriptions,
            'unverified_prescriptions': unverified_prescriptions,
        })
    else:
        # Handle non-employee access (e.g., return a 403 Forbidden response)
        return render(request, 'access_denied.html')
    
    
def representative_dashboard(request):
    return render(request, 'representative_dashboard.html')
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()

@method_decorator(login_required, name='dispatch')
class TotalCustomersView(View):
    template_name = 'home/customers_list.html'

    def get(self, request):
        customers = Customer.objects.all()
        return render(request, self.template_name, {'users': customers, 'title': 'Total Customers'})

    def post(self, request):
        if "action" in request.POST:
            action = request.POST["action"]
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(pk=user_id)
                if action == "deactivate_user" and user.is_active:
                    user.is_active = False
                    user.save()
                    messages.success(request, f'User {user.username} has been deactivated.')
                elif action == "activate_user" and not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, f'User {user.username} has been activated.')
            except User.DoesNotExist:
                print("User does not exist")
            except Exception as e:
                print(f"Error processing user action: {str(e)}")

        return redirect('total_customers')

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()

@method_decorator(login_required, name='dispatch')
class TotalUsersView(View):
    template_name = 'home/users.html'

    def get(self, request):
        users = User.objects.filter(is_superuser=False)
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        if "action" in request.POST:
            action = request.POST["action"]
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(pk=user_id)
                if action == "deactivate_user" and user.is_active:
                    user.is_active = False
                    user.save()
                    messages.success(request, f'User {user.username} has been deactivated.')
                elif action == "activate_user" and not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, f'User {user.username} has been activated.')
            except User.DoesNotExist:
                print("User does not exist")
            except Exception as e:
                print(f"Error processing user action: {str(e)}")

        return redirect('total_users')

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee

@method_decorator(login_required, name='dispatch')
class TotalPharmacistsView(View):
    template_name = 'home/pharmacist.html'

    def get(self, request):
        pharmacists = Employee.objects.all()
        return render(request, self.template_name, {'pharmacists': pharmacists, 'title': 'Total Pharmacists'})

    def post(self, request):
        if "action" in request.POST:
            action = request.POST["action"]
            user_id = request.POST.get('user_id')
            try:
                pharmacist = Employee.objects.get(pk=user_id)
                if action == "deactivate_user" and pharmacist.user.is_active:
                    pharmacist.user.is_active = False
                    pharmacist.user.save()
                    messages.success(request, f'Pharmacist {pharmacist.user.username} has been deactivated.')
                elif action == "activate_user" and not pharmacist.user.is_active:
                    pharmacist.user.is_active = True
                    pharmacist.user.save()
                    messages.success(request, f'Pharmacist {pharmacist.user.username} has been activated.')
            except Employee.DoesNotExist:
                print("Pharmacist does not exist")
            except Exception as e:
                print(f"Error processing pharmacist action: {str(e)}")

        return redirect('total_pharmacists')

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Medicine
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class TotalMedicinesView(View):
    template_name = 'home/product.html'

    def get(self, request):
        medicines = Medicine.objects.all()
        return render(request, self.template_name, {'medicines': medicines})

    def post(self, request):
        if "action" in request.POST:
            action = request.POST["action"]
            medicine_id = request.POST.get('medicine_id')
            try:
                medicine = Medicine.objects.get(pk=medicine_id)
                if action == "deactivate_medicine" and medicine.active_status:
                    medicine.active_status = False
                    medicine.save()
                    messages.success(request, f'Medicine {medicine.medicine_name} has been deactivated.')
                elif action == "activate_medicine" and not medicine.active_status:
                    medicine.active_status = True
                    medicine.save()
                    messages.success(request, f'Medicine {medicine.medicine_name} has been activated.')
            except Medicine.DoesNotExist:
                print("Medicine does not exist")
            except Exception as e:
                print(f"Error processing medicine action: {str(e)}")

        return redirect('total_medicines')

from .models import Medicine
from main_project.models import PurchaseOrder

from .models import Medicine
from main_project.models import PurchaseOrder

def low_stock_medicines(request):
    threshold = 5
    low_stock_medicines = Medicine.objects.filter(in_stock__lt=threshold)
    
    # Query all medicine IDs for which there is a purchase order
    purchase_order_med_ids = PurchaseOrder.objects.values_list('medicine_id', flat=True).distinct()
    
    return render(request, 'home/low_stock_medicines.html', {'low_stock_medicines': low_stock_medicines, 'purchase_order_med_ids': purchase_order_med_ids})
