from django.shortcuts import render

def home_view(request):
    user = request.user

    about_bullets = [
        {
            "icon": "zap",
            "title": "Fast Setup",
            "text": "Get started in minutes - no tech skills required."
        },
        {
            "icon": "headphones",
            "title": "Reliable Support",
            "text": "24/7 availability to help you when you need it most."
        },
        {
            "icon": "bar-chart-3",
            "title": "Performance Insights",
            "text": "Track what has been paid and manage contributions effortlessly."
        },
    ]
    features = [
        {
            'icon': 'credit-card',
            'title': 'Flexible Payments',
            'text': 'Pay using secure bank transfers or Paystack - the choice is yours.'
        },
        {
            'icon': 'check-circle',
            'title': 'Seamless Tracking',
            'text': 'See your payment status and history in one organized dashboard.'
        },
        {
            'icon': 'shield',
            'title': 'Reliable & Secure',
            'text': 'Your data and transactions are encrypted and protected.'
        },
        {
            'icon': 'zap',
            'title': 'Fast Processing',
            'text': 'We make your school payments quickly so you don’t miss deadlines.'
        },
        {
            'icon': 'layout-dashboard',
            'title': 'Simple Dashboard',
            'text': 'An easy-to-use interface to view, manage, and track your payments.'
        },
        {
            'icon': 'users',
            'title': 'Built for Students',
            'text': 'Designed with you in mind - no technical jargon, just results.'
        },
    ]
    overview_steps = [
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
    testimonials = [
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

    context = {
        'user': user,
        'features': features,
        'about_bullets': about_bullets,
        'overview_steps': overview_steps,
        'testimonials': testimonials,
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