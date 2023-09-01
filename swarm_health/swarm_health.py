import subprocess
import requests
import os
from dotenv import load_dotenv

# Load environment vars from .env

load_dotenv()


def check_docker_swarm_health():
    try:
        # Use the Docker CLI to check the Swarm health
        result = subprocess.run(
            ["docker", "node", "ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            # Docker Swarm is healthy
            print("Docker Swarm is healthy.")
            print(result.stdout)
        else:
            # Docker Swarm is not healthy
            print("Docker Swarm is not healthy. Error:")
            print(result.stderr)

        unavailable_nodes = [
            line for line in result.stdout.splitlines() if "Unavailable" in line]
        # Check for unavailable nodes

        if unavailable_nodes:
            print("One or more nodes are unavailable. Sending a curl request...")

            # Replace with your actual username and password
            username = os.getenv("NTFY_USERNAME")
            password = os.getenv("NTFY_PASSWORD")

            # Replace with the appropriate URL for your curl command
            url = os.getenv("NTFY_SERVER_STATUS_URL")

            # Data to send in the POST request
            data = f"{result.stdout}"

            # Send a curl request to notify about the unavailable nodes
            response = requests.post(url, auth=(username, password), data=data)

            if response.status_code == 200:
                print("Curl request sent successfully.")
            else:
                print(
                    f"Failed to send curl request. Status code: {response.status_code}")
        else:
            print("All nodes are healthy!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    check_docker_swarm_health()
