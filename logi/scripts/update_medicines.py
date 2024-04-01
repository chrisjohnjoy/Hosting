# update_medicines.py

import pandas as pd
from models import Medicine  # Import your Medicine model
from datetime import datetime

def update_medicines_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')

    for index, row in df.iterrows():
        medicine_name = row['medicine_name']
        try:
            medicine = Medicine.objects.get(medicine_name=medicine_name)
            
            # Update fields based on your Excel columns
            medicine.type_of_sell = row['type_of_sell']
            medicine.manufacturer = row['manufacturer']
            medicine.salt = row['salt']
            medicine.mrp = row['mrp']
            medicine.uses = row['uses']
            medicine.alternate_medicines = row['alternate_medicines']
            medicine.side_effects = row['side_effects']
            medicine.how_to_use = row['how_to_use']
            medicine.chemical_class = row['chemical_class']
            medicine.habit_forming = row['habit_forming']
            medicine.therapeutic_class = row['therapeutic_class']
            medicine.action_class = row['action_class']
            medicine.how_it_works = row['how_it_works']
            medicine.batch_no = row['batch_no']
            medicine.exp_date = datetime.strptime(row['exp_date'], '%Y-%m-%d').date()
            medicine.mfg_date = datetime.strptime(row['mfg_date'], '%Y-%m-%d').date()
            medicine.in_stock = row['in_stock']
            medicine.wholesale_price = row['wholesale_price']
            medicine.medicine_image = row['medicine_image']  # Replace with the actual column name in your Excel file

            # Add/update other fields as needed

            medicine.save()  # Save the changes to the database
            print(f"Medicine '{medicine_name}' updated successfully.")
        except Medicine.DoesNotExist:
            print(f"Medicine '{medicine_name}' not found.")

if __name__ == "__main__":
    excel_file_path = "E:\\Project\\django\\MedicalStore\\project1\\New_Sample.xlsx"
    update_medicines_from_excel(excel_file_path)
