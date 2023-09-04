import subprocess
import requests
import os
from dotenv import load_dotenv

# Load environment vars from .env
load_dotenv()

# List of manager nodes to try
manager_nodes = ["manager1", "manager2", "manager3"]


def run_docker_command(node):
    try:
        # Use the Docker CLI to check the Swarm health on the specified node
        result = subprocess.run(
            ["docker", "-H",
                f"ssh://{node}:22/var/run/docker.sock", "node", "ls"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            # Docker Swarm on this node is healthy
            print(f"Docker Swarm on {node} is healthy.")
            print(result.stdout)
        else:
            # Docker Swarm on this node is not healthy
            print(f"Docker Swarm on {node} is not healthy. Error:")
            print(result.stderr)

        unavailable_nodes = [
            line for line in result.stdout.splitlines() if "Unavailable" in line
        ]

        if unavailable_nodes:
            print(
                f"One or more nodes on {node} are unavailable. Sending a curl request...")

            # Replace with your actual username and password
            username = os.getenv("NTFY_USERNAME")
            password = os.getenv("NTFY_PASSWORD")

            # Replace with the appropriate URL for your curl command
            url = os.getenv("NTFY_SERVER_STATUS_URL")

            # Data to send in the POST request
            data = f"{result.stdout}"

            # Send a curl request to notify about the unavailable nodes on this node
            response = requests.post(url, auth=(username, password), data=data)

            if response.status_code == 200:
                print(f"Curl request sent successfully for {node}.")
            else:
                print(
                    f"Failed to send curl request for {node}. Status code: {response.status_code}")
        else:
            print(f"All nodes on {node} are healthy!")

    except Exception as e:
        print(f"An error occurred on {node}: {str(e)}")


def check_docker_swarm_health():
    for node in manager_nodes:
        if run_docker_command(node):
            break


if __name__ == "__main__":
    check_docker_swarm_health()
