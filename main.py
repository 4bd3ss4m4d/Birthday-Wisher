# Birthday Wishes Sender

#########################
# Created by 4bd3ss4m4d #
#########################

import csv
import datetime as dt
import smtplib
import random
import os

# ---------------------------- CONSTANTS ------------------------------- #
# My Account Credentials
my_email = os.environ.get('GMAIL_USER')
my_password = os.environ.get('GMAIL_PASSWORD')


# ---------------------------- Main function------------------------------- #
def main():
    # Open the birthday.csv file
    with open('birthdays.csv', 'r') as data_file:
        # Read csv file
        csv_file = csv.DictReader(data_file, delimiter=',')

        # Append records as Dictionaries
        data_list = [line for line in csv_file]

        # Create a list containing only birth dates
        birth_dates = []
        # Loop through each line of data_list
        for data_line in data_list:
            # Get the birth dates from data_list
            year = int(data_line['year'])
            month = int(data_line['month'])
            day = int(data_line['day'])

            # Create an instance of datetime
            birth_date = dt.datetime(year, month, day).date()

            # Get the current day and time
            now = dt.datetime.now()
            current_date = now.date()

            # If the current day equals birth_date
            if current_date.month == birth_date.month and current_date.day == birth_date.day:
                # Create letter template list:
                letter_templates_list = ['letter_templates\letter_1.txt',
                                         'letter_templates\letter_2.txt',
                                         'letter_templates\letter_3.txt']

                with open(random.choice(letter_templates_list), 'r') as letter_file:
                    # Read the original letter
                    original_letter = letter_file.read()

                    # Replace [name] by the name of the one who's birth date is the current day
                    done_letter = original_letter
                    done_letter = done_letter.replace('[NAME]', data_line['name'])
                    mail_sender(done_letter, data_line['email'], data_line['name'])


# ---------------------------- SMTP SENDER ------------------------------- #
def mail_sender(birthday_letter, email, name):
    # Recipient email
    recipient_email = email
    # Message's subject and body
    message_subject = 'HAPPY BIRTHDAY!!'
    message_body = birthday_letter

    # Open an SMTP connexion using the default mail submission port using 587
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # command sent by an email server to identify itself when connecting to another email server to start the
        # process of sending an email.
        smtp.ehlo()
        # StartTLS is a protocol command used to inform the email server that the email client wants to upgrade from an
        # insecure connection to a secure one using TLS
        smtp.starttls()
        # Rerun ehlo to reidentify ourselves as an encrypted connexion
        smtp.ehlo()
        # Login
        smtp.login(user=my_email, password=my_password)
        # Message to send
        message = f'Subject: {message_subject}\n\n{message_body}'
        # Sending the Message
        smtp.sendmail(from_addr=my_email, to_addrs=recipient_email, msg=message)
        # Print email successfully sent
        print(f'Birthday wish successfully sent to {name}')


# ---------------------------- Run Main Program ------------------------------- #
main()
