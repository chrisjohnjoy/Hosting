
from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('razorpay_payment_handler/', views.razorpay_payment_handler, name='razorpay_payment_handler'),
    path('paymentsuccess/<int:order_id>/', views.paymentsuccess, name='paymentsuccess'),
    path('order_history/', views.customer_order_history, name='customer_order_history'),
    path('pharmacist_order_details/', views.pharmacist_order_details, name='pharmacist_order_history'),
    path('track_order/<int:order_id>/', views.track_order, name='track_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('latest_orders/', views.latest_orders, name='latest_orders'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
    path('sales-analysis/', views.SalesAnalysisView.as_view(), name='sales_analysis'),
    path('manufacturer-pie-chart/', views.manufacturer_pie_chart, name='manufacturer_pie_chart'),
    path('manufacturer-products/',views.manufacturer_products_view, name='manufacturer_products'),
    path('save_order/', views.save_order, name='save_order'),
    path('purchase_orders/', views.purchase_order, name='purchase_orders'),
    path('delivery-personnel/', views.delivery_person_list, name='delivery_person_list'),
    path('delivery/edit/<int:delivery_person_id>/', views.edit_delivery_person, name='edit_delivery_person'),
    path('delivery/dashboard/<int:delivery_person_id>/', views.delivery_dashboard, name='delivery_dashboard'),
    path('assign_delivery_person/', views.assign_delivery, name='assign_delivery'),
    path('assigned_deliveries/', views.assigned_orders_list, name='assigned_deliveries_list'),
    path('mark_delivered/<int:delivery_id>/', views.mark_delivered, name='mark_delivered'),


    # URL for deleting a delivery person
    path('delivery/delete/<int:delivery_person_id>/', views.delete_delivery_person, name='delete_delivery_person'),
]


