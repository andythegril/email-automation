# -------------------- FINALE --------------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import schedule
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import glob

recent_file = None


def send_email_with_attachment(file_path, recipient):
    # Sender and recipient details
    sender_email = 'your-email'
    password = 'your-pw' #the password you generated from your Gmail (Part 1)
    recipient_email = recipient
    # sender_email = 'dinhnguyetanh.ue@gmail.com'
    # password = 'woxwanpjoqgpybmm'
    # recipient_email = recipient

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Testing testing'

    # Add body text to the email
    message.attach(MIMEText('Check out the attached file.'))

    # Open the file in bytemode
    with open(file_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), Name=os.path.basename(file_path))
    attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    message.attach(attachment)

    # Connect to the SMTP server (Gmail in this case)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Send the email
    server.send_message(message)
    server.quit()


# File event handler
class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            send_email_with_attachment(file_path=recent_file, recipient=recipient_email)


# Set the directory to monitor
directory = 'your-dir'

# directory = '/Users/andythegril/school/careerbliss'

# Set the recipient email address
recipient_email = 'nhi-email'

# recipient_email = 'andythegril@gmail.com'

# Get the most recently edited file in the directory
def get_recent_file():
    global recent_file
    files = glob.glob(os.path.join(directory, '*'))
    recent_file = max(files, key=os.path.getmtime)

# Schedule the script to run at the desired times every week
def schedule_email_job():
    schedule.every().monday.at("09:00").do(send_email_with_attachment, file_path=recent_file, recipient=recipient_email)
    schedule.every().friday.at("15:35").do(send_email_with_attachment, file_path=recent_file, recipient=recipient_email)

# Create the file event handler and observer
event_handler = FileModifiedHandler()
observer = Observer()
observer.schedule(event_handler, directory, recursive=True)

# Start the observer
observer.start()

try:
    # Get the most recently edited file initially
    get_recent_file()

    # Schedule the email job
    schedule_email_job()

    # Run the scheduled tasks and observer indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the observer if interrupted
    observer.stop()

# Wait for the observer to finish
observer.join()
