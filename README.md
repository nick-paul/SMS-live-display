# SMSdisplay

A small python script for displaying SMS messages on a display as they are received.

![Demo](a_new_message.gif)


# Setup

This script uses Gmail to receive and display SMS messages and therefore requires some setup before it can be used.

  1. Create a new gmail account that you would like to use for this display
  2. Follow the steps [here](https://developers.google.com/gmail/api/quickstart/python) to set up a Google API authentication for your newly created email address.
  3. Copy the .json file you downloaded in the previous step into this directory and rename it `auth.json`
  4. Create a text file called `phone_number.txt` and enter the phone number whose messages you would like to display.
  5. Messages are displayed in your default browser. Each time a new message is received, it opens a new tab. To avoid too many tabs staying open, set Goole Chrome as your default browser and install [xTab](https://chrome.google.com/webstore/detail/xtab/amddgdnlkmohapieeekfknakgdnpbleb?hl=en). This will automatically close tabs after too many accumulate.
  6. Open Chrome then run the script!

## Sending messages to your email

  To display your text message, simply send a text to the email you created in step 1 of the setup. The texts will appear on the display shortly after sending.
