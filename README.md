
# Cloudflare Dynamic DNS Updater

This Python script automatically updates your Cloudflare DNS records with your current public IP address whenever it changes.

## Features
- Automatically detects IP changes: The script checks your public IP and compares it to the last recorded IP.
- Updates all 'A' type records: If a change is detected, it updates all 'A' type DNS records in the specified zone to the new IP.
- Securely stores credentials: Cloudflare API credentials are stored in a separate JSON file for security.
- User-friendly setup: The script guides you through the initial setup process, including entering your Cloudflare credentials.
- Clear logging: The script provides informative messages about its actions, such as success or failure of DNS updates.

## Requirements
- Python 3.x
- requests library (pip install requests)

## Setup
1. Obtain Cloudflare API credentials:
- Log in to your Cloudflare account.
- Go to My Profile > API Tokens.
- Create a new API token with the Zone.Zone and DNS.Edit permissions.
- Copy the API key and your Cloudflare email address.

2. Install the required library:
``` Bash
pip install requests
```

3. Run the script:

```Bash
python update.py
```

The script will prompt you for your Cloudflare Zone ID, email, and API key if the credentials file doesn't exist.

4. (Optional) Set up a cron job or create a service or use task scheduler in Windows:
To automate the script's execution, set up a cron job to run it at regular intervals (e.g., every hour).

## Usage
- The script will automatically check for IP changes and update DNS records accordingly.
- You can manually trigger a DNS update by running the script again.

## Additional Notes
- The script stores the last recorded IP in a file named last_ip.txt.
- The script stores Cloudflare credentials in a file named credentials.json. **Keep this file secure.**
- For more advanced usage, refer to the Cloudflare API documentation: https://api.cloudflare.com/

## License

This project is licensed under the [The MIT License](https://mit-license.org/) - see the [LICENSE](LICENSE) file for details.