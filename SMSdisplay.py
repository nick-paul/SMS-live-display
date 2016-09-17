# SMSdisplay.py
# A simple script for displaying SMS messages live

# This file includes code from the Goolge API docs:
#   https://developers.google.com/gmail/api/quickstart/python
#   https://developers.google.com/gmail/api/v1/reference/users/messages/list#python


from __future__ import print_function
import httplib2
import os
import time
import webbrowser

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# The body of the display page
HTML_BODY = """
<br />
<br />
<center>
    <h1 style="font-size: 100pt">[[MESSAGE TEXT]]</h1>
</center>
"""

# For Google API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'auth.json'
APPLICATION_NAME = 'Python Desktop'

# From Google API QuickStart
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# From Google API Samples
def GetMessage(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except:
        return None

# From Google API Samples
def ListMessagesMatchingQuery(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except:
        return None



def main():

    # Get the phone number from phone_number.txt
    try:
        with open('phone_number.txt', 'r') as pn_file:
            PHONE_NUMBER = pn_file.readline().strip()
    except FileNotFoundError:
        print('Please provide a "phone_number.txt" file in the same directory as SMSdisplay.py containing the phone number whose messages you would like to display')
        return

    # Get the required credentials
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    lastSnippet = ''

    # Loop to fetch new emails and display them
    while True:
        messages = ListMessagesMatchingQuery(service, 'me', query=PHONE_NUMBER)

        # No messages
        if not messages:
            print('No messages recieved. Please check internet connection')
            time.sleep(10)
            continue # Try again
        else:
            msg = messages[0]
            snipStr = GetMessage(service, 'me', msg['id'])['snippet']
            if not snipStr:
                print('Empty message recieved. Please check internet connection.')
                time.sleep(5)
                continue #Try again
            # Only refresh the browser page if we have a new message
            if not snipStr == lastSnippet:
                lastSnippet = snipStr

                snipStr = HTML_BODY.replace('[[MESSAGE TEXT]]', snipStr)

                # Write the message to the html file
                f = open('snip.html','w')
                f.write(snipStr)
                f.close()

                # Open the file in the browser
                webbrowser.open('snip.html', new=0)

            time.sleep(5) # Sleep 5 seconds






if __name__ == '__main__':
    main()
