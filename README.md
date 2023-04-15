# SSH Failed Login Detection Script

This Python script monitors the system log for failed SSH login attempts and sends notifications to a Rocket.Chat webhook and/or an email address.

## Requirements

- Python 3.x
- `requests` module for Python (for sending notifications to Rocket.Chat)
- `smtplib` and `email` modules for Python (for sending email notifications)

## Usage

1. Clone or download the repository.
```
git clone https://github.com/mrmoghadasi/login_failed_alert.git
```

2. Navigate to the project directory:

```
cd login_failed_alert
```


3. Edit the configuration variables in the `config.ini` script to match your setup.

The `[script_settings]` section appears to be specifying some general settings for the script that is using this configuration file. It includes settings for email and webhook notifications as well as a path to a log file.

The `[email_settings]` section appears to be configuring the email settings for the script, including the SMTP server to use, the SMTP port number, the SMTP username and password, and the sender and recipient email addresses.

The `[webhook_settings]` section appears to be configuring the webhook settings for the script, including the URL of the webhook to use.

The following configuration variables can be edited in the `ssh-failed-login.py` script:

- `LOG_FILE`: the path to the system log file (default is `/var/log/auth.log` on Ubuntu and Debian)
- `email_notif`: enable or disable send email notification
- `hook_notif`: enable or disable send webhook notification
- `WEBHOOK_URL`: the URL of the Rocket.Chat webhook to send notifications to (optional)
- `EMAIL_FROM`: the email address to send notifications from (optional)
- `EMAIL_TO`: the email address(es) to send notifications to (optional)
- `SMTP_SERVER`: the SMTP server to use for sending email notifications (optional)
- `SMTP_PORT`: the SMTP server port to use for sending email notifications (default is 587)
- `SMTP_USERNAME`: the SMTP server username (optional)
- `SMTP_PASSWORD`: the SMTP server password (optional)

4. run installer script
```
chmod +x installer.sh
./installer.sh
```

## New Feature Release 

### v.2
In this version 3, new patterns have been added to detect other states besides "login failed".

```
pattern1 = r"Failed password for invalid user (\w+) from (\d+\.\d+\.\d+\.\d+) port (\d+) ssh2"
pattern2 = r"authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=(\d+\.\d+\.\d+\.\d+)  user=(\w+)"
pattern3 = r"Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+) port (\d+) ssh2"
pattern4 = r"Authentication failure for (\w+) from (\d+\.\d+\.\d+\.\d+)"
```


## License

[MIT](https://choosealicense.com/licenses/mit/) 
This project is licensed under the MIT License.

## Credits

This project was created by My User (mrm.elec@email.com)

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/mohamad-reza-moghadasi-5755b959/)](https://www.linkedin.com/in/mohamad-reza-moghadasi-5755b959/) [![Gmail](https://img.shields.io/badge/-Gmail-red?style=flat-square&logo=Gmail&logoColor=white&link=mailto:mrm.elec@gmail.com)](mailto:mrm.elec@gmail.com)