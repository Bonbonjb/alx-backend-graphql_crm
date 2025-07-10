#!/bin/bash

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
cd /home/brendajb/alx-backend-graphql_crm

DELETED_COUNT=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(id__in=Order.objects.values_list('customer_id', flat=True)).filter(created_at__lt=cutoff)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
" | tail -n 1)

echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
