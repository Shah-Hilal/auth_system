
from django.contrib import admin
from .models import Service

# Register the Service model with the admin site
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_price', 'service_package', 'service_tax', 'active')
    search_fields = ('service_name', 'service_package')
    list_filter = ('active',)
    list_editable = ('active',)  # Allows editing the 'active' field directly from the list view


