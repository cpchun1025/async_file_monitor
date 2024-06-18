import os
import time
import asyncio
import aiosmtplib
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

async def send_email(missing_files, present_files):
    subject = "File Monitoring Alert"
    body = f"The following files are missing: {', '.join(missing_files)}\n" \
           f"The following files are present: {', '.join(present_files)}"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    await aiosmtplib.send(
        message,
        hostname=smtp_server,
        port=smtp_port,
        username=smtp_username,
        password=smtp_password,
        start_tls=True,
    )

async def check_files():
    present_files = [file for file in files_to_check if os.path.exists(file)]
    missing_files = [file for file in files_to_check if file not in present_files]
    return missing_files, present_files

async def monitor_files():
    start_time = time.time()
    last_email_time = start_time

    while True:
        missing_files, present_files = await check_files()

        if not missing_files:
            return 0

        current_time = time.time()
        elapsed_time = current_time - start_time

        if (current_time - last_email_time) >= email_interval:
            await send_email(missing_files, present_files)
            last_email_time = current_time

        await asyncio.sleep(check_interval)

if __name__ == "__main__":
    exit_code = asyncio.run(monitor_files())
    exit(exit_code)