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

# Notification Settings
email_notif = False
hook_notif = True


# SSH log file path
log_path = "/var/log/auth.log"

# Regular expression to match failed SSH login attempts
pattern1 = r"Failed password for invalid user (\w+) from (\d+\.\d+\.\d+\.\d+) port (\d+) ssh2"
pattern2 = r"authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=(\d+\.\d+\.\d+\.\d+)  user=(\w+)"
pattern3 = r"Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+) port (\d+) ssh2"
pattern4 = r"Authentication failure for (\w+) from (\d+\.\d+\.\d+\.\d+)"



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
                "text": "User: {} \n\nIP address: {} \n\nPort: {} \n\nTime: {}".format(
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
    username = ""
    # Check if line matches regex pattern
    match1 = re.search(pattern1, line)
    match2 = re.search(pattern2, line)
    match3 = re.search(pattern3, line)
    match4 = re.search(pattern4, line)


    # If the line matches pattern1
    if match1:
        print ("match1")
        # Get the user, IP address, and port from the matched groups
        username = match1.group(1)
        ip_address = match1.group(2)
        port = match1.group(3)

    
    # If the line matches pattern2
    elif match2:
        print ("match2")
        # Get the user, IP address from the matched groups
        username = match2.group(2)
        ip_address = match2.group(1)
        port = "unknown"
        

    # If the line matches pattern3
    elif match3:
        print ("match3")
        # Get the user, IP address, and port from the matched groups
        username = match3.group(1)
        ip_address = match3.group(2)
        port = match3.group(3)
        

    elif match4:
        # Get the user and IP address from the matched groups
        username = match4.group(1)
        ip_address = match4.group(2)
        port = "unknown"
       


    if username:
        # Call the webhook or Email with the user, IP address, and port information

        if hook_notif:
            call_webhook(username, ip_address, port,hostname)
        if email_notif:
            send_email(username, ip_address, port,hostname)    

