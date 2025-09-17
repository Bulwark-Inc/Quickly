from django.shortcuts import render

def home_view(request):
    user = request.user

    features = [
        {
            'icon': 'settings',
            'title': 'Fully Customizable',
            'text': 'Easily tailor features to match your unique workflow and needs.'
        },
        {
            'icon': 'link-2',
            'title': 'App Integration',
            'text': 'Seamlessly connect Quickly with the tools you already use and love.'
        },
        {
            'icon': 'box',
            'title': 'Drag & Drop',
            'text': 'Build layouts and organize content easily with our intuitive editor.'
        },
    ]

    about_bullets = [
        {"icon": "check", "text": "Quick setup in minutes — no tech skills needed."},
        {"icon": "headphones", "text": "24/7 support whenever you need assistance."},
        {"icon": "bar-chart-3", "text": "Powerful analytics to track performance and growth."},
    ]

    overview_steps = [
        {
            'icon': 'download',
            'title': 'Install the Software',
            'desc': 'Sign up and set up your account in just minutes.',
        },
        {
            'icon': 'user-cog',
            'title': 'Customize Your Profile',
            'desc': 'Set your preferences and personalize your dashboard.',
        },
        {
            'icon': 'rocket',
            'title': 'Start Using Quickly',
            'desc': 'Access features that help you work smarter and grow faster.',
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
