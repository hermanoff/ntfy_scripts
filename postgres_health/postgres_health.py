import requests
import os
from dotenv import load_dotenv

# Load environment vars from .env
load_dotenv()

# Define a list of manager nodes
manager_nodes = ['manager1', 'manager2', 'manager3']

# Function to check the health of a node
def check_node_health(node_url):
    try:
        response = requests.get(node_url)
        response.raise_for_status()
        data = response.json()
        return data['state'] == 'running'
    except Exception as e:
        return False

# Iterate through the list of manager nodes and check their health
unhealthy_nodes = []
for node in manager_nodes:
    node_url = f'http://{node}:8008/patroni'
    node_status = check_node_health(node_url)
    if node_status:
        print(f"{node} is healthy.")
    else:
        print(f"{node} is not healthy.")
        unhealthy_nodes.append(node)

# Check if any node is not healthy and send a report
if unhealthy_nodes:
    print("Cluster has one or more unhealthy nodes. Sending a report...")
    username = os.getenv("NTFY_USERNAME")
    password = os.getenv("NTFY_PASSWORD")
    url = os.getenv("NTFY_SERVER_STATUS_URL")
    data = f"Unhealthy nodes: {', '.join(unhealthy_nodes)}"
    
    try:
        response = requests.post(url, auth=(username, password), data=data)
        response.raise_for_status()
        print("Report sent successfully.")
    except Exception as e:
        print(f"Failed to send the report: {str(e)}")
else:
    print("Cluster is healthy.")

