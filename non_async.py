import os
import asyncio
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

async def send_email(missing_files, present_files):
    subject = "File Monitoring Alert"
    body = f"The following files are missing: {', '.join(missing_files)}\n" \
           f"The following files are present: {', '.join(present_files)}"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    async with asyncio.open_connection(smtp_server, smtp_port) as reader, writer:
        await writer.write(b'EHLO example.com\r\n')
        await writer.write(b'STARTTLS\r\n')
        await writer.drain()

        await writer.write(f'AUTH LOGIN {smtp_username}\r\n'.encode())
        await writer.write(f'{smtp_password}\r\n'.encode())
        await writer.drain()

        await writer.write(f'MAIL FROM:{sender_email}\r\n'.encode())
        await writer.write(f'RCPT TO:{recipient_email}\r\n'.encode())
        await writer.write(b'DATA\r\n')
        await writer.write(message.as_string().encode())
        await writer.write(b'.\r\n')
        await writer.drain()

        await writer.write(b'QUIT\r\n')
        await writer.drain()

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