import requests
import csv

def get_structured_data(url):
    """Retrieves the JSON content from the specified URL."""

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        
        if url.endswith(".csv"):
            data = csv.reader(response.text.splitlines())
            # make json object. header as key and rest as array of values
            json_data = {}
            for i, row in enumerate(data):
                if i == 0:
                    headers = row
                    continue
                json_data[i] = dict(zip(headers, row))
            return json_data
        else:
          return response.json()  # Assuming the response is JSON

    except requests.exceptions.RequestException as e:
        print(f"Error: {type(e).__name__} - {e}")
        return None

def get_user_input():
    """Prompts the user for link, method, and optional headers."""
    while True:
        link = input("Enter the URL: ")
        if not link:
            print("Please enter a valid URL.")
            continue

        method = input("Enter the request method (GET, POST, or others): ").upper().strip()
        if method not in ("GET", "POST"):
            print(f"Warning: '{method}' method is not common. Are you sure you want to proceed?")
            confirmation = input("y/N: ")
            if confirmation.lower() != "y":
                continue

        headers = input("Enter additional headers (separate key-value pairs with commas): ").strip()
        headers_dict = {}
        if headers:
            for pair in headers.split(","):
                key, value = pair.strip().split(":", 1)
                headers_dict[key.strip()] = value.strip()

        return link, method, headers_dict

def send_request(link, method, headers=None):
    """Sends a request to the specified URL using the given method and headers."""
    try:
        response = requests.request(method, link, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error: {type(e).__name__} - {e}")
        return None

def main():
    """Executes the main program loop."""
    while True:
        link, method, headers = get_user_input()
        response = send_request(link, method, headers)

        if response:
            print("Status Code:", response.status_code)
            print("Headers:")
            for key, value in response.headers.items():
                print(f"{key}: {value}")

            # Optionally handle different content types (e.g., HTML, JSON)
            content_type = response.headers.get('Content-Type', None)
            if content_type and content_type.startswith('text/'):
                print("Content:")
                print(response.text[:100] + ("..." if len(response.text) > 100 else ""))  # Truncate long content
            else:
                print("Content may be binary or of a different format.")

        print("\nWould you like to make another request? (y/N): ")
        if input().lower() != "y":
            break

if __name__ == "__main__":
    main()

# Optional comment for attribution
# # This script was written by Bard, a large language model from Google AI.
