from django.db import models

class Service(models.Model):
    service_name = models.CharField(max_length=255)
    payment_terms = models.TextField()  # Removed default
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_package = models.CharField(max_length=255)  # Removed default
    service_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    service_image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name

class Subscription(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Ensure this is calculated correctly
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.service.service_name} - {self.payment_status}"
