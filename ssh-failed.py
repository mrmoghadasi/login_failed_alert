import re
import requests
import time
import socket
import smtplib

# Change these to the URL of the webhook you want to call
webhook_url = "https://Rocket.Chat/hooks/***********************"


# Change these to your email settings
smtp_server = "mail.domain.com"
smtp_port = 587
smtp_username = "monitor@domain.com"
smtp_password = "************"
sender_email = "monitor@domain.com"
recipient_email = "user@domain.com"


# SSH log file path
log_path = "/var/log/auth.log"

# Regular expression to match failed SSH login attempts
regex_pattern = r"Failed password for.*from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (\d+)"

# Get hostname of server
hostname = socket.gethostname()

def tail(file_path):
    """
    Generator that yields new lines appended to a file.
    """
    with open(file_path, "r") as f:
        # Start at end of file
        f.seek(0, 2)

        while True:
            line = f.readline()

            if not line:
                # Wait for more data
                time.sleep(0.1)
                continue

            yield line

def call_webhook(username, ip_address, port, hostname):
    """
    Calls the webhook with the relevant information about the failed login attempt.
    """
    payload = {
        "alias": "SSH Failed Login",
        "attachments": [
            {
                "title": "SSH Failed Login To Server {}".format(hostname),
                "text": "Failed SSH login attempt by user {} from IP address {} on port {} at {}".format(
                    username, ip_address, port, time.strftime("%Y-%m-%d %H:%M:%S")
                ),
                "color": "#FF0000"
            }
        ]
    }
    headers = {
        "Content-type": "application/json"
    }
    requests.post(webhook_url, json=payload, headers=headers)



def send_email(username, ip_address, port, hostname):
    """
    Sends an email notification about the failed login attempt.
    """
    subject = "SSH Failed Login To Server {}".format(hostname)
    body = "Failed SSH login attempt by user {} from IP address {} on port {} at {}".format(
        username, ip_address, port, time.strftime("%Y-%m-%d %H:%M:%S")
    )
    message = "Subject: {}\n\n{}".format(subject, body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message)



# Start tailing the SSH log file
for line in tail(log_path):
    # Check if line matches regex pattern
    match = re.search(regex_pattern, line)

    if match:
        # Get IP address and port from regex match
        ip_address = match.group(1)
        port = match.group(2)

        # Get user and date/time
        user = line.split(" ")[8]
        date_time = line.split(" ")[0] + " " + line.split(" ")[1] + " " + line.split(" ")[2]

        # Call webhook with IP address, port, user, date/time, and title
        call_webhook(user, ip_address, port,hostname)
        send_email(user, ip_address, port,hostname)
