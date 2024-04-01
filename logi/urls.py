# urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', views.CustomerRegisterView.as_view(), name='register'),
    path('registeremployee/', views.EmployeeRegisterView.as_view(), name='employee_register'),
    path('login/', views.userlo, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('customer/profile/<int:user_id>/', views.update_customer_profile, name='update_customer_profile'),
    path('login/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('login/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('medicine-list/', views.medicine_list, name='medicine_list'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('edit_medicine/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('delete_medicine/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    path('add_to_cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:medicine_id>/', views.update_cart, name='update_cart'),
    path('reset_cart/', views.reset_cart, name='reset_cart'), 
    path('remove_from_cart/<int:medicine_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('check-medicine-name-availability/', views.check_medicine_name_availability, name='check_medicine_name_availability'),
    path('search-medicines/', views.search_medicines, name='search_medicines'),
    path('medicine-detail/<int:medicine_id>/', views.medicine_details, name='medicine_details'),
    path('upload_prescription/', views.upload_prescription, name='upload_prescription'),
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('verify_prescription/<int:prescription_id>/', views.verify_prescription, name='verify_prescription'),
    path('prescription_verification/', views.prescription_verification_dashboard, name='prescription_verification_dashboard'),
    path('total_users/', views.TotalUsersView.as_view(), name='total_users'),
    path('total_customers/', views.TotalCustomersView.as_view(), name='total_customers'),
    path('total-pharmacists/', views.TotalPharmacistsView.as_view(), name='total_pharmacists'),
    path('total_medicines/', views.TotalMedicinesView.as_view(), name='total_medicines'),
    path('low-stock-medicines/', views.low_stock_medicines, name='low_stock_medicines'),
    path('delivery/', views.DeliveryPersonRegisterView.as_view(), name='delivery_person_register'),

    

    ]


