#!/usr/bin/env python3
import requests
import json
import os
import signal
import sys
from pprint import pprint  # For pretty printing of JSON responses

# Default Base URL
BASE_URL = "http://localhost:8000"
ENDPOINTS_FILE = "endpoints.json"
README_FILE = "README.md"
last_token = None  # To store the last Authorization token for reuse

def handle_sigint(signal_received, frame):
    """Handle the SIGINT signal (Ctrl + C) gracefully."""
    print("\nBye! See you next time!")
    sys.exit(0)

# Register the SIGINT handler
signal.signal(signal.SIGINT, handle_sigint)

def load_endpoints():
    """Load endpoints from the JSON file."""
    if os.path.exists(ENDPOINTS_FILE):
        with open(ENDPOINTS_FILE, "r") as file:
            try:
                return json.load(file) or []
            except json.JSONDecodeError:
                return []
    return []

def save_endpoints(endpoints):
    """Save endpoints to the JSON file."""
    with open(ENDPOINTS_FILE, "w") as file:
        json.dump(endpoints, file, indent=4)

def validate_base_url(url):
    """Ensure the base URL starts with http:// or https://"""
    if not url.startswith(("http://", "https://")):
        return "http://" + url  # Default to http if no scheme provided
    return url

def get_user_input(prompt, default=None, allowed_values=None, required=False):
    """Helper to get user input with a default value and optional validation."""
    while True:
        user_input = input(f"{prompt} [{default}]: ").strip()
        
        # Default handling
        if not user_input and default:
            user_input = default

        # Validate against allowed values
        if allowed_values:
            if user_input.lower() in allowed_values:
                return user_input.lower()
            else:
                print(f"Invalid input. Please enter one of the following: {', '.join(allowed_values)}")
        elif user_input:  # Ensure empty inputs are not allowed if required
            return user_input
        elif required:
            print("Input cannot be empty. Please provide a valid response.")
        else:
            return user_input  # Accept empty input if not required and no default

def add_headers():
    """Interactively add headers with suggestions."""
    global last_token
    headers = {}
    print("\n--- Add Headers ---")
    print("Suggested keys: Authorization, Content-Type, Accept")

    while True:
        header_key = input("Enter header key (or press Enter to finish): ").strip()
        if not header_key:
            break

        # Handle Authorization header specifically
        if header_key.lower() == "authorization":
            if last_token:
                token = input(f"Enter your token [{last_token}]: ").strip() or last_token
            else:
                token = input("Enter your token: ").strip()
            if not token.startswith("Bearer "):
                token = f"Bearer {token}"
            headers["Authorization"] = token
            last_token = token  # Update the token for future use
            print("Authorization header added with Bearer token.")
        else:
            header_value = input(f"Enter value for '{header_key}': ").strip()
            headers[header_key] = header_value

    if not headers:
        print("No headers were added.")
    else:
        print("Headers added successfully.")

    return headers

def select_endpoint(endpoints):
    """Allow the user to select or add an endpoint."""
    print("\n--- Select an Endpoint ---")
    if endpoints:
        for idx, endpoint in enumerate(endpoints, start=1):
            print(f"{idx}. {endpoint}")
        print(f"{len(endpoints) + 1}. Add a new endpoint")
    else:
        print("1. Add a new endpoint")

    while True:
        choice = get_user_input(f"Choose [1-{len(endpoints) + 1}]: ", required=True)
        try:
            choice = int(choice)
            if 1 <= choice <= len(endpoints) + 1:
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(endpoints) + 1}.")
        except ValueError:
            print("Please enter a valid number.")

    if choice == len(endpoints) + 1:
        new_endpoint = get_user_input("Enter a new endpoint (e.g., /api/example): ", required=True)
        if not new_endpoint.startswith("/"):
            new_endpoint = "/" + new_endpoint
        endpoints.append(new_endpoint)
        save_endpoints(endpoints)
        return new_endpoint
    else:
        return endpoints[choice - 1]

def make_request(endpoints):
    global BASE_URL

    print("\n--- API Request ---")
    endpoint = select_endpoint(endpoints)
    full_url = f"{BASE_URL}{endpoint}"

    method = get_user_input("Enter HTTP method (GET, POST, PUT, DELETE)", "GET", ["get", "post", "put", "delete"], required=True).upper()

    # Add headers
    headers = {}
    add_headers_prompt = get_user_input("Do you want to add headers? (yes/no)", "no", ["yes", "no"], required=True)
    if add_headers_prompt == "yes":
        headers = add_headers()

    # Add JSON data if needed
    data = None
    if method in ["POST", "PUT"]:
        add_data = get_user_input("Do you want to send JSON data? (yes/no)", "no", ["yes", "no"], required=True)
        if add_data == "yes":
            while True:
                try:
                    raw_data = input("Enter JSON data (as a dictionary): ").strip()
                    data = json.loads(raw_data)
                    break
                except json.JSONDecodeError:
                    print("Invalid JSON format. Please try again.")

    # Make the request
    try:
        response = None
        if method == "GET":
            response = requests.get(full_url, headers=headers)
        elif method == "POST":
            response = requests.post(full_url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(full_url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(full_url, headers=headers)

        # Print the response
        print("\n--- Response ---")
        print(f"Status Code: {response.status_code}")
        try:
            response_json = response.json()
            print("Response JSON:")
            pprint(response_json)
        except json.JSONDecodeError:
            print("Response Text:", response.text)

    except requests.RequestException as e:
        print(f"Error making the request: {e}")

def main():
    global BASE_URL

    print("Welcome to the Enhanced API Automation Script!")

    # Load saved endpoints
    endpoints = load_endpoints()

    # Update Base URL if needed
    base_url = get_user_input(f"Enter the base URL [{BASE_URL}]: ", BASE_URL)
    if base_url:
        BASE_URL = validate_base_url(base_url)

    while True:
        make_request(endpoints)
        another_request = get_user_input("\nDo you want to make another request? (yes/no): ", "yes", ["yes", "no"], required=True)
        if another_request != "yes":
            break

if __name__ == "__main__":
    main()
