import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from home.models import Feature, AboutBullet, OverviewStep, Testimonial


# ---- Static Data to Insert ----

ABOUT_BULLETS = [
    {"icon": "zap", "title": "Fast Setup", "text": "Get started in minutes - no tech skills required."},
    {"icon": "headphones", "title": "Reliable Support", "text": "24/7 availability to help you when you need it most."},
    {"icon": "bar-chart-3", "title": "Performance Insights", "text": "Track what has been paid and manage contributions effortlessly."},
]

FEATURES = [
    {'icon': 'credit-card', 'title': 'Flexible Payments', 'text': 'Pay using secure bank transfers or Paystack - the choice is yours.'},
    {'icon': 'check-circle', 'title': 'Seamless Tracking', 'text': 'See your payment status and history in one organized dashboard.'},
    {'icon': 'shield', 'title': 'Reliable & Secure', 'text': 'Your data and transactions are encrypted and protected.'},
    {'icon': 'zap', 'title': 'Fast Processing', 'text': 'We make your school payments quickly so you don’t miss deadlines.'},
    {'icon': 'layout-dashboard', 'title': 'Simple Dashboard', 'text': 'An easy-to-use interface to view, manage, and track your payments.'},
    {'icon': 'users', 'title': 'Built for Students', 'text': 'Designed with you in mind - no technical jargon, just results.'},
]

OVERVIEW_STEPS = [
    {
        'icon': 'user-plus',
        'title': 'Register an Account',
        'desc': 'Begin by creating your account on our platform. Just head over to the registration page, fill in your details, and set a secure password. It takes less than a minute to get started with Quickly!'
    },
    {
        'icon': 'mail-check',
        'title': 'Confirm Your Email',
        'desc': 'After registering, check your email inbox for a confirmation message. Click the verification link to activate your account. Didn’t receive the email? You can easily request a new one from your dashboard.'
    },
    {
        'icon': 'log-in',
        'title': 'Login to Your Dashboard',
        'desc': 'Once your email is confirmed, sign in using your registered email and password. This takes you to your personalized dashboard where you can track your payment status and update your information.'
    },
    {
        'icon': 'edit-3',
        'title': 'Update Your Info',
        'desc': 'To ensure smooth communication, please provide your school portal password (for verification) and a valid WhatsApp number. This helps us reach you quickly and deliver services efficiently.'
    },
    {
        'icon': 'credit-card',
        'title': 'Make a Payment',
        'desc': 'When you’re ready, proceed to make your payment using our secure platform. You can choose between direct bank transfer or Paystack for a fast, reliable experience. Your data is always encrypted.'
    },
    {
        'icon': 'receipt',
        'title': 'Receive Your Receipt',
        'desc': 'Once payment is confirmed, we’ll automatically generate your receipt. You’ll receive a digital copy via email and WhatsApp, and we can also arrange a printed version if required.'
    },
]

TESTIMONIALS = [
    {
        'quote': '“Quickly helped me automate my workflow and reclaim hours every week.”',
        'name': 'Jane Doe',
        'role': 'Entrepreneur',
    },
    {
        'quote': '“Intuitive, clean, and very responsive. Plus, the support team is amazing.”',
        'name': 'John Smith',
        'role': 'Startup Founder',
    },
    {
        'quote': '“The best investment I’ve made in my business tools this year.”',
        'name': 'Alice Johnson',
        'role': 'Business Coach',
    },
]

PRICING_ENTRIES = [
    {
        'title': 'Single Payment',
        'headline': '₦1,000 – ₦2,000',
        'description': 'For one-time payment assistance.',
        'features': '\n'.join([
            '₦1k for payments < ₦50k',
            '₦1.5k for ₦50k – ₦99,999',
            '₦2k for ₦100k and above',
        ]),
        'cta_text': 'Get Started',
        'cta_link': '/register/'  # or keep blank if you want template tag
    },
    {
        'title': 'Two Payments',
        'headline': '₦1,000 – ₦1,500 per payment',
        'description': "Ideal if you're making two different payments.",
        'features': '\n'.join([
            '₦1k each ≤ ₦100k',
            '₦1.5k each > ₦100k',
            'Separate receipts for each',
        ]),
        'cta_text': 'Start Now',
        'cta_link': '/register/'
    },
    {
        'title': '3+ Payments',
        'headline': '20% Discount',
        'description': 'Let us handle 3 or more payments and enjoy automatic discounts.',
        'features': '\n'.join([
            '20% off total service fee',
            'Priority processing',
            'Grouped receipt delivery',
        ]),
        'cta_text': 'Pay Less Now',
        'cta_link': '/register/'
    },
]

# ---- Population Functions ----

def populate_about_bullets():
    print("Populating AboutBullet...")
    AboutBullet.objects.all().delete()
    for bullet in ABOUT_BULLETS:
        AboutBullet.objects.create(**bullet)
        print(f"✓ Created AboutBullet: {bullet['title']}")
    print("Done.\n")

def populate_features():
    print("Populating Feature...")
    Feature.objects.all().delete()
    for feature in FEATURES:
        Feature.objects.create(**feature)
        print(f"✓ Created Feature: {feature['title']}")
    print("Done.\n")

def populate_overview_steps():
    print("Populating OverviewStep...")
    OverviewStep.objects.all().delete()
    for i, step in enumerate(OVERVIEW_STEPS, start=1):
        OverviewStep.objects.create(order=i, **step)
        print(f"✓ Created OverviewStep: {step['title']}")
    print("Done.\n")

def populate_testimonials():
    print("Populating Testimonial...")
    Testimonial.objects.all().delete()
    for testimonial in TESTIMONIALS:
        Testimonial.objects.create(**testimonial)
        print(f"✓ Created Testimonial: {testimonial['name']}")
    print("Done.\n")

def populate_pricing_options():
    from home.models import PricingOption

    print("Populating PricingOptions...")
    PricingOption.objects.all().delete()

    for entry in PRICING_ENTRIES:
        PricingOption.objects.create(
            title=entry['title'],
            headline=entry['headline'],
            description=entry['description'],
            features=entry['features'],
            cta_text=entry['cta_text'],
            cta_link=entry['cta_link']
        )
        print(f"Created PricingOption: {entry['title']}")
    print("Done.\n")

# ---- CLI Interface ----

def run():
    print("📦 Which model do you want to populate?")
    print("1. AboutBullet")
    print("2. Feature")
    print("3. OverviewStep")
    print("4. Testimonial")
    print("5. Pricing")
    print("0. All")

    choice = input("Enter your choice (1/2/3/4/0): ").strip()

    if choice == '1':
        populate_about_bullets()
    elif choice == '2':
        populate_features()
    elif choice == '3':
        populate_overview_steps()
    elif choice == '4':
        populate_testimonials()
    elif choice == '5':
        populate_pricing_options()
    elif choice == '0':
        populate_about_bullets()
        populate_features()
        populate_overview_steps()
        populate_testimonials()
        populate_pricing_options()
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    run()
