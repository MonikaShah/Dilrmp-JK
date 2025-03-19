# admin.py
from django.contrib import admin
from .models import MasterTrainer,Course,Attendance

class MasterTrainerAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view in the admin panel
    list_display = ('regis_date','name', 'email', 'phone_number', 'specialization_subject', 'institution', 
                    'experience_years_gis', 'city', 'district', 'state')

    # Add filters to the sidebar for these fields
    list_filter = ('regis_date','state', 'district', 'city', 'specialization_subject', 'experience_years_gis')

    # Optional: Add search functionality for easier search in the admin panel
    search_fields = ('name', 'email', 'phone_number', 'specialization_subject', 'institution', 
                     'city', 'district', 'state')

# Register the model with the admin interface
admin.site.register(Course)
admin.site.register(MasterTrainer, MasterTrainerAdmin)
admin.site.register(Attendance)