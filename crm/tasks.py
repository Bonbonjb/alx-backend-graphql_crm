from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    query = '''
        query {
            customers { id }
            orders { id totalAmount }
        }
    '''
    response = requests.post("http://127.0.0.1:8000/graphql/", json={"query": query})
    data = response.json()["data"]
    total_customers = len(data["customers"])
    total_orders = len(data["orders"])
    total_revenue = sum(order["totalAmount"] for order in data["orders"])

    with open("/tmp/crm_report_log.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")
