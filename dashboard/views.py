from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payments.models import PaymentRecord  # import your model

@login_required
def dashboard_view(request):
    user = request.user

    payment_records = PaymentRecord.objects.filter(user=user).select_related('fee_type').order_by('-date_paid')

    context = {
        "user": user,
        "payment_records": payment_records
    }

    return render(request, 'dashboard/dashboard.html', context)
