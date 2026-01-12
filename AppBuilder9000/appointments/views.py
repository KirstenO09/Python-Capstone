from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment, Hairstyle, Inquiry
from .forms import AppointmentForm, InquiryForm
import requests
from django.conf import settings
from django.shortcuts import render
from bs4 import BeautifulSoup
import re

def home(request):
    """
    Landing page showing available hairstyles with images.
    This is what customers see first.
    """
    hairstyles = Hairstyle.objects.filter(is_available=True)
    return render(request, 'appointments/home.html', {'hairstyles': hairstyles})


def create_appointment(request):
    """
    Customer booking form.
    Can pre-select hairstyle from URL parameter (when clicking "Book This Style").
    """
    # Check if a hairstyle was pre-selected from the home page
    preselected_hairstyle_id = request.GET.get('hairstyle')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(
                request,
                f'Appointment booked successfully! Total cost: ${appointment.get_cost()}'
            )
            return redirect('appointment_confirmation', pk=appointment.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form if hairstyle was selected from home page
        if preselected_hairstyle_id:
            form = AppointmentForm(initial={'hairstyle': preselected_hairstyle_id})
        else:
            form = AppointmentForm()

    return render(request, 'appointments/create.html', {'form': form})


def appointment_confirmation(request, pk):
    """
    Confirmation page shown after successful booking.
    Shows all details and total cost.
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/confirmation.html', {'appointment': appointment})


def appointment_list(request):
    """
    Admin view - list all appointments.
    Shows all bookings in a table.
    """
    appointments = Appointment.objects.all().select_related('hairstyle')
    return render(request, 'appointments/list.html', {'appointments': appointments})


def update_appointment(request, pk):
    """
    Edit an existing appointment.
    Customer can change date, time, or hairstyle.
    """
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/update.html', {
        'form': form,
        'appointment': appointment
    })


def delete_appointment(request, pk):
    """
    Cancel an appointment.
    Shows confirmation before deleting.
    """
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointment_list')

    return render(request, 'appointments/delete.html', {'appointment': appointment})


def contact(request):
    """
    Contact form for customer inquiries.
    """
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            messages.success(
                request,
                'Thank you for your inquiry! We will get back to you within 24 hours.'
            )
            return redirect('contact_confirmation', pk=inquiry.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InquiryForm()

    return render(request, 'appointments/contact.html', {'form': form})


def contact_confirmation(request, pk):
    """
    Confirmation page after submitting inquiry.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    return render(request, 'appointments/contact_confirmation.html', {'inquiry': inquiry})

def inspiration_gallery(request):
    """
    Fetch hairstyle inspiration photos from Pixabay API
    Displays searchable photo gallery with pagination
    """
    # Get search query from GET parameter, default to 'hairstyles'
    query = request.GET.get('search', 'hairstyles')
    page = request.GET.get('page', '1')

    # Pixabay API endpoint
    url = 'https://pixabay.com/api/'

    # Query parameters - Pixabay uses simple URL parameters
    params = {
        'key': settings.PIXABAY_API_KEY,  # API key authentication
        'q': query,  # Search query
        'page': page,  # Page number
        'per_page': 15,  # Results per page (max 200)
        'image_type': 'photo',  # Only photos, not illustrations
        'orientation': 'vertical',  # Portrait orientation for hairstyles
        'safesearch': 'true',  # Filter inappropriate content
    }

    try:
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse JSON response
        data = response.json()

        # Pixabay returns 'hits' instead of 'results'
        photos = data.get('hits', [])
        total = data.get('totalHits', 0)

        # Calculate total pages (max 500 results due to Pixabay limitation)
        per_page = 15
        total_pages = min((total + per_page - 1) // per_page, 34)  # Pixabay max ~500 results

        context = {
            'photos': photos,
            'total': total,
            'total_pages': total_pages,
            'page': int(page),
            'query': query,
        }

    except requests.exceptions.RequestException as e:
        # Handle errors gracefully
        context = {
            'error': 'Unable to fetch images. Please try again later.',
            'photos': [],
            'query': query,
            'page': int(page)
        }
        # Log error for debugging
        print(f"Pixabay API Error: {e}")

        print(f"Photos: {len(photos)}")  # Add this
        print(f"Query: {query}")  # Add this
        print(f"Error: {context.get('error')}")  # Add this

    return render(request, 'appointments/inspiration_gallery.html', context)

def natural_hair_tips(request):
    SOURCE_URL = "https://www.beautycon.com/article/heat-damage-101-how-long-will-it-take-to-get-your-curls-back"

    tips = []
    error = None

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Main article container
        article = soup.select_one("section#primary.content-area") or soup.select_one("#primary")

        if not article:
            error = "Could not find article content on the source page."
        else:
            # Look at all H2/H3 headings: Month 1, Month 6, One year, etc.
            for heading in article.find_all(["h2", "h3"]):
                title = heading.get_text(strip=True)
                if not title:
                    continue

                body_parts = []

                # Collect everything after this heading until the next heading
                for sibling in heading.next_siblings:
                    name = getattr(sibling, "name", None)

                    if name in ["h2", "h3"]:
                        break

                    # Paragraph text
                    if name == "p":
                        text = sibling.get_text(" ", strip=True)
                        if text:
                            body_parts.append(text)

                    # (Optional) if the page uses real lists too
                    if name in ["ul", "ol"]:
                        for li in sibling.find_all("li"):
                            li_text = li.get_text(" ", strip=True)
                            if li_text:
                                body_parts.append(f"• {li_text}")

                if body_parts:
                    # Join all segments into one big string
                    body = " ".join(body_parts)

                    # 🔥 NOW force line breaks before each bullet character
                    # e.g. "... are: • A • B" -> "... are:<br>• A<br>• B"
                    body = re.sub(r"\s*•\s*", r"<br>• ", body)

                    tips.append(
                        {
                            "title": title,
                            "body": body,  # contains <br> tags now
                        }
                    )

            # Optional: limit number of sections
            tips = tips[:10]

    except Exception as e:
        print("Error scraping natural hair tips:", e)
        error = "Sorry, we couldn’t load the natural hair tips right now."

    context = {
        "tips": tips,
        "source_url": SOURCE_URL,
        "error": error,
    }
    return render(request, "appointments/natural_hair_tips.html", context)


