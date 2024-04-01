from django.contrib import admin
from .models import Customer,Employee,User,Medicine,demo
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Customer)
admin.site.register(User)
@admin.register(Employee)
class user(ImportExportModelAdmin):
    pass
@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    list_display = ( 'medicine_name', 'requires_prescription', 'type_of_sell', 'manufacturer', 'salt',
                    'mrp', 'uses', 'alternate_medicines', 'side_effects', 'how_to_use', 'chemical_class',
                    'habit_forming', 'therapeutic_class', 'action_class', 'how_it_works', 'batch_no', 'exp_date',
                    'mfg_date', 'in_stock', 'wholesale_price', 'added_date', 'medicine_image', 'active_status')


    
@admin.register(demo)
class user(ImportExportModelAdmin):
    pass 