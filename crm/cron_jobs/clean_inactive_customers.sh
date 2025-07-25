#!/bin/bash

# Determine current working directory using BASH_SOURCE
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cwd=$(pwd)

# Move to project root (assumes script is in crm/cron_jobs)
if [ -d "$SCRIPT_DIR/../.." ]; then
    cd "$SCRIPT_DIR/../.."
else
    echo "Could not change to project root from $SCRIPT_DIR"
    exit 1
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Run Django shell command to delete inactive customers
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

# Log the result
if [ -n "$DELETED_COUNT" ]; then
    echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$TIMESTAMP - Error: DELETED_COUNT is empty" >> /tmp/customer_cleanup_log.txt
fi
