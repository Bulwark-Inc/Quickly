from django.shortcuts import render
from .models import Feature, AboutBullet, OverviewStep, Testimonial, PricingOption

def home_view(request):
    context = {
        'user': request.user,
        'features': Feature.objects.all(),
        'about_bullets': AboutBullet.objects.all(),
        'overview_steps': OverviewStep.objects.all(),
        'testimonials': Testimonial.objects.all(),
        'pricing_options': PricingOption.objects.all(),
    }
    return render(request, 'home/home.html', context)

def about_view(request):
    return render(request, 'home/about.html')

def contact_view(request):
    return render(request, 'home/contact.html')

def privacy_view(request):
    policy_sections = [
        {
            "title": "1. Information We Collect",
            "content": """
                <ul>
                    <li>Your name, email address, and contact information.</li>
                    <li>Payment data to process your academic transactions.</li>
                    <li>Device & browser details via cookies and analytics tools.</li>
                </ul>
            """
        },
        {
            "title": "2. How We Use Your Information",
            "content": """
                <ul>
                    <li>To process payments securely and notify you via email/WhatsApp.</li>
                    <li>To personalize your experience and improve service delivery.</li>
                    <li>To show relevant ads using Google AdSense.</li>
                </ul>
            """
        },
        {
            "title": "3. Google AdSense & Cookies",
            "content": """
                <p>We use Google AdSense which may use cookies to serve personalized ads. You can opt out at 
                <a href='https://www.google.com/settings/ads' target='_blank' class='underline'>Google Ads Settings</a>.</p>
            """
        },
        {
            "title": "4. Data Security",
            "content": """
                <p>We apply strong encryption and secure hosting protocols to protect your data against unauthorized access, alteration, or deletion.</p>
            """
        },
        {
            "title": "5. Your Rights",
            "content": """
                <ul>
                    <li>Access, edit, or delete your personal data anytime.</li>
                    <li>Opt out of tracking or email communications.</li>
                </ul>
            """
        },
        {
            "title": "6. Policy Updates",
            "content": """
                <p>This privacy policy may be updated from time to time. We will notify users via email or an in-app message when changes occur.</p>
            """
        },
    ]
    return render(request, 'home/privacy.html', {'policy_sections': policy_sections})

def terms_view(request):
    return render(request, 'home/terms.html')