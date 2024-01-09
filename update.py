import requests
import os
import json

# Function to get the public IP address
def get_public_ip():
    response = requests.get('https://httpbin.org/ip')
    if response.status_code == 200:
        return response.json().get('origin')
    else:
        print('Failed to fetch IP address')
        return None

# Function to read the last recorded IP from a file
def read_last_ip(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    return None

# Function to save the current IP to a file
def save_current_ip(file_path, current_ip):
    with open(file_path, 'w') as file:
        file.write(current_ip)

# Function to update all 'A' type DNS records to current IP if it has changed
def update_dns_if_ip_changed(ip_file_path, zone_id, api_key, email):
    current_ip = get_public_ip()
    if not current_ip:
        print("Could not retrieve current IP. Aborting DNS update.")
        return

    last_ip = read_last_ip(ip_file_path)
    if current_ip != last_ip:
        save_current_ip(ip_file_path, current_ip)
        update_all_a_records(zone_id, api_key, email, current_ip)
    else:
        print("IP has not changed. Skipping DNS update.")

# Function to update all 'A' type DNS records to current IP
def update_all_a_records(zone_id, api_key, email, current_ip):
    if not current_ip:
        print("Could not retrieve current IP. Aborting DNS update.")
        return

    # Fetch all 'A' type DNS records for the specified zone
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": email,
        "X-Auth-Key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dns_records = response.json()["result"]
        for record in dns_records:
            record_id = record["id"]
            payload = {
                "content": current_ip,
                "name": record["name"],
                "proxied": record["proxied"],
                "type": record["type"],
                "ttl": record["ttl"]
            }
            update_dns_record(zone_id, api_key, email, record_id, payload)
    else:
        print("Failed to fetch DNS records")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

# Function to update DNS record
def update_dns_record(zone_id, api_key, email, record_id, payload):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": email,
        "X-Auth-Key": api_key
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"DNS record for ID {record_id} updated successfully!")
        print(response.json())
    else:
        print(f"Failed to update DNS record for ID {record_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

# Check if the IP file exists and read the last recorded IP
ip_file_path = 'last_ip.txt'

# Check if the credentials file exists and read the credentials
credentials_file_path = 'credentials.json'

# If credentials file doesn't exist, prompt user for information and save it to the file
if not os.path.exists(credentials_file_path):
    zone_id = input("Enter your Zone ID: ")
    auth_email = input("Enter your Cloudflare email: ")
    auth_key = input("Enter your Cloudflare API key: ")

    credentials = {
        "zone_id": zone_id,
        "auth_email": auth_email,
        "auth_key": auth_key
    }

    with open(credentials_file_path, 'w') as file:
        json.dump(credentials, file)
else:
    # Read credentials from the file
    with open(credentials_file_path, 'r') as file:
        credentials = json.load(file)
        zone_id = credentials.get("zone_id")
        auth_email = credentials.get("auth_email")
        auth_key = credentials.get("auth_key")

        # Call the update_dns_if_ip_changed function
        update_dns_if_ip_changed(ip_file_path, zone_id, auth_key, auth_email)
