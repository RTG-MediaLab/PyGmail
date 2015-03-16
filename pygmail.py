from apiclient.discovery import build
from oauth2client.file import Storage
from email.mime.text import MIMEText
from apiclient import errors
import httplib2
import base64
import argparse
import sys

def _get_args():
    parser = argparse.ArgumentParser(description="Send email using the gmail API")
    parser.add_argument('message', help="the body of the message to send")
    parser.add_argument('to', nargs="+", help="the recipiants of the message")
    parser.add_argument('-s', '--subject', default="OEP Message", help="the subject line of the message")
    parser.add_argument('-c', '--credentials', default="credentials.json", help="the OAuth2 credentials file to use")

    args = vars(parser.parse_args())

    return args['to'], args['message'], args['subject'], args['credentials']

def _create_message(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def _send_message(service, message):
    try:
        response = service.users().messages().send(userId="me", body=message).execute()
    except errors.HttpError, error:
        print "An error occured:", error

def dispact_messages(to_list, message_body, subject, credentials_file):
    messages = []
    for person in to_list:
        messages.append(_create_message(person, subject, message_body))

    storage = Storage(credentials_file)
    credentials = storage.get()

    http = credentials.authorize(httplib2.Http())
    gmail_service = build('gmail', 'v1', http=http)

    for message in messages:
        _send_message(gmail_service, message)

def main():
    to_list, message_body, subject, credentials_file = _get_args()

    dispact_messages(to_list, message_body, subject, credentials_file)

if __name__ == "__main__":
    main()
