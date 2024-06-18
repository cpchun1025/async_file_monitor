import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_email@example.com'
smtp_password = 'your_password'
recipient_email = 'recipient@example.com'
sender_email = 'your_email@example.com'

# File paths to monitor
files_to_check = ['file1.txt', 'file2.txt', 'file3.txt']

# Monitoring parameters
check_interval = 60  # 1 minute in seconds
email_interval = 600  # 10 minutes in seconds

def send_email(missing_files, present_files):
    subject = "File Monitoring Alert"
    body = f"The following files are missing: {', '.join(missing_files)}\n" \
           f"The following files are present: {', '.join(present_files)}"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

def monitor_files():
    start_time = time.time()
    last_email_time = start_time

    while True:
        present_files = [file for file in files_to_check if os.path.exists(file)]
        missing_files = [file for file in files_to_check if file not in present_files]

        if not missing_files:
            return 0

        current_time = time.time()
        elapsed_time = current_time - start_time

        if (current_time - last_email_time) >= email_interval:
            send_email(missing_files, present_files)
            last_email_time = current_time

        time.sleep(check_interval)

if __name__ == "__main__":
    exit_code = monitor_files()
    exit(exit_code)