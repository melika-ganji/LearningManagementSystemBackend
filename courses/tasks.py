from celery import shared_task
from django.utils.timezone import now
from courses.models import Purchase, RevenueReport
from django.db import models

@shared_task
def calculate_total_revenue():
    today = now().date()
    total_revenue = Purchase.objects.filter(purchase_date__date=today).aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0

    # Save revenue report
    RevenueReport.objects.create(date=today, total_revenue=total_revenue)

    return f"Total revenue calculated for {today}: {total_revenue}"
