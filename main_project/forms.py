# forms.py
from django import forms
from .models import PurchaseOrder

from django import forms
from .models import PurchaseOrder

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['medicine', 'quantity', 'company_name']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),  # Make the company_name field read-only
        }



# class PurchaseOrderForm(forms.Form):
#     purchase_order_id = forms.CharField(label='Purchase Order ID', max_length=20)
#     timestamp = forms.DateTimeField(label='Timestamp')
#     status = forms.CharField(label='Status', max_length=20)
    
#     company_name = forms.CharField(label='Company Name', max_length=100)
#     company_address = forms.CharField(label='Company Address', widget=forms.Textarea)
#     company_phone = forms.CharField(label='Company Phone', max_length=20)
#     company_email = forms.EmailField(label='Company Email')

#     medicine_name = forms.CharField(label='Medicine Name', max_length=100)
#     quantity = forms.IntegerField(label='Quantity')
#     batch_number = forms.CharField(label='Batch Number', max_length=20, required=False)
#     manufacturer = forms.CharField(label='Manufacturer', max_length=100)

#     additional_notes = forms.CharField(label='Additional Notes', widget=forms.Textarea, required=False)

#     requester_name = forms.CharField(label='Requester Name', max_length=100)
#     requester_email = forms.EmailField(label='Requester Email')
#     requester_phone = forms.CharField(label='Requester Phone', max_length=20)

#     delivery_address = forms.CharField(label='Delivery Address', widget=forms.Textarea)

from django import forms
from logi.models import DeliveryPerson

class DeliveryPersonForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = ['phone_number', 'vehicle_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['vehicle_number'].widget.attrs.update({'class': 'form-control'})
from django import forms
from logi.models import DeliveryPerson

class DeliveryAssignmentForm(forms.Form):
    order = forms.ModelChoiceField(queryset=None, label='Select Order')
    delivery_person = forms.ModelChoiceField(queryset=DeliveryPerson.objects.all(), label='Select Delivery Person')

    def __init__(self, *args, **kwargs):
        undelivered_orders = kwargs.pop('undelivered_orders', None)
        super(DeliveryAssignmentForm, self).__init__(*args, **kwargs)
        if undelivered_orders is not None:
            # Customize the labels for order options to display order ID
            self.fields['order'].queryset = undelivered_orders
            self.fields['order'].label_from_instance = lambda obj: f'Order ID: {obj.id}'

            # Customize the labels for delivery person options to display name
            self.fields['delivery_person'].label_from_instance = lambda obj: obj.user.name  # Assuming 'user' is the related User model field in DeliveryPerson
