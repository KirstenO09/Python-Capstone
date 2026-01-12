from django import forms
from .models import Appointment, Hairstyle, Inquiry

# Time slot choices for the dropdown
TIME_SLOTS = [
    ('09:00', '9:00 AM'),
    ('09:30', '9:30 AM'),
    ('10:00', '10:00 AM'),
    ('10:30', '10:30 AM'),
    ('11:00', '11:00 AM'),
    ('11:30', '11:30 AM'),
    ('12:00', '12:00 PM'),
    ('12:30', '12:30 PM'),
    ('13:00', '1:00 PM'),
    ('13:30', '1:30 PM'),
    ('14:00', '2:00 PM'),
    ('14:30', '2:30 PM'),
    ('15:00', '3:00 PM'),
    ('15:30', '3:30 PM'),
    ('16:00', '4:00 PM'),
    ('16:30', '4:30 PM'),
    ('17:00', '5:00 PM'),
]


class AppointmentForm(forms.ModelForm):
    # Override time field to use dropdown choices
    appointment_time = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['customer_name', 'customer_email', 'hairstyle',
                  'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'hairstyle': forms.Select(attrs={
                'class': 'form-control'
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker (built-in calendar!)
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests? (optional)'
            }),
        }
        labels = {
            'customer_name': 'Your Name',
            'customer_email': 'Email Address',
            'hairstyle': 'Select Hairstyle',
            'appointment_date': 'Preferred Date',
            'appointment_time': 'Preferred Time',
            'notes': 'Special Requests'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available hairstyles in the dropdown
        self.fields['hairstyle'].queryset = Hairstyle.objects.filter(is_available=True)

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 123-4567 (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is your inquiry about?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Please describe your question or concern...'
            }),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'subject': 'Subject',
            'message': 'Your Message'
        }