#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Configure logging
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Setup GraphQL client
transport = RequestsHTTPTransport(
    url='http://localhost:8000/api/graphql/',
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Define the date range
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')

# GraphQL query
query = gql(f"""
query {{
  orders(orderDate_Gte: "{seven_days_ago}", orderDate_Lte: "{today}") {{
    id
    customer {{
      email
    }}
  }}
}}
""")

try:
    result = client.execute(query)
    with open(log_file, 'a') as log:
        for order in result.get("orders", []):
            order_id = order["id"]
            customer_email = order["customer"]["email"]
            log.write(f"{timestamp} - Reminder for Order #{order_id} to {customer_email}\n")
    print("Order reminders processed!")
except Exception as e:
    with open(log_file, 'a') as log:
        log.write(f"{timestamp} - Error: {str(e)}\n")
    print("Order reminder script failed:", e)
