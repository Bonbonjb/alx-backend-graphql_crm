from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/crm_heartbeat_log.txt"

    # Default message
    message = f"{timestamp} CRM is alive"

    # Set up GraphQL transport
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Define hello query
    query = gql("""
    query {
        hello
    }
    """)

    try:
        result = client.execute(query)
        hello_response = result.get("hello", "No hello response")
        message += f" | GraphQL says: {hello_response}"
    except Exception as e:
        message += f" | GraphQL ERROR: {str(e)}"

    # Write to log file
    with open(log_file, "a") as f:
        f.write(message + "\n")
