from django.db import models


class Hairstyle(models.Model):
    """
    Pre-defined hairstyles available at the salon.
    Admin manages these through Django admin.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField(help_text="How long this service takes")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True, help_text="Image URL for this hairstyle")
    is_available = models.BooleanField(default=True, help_text="Is this style currently offered?")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (${self.price})"


class Appointment(models.Model):
    """
    Customer bookings created through the booking form.
    """
    # Customer information
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()

    # Appointment details
    hairstyle = models.ForeignKey(
        Hairstyle,
        on_delete=models.CASCADE,
        help_text="Selected hairstyle service"
    )
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=8)

    # Optional notes
    notes = models.TextField(blank=True, help_text="Special requests or notes")

    # Auto-generated timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.customer_name} - {self.hairstyle.name} on {self.appointment_date}"

    def get_cost(self):
        """Get the cost from the selected hairstyle"""
        return self.hairstyle.price


class Inquiry(models.Model):
    """
    Customer inquiries and questions submitted through contact form.
    """
    # Contact information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, help_text="Optional phone number")

    # Inquiry details
    subject = models.CharField(max_length=200)
    message = models.TextField()

    # Status tracking
    STATUS_CHOICES = [
        ('new', 'New'),
        ('replied', 'Replied'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Auto-generated fields
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']  # Newest first
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.name} - {self.subject}"