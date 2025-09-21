# Quickly

A Django-based Payment & Dashboard System tailored for Abia State University Medical Teaching Hospital to streamline student fee management, profile updates, and payment processing.
Overview
Quickly is a web application designed to simplify fee payments and user profile management for students at Abia State University Medical Teaching Hospital. It supports:
Tiered fee pricing with flexible business rules.
Multi-payment options: single, two-installment, and multi-installments with discounts.
Secure payment processing via Paystack and bank transfers.
User dashboard with profile picture upload, phone number, and portal password management.
Admin control panel for fee and payment management.
Responsive UI leveraging Tailwind CSS, Alpine.js, AOS, and Lucide icons.
Smooth user experience with multi-step payment flows and clear messaging.

## Tech Stack
- Backend: Django
- Frontend: Tailwind CSS, Alpine.js, AOS, Lucide icons, Splide.js
- Database: MySQL (Production)
- Testing: Pytest
- Deployment: PythonAnywhere (backend), potential frontend fragments deployed on Vercel/Netlify

## Features
Dynamic Fee Management: Admin can add/edit fee types, amounts, and service charges without touching code.
Tiered Pricing Logic: Automatically adjusts fees based on payment amount and number of installments.
Multiple Payment Methods: Paystack integration for instant payments and bank transfer uploads for manual verification.
User Dashboard: Displays profile info, payment history, and prompts users to update missing profile details.
Secure File Uploads: Handles proof of payment uploads with validation for file type and size.
Responsive & Accessible UI: Ensures usability across devices with smooth animations and modern UI components.

## Installation & Setup
### Prerequisites:
- Python 3.8+
- Django
- Node
- MySQL server
- Virtualenv or similar environment manager
- Git

### Setup Instructions
1. Clone the repository:
```bash
git clone <repo_url>
cd quickly
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment variables:
Create a .env file or set environment variables for:
- DJANGO_SECRET_KEY
- DATABASE_URL or individual DB params
- PAYSTACK_PUBLIC_KEY
- PAYSTACK_SECRET_KEY
- PAYSTACK_CALLBACK_URL

5. Apply migrations:
```bash
python manage.py migrate
```

6. Create superuser for admin:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

8. Run the development server:
```bash
python manage.py runserver
```
9. Access the site:
Frontend: http://localhost:8000/
Admin panel: http://localhost:8000/admin/

## Testing
Run the test suite using Pytest:
```bash
pytest
```

## Deployment
- The backend is deployed on PythonAnywhere.
- Frontend static assets are served via Django.
- Future frontend components consuming the backend API may be deployed on Vercel or Netlify.

## License
This project is licensed under the MIT License
### Author
Developed and maintained solo by [Shiloh].