# PyGmail

PyGmail is a Python utility for sending emails using the Gmail API.
It consists of two distinct scripts, oauth_server.py and pygmail.py, described below.

## Requirements
* Python 2.7
* Google APIs Client Library for Python - [Installation instructions here](https://developers.google.com/api-client-library/python/)
* A computer with a web browser (Only required during setup)

## Scripts

### oauth_server.py

The oauth_server script is used to generate the OAuth2 access and refresh tokens, useable by any script to access the Google API on behalf of a user.

#### Usage

```
python oauth_server.py [-h] [-s SECRET] [-c CREDENTIALS] [-p PORT] scope
```

#### Required arguments

Argument|Explenation
--------|-----------
scope   |The OAuth2 scope to request access to

#### Optional arguments

Argument|Explenation|Default
--------|-----------|-------
-s, --secret SECRET|The client id / secret file to use for identifying the application|client_secret.json
-c, --credentials CREDENTIALS|The file to save the OAuth2 credentials to|credentials.json
-p, --port PORT|The port to run the local http server on|8000

#### Example

```
python oauth_server.py -p 80 https://www.googleapis.com/auth/gmail.compose
```

This will run the script with a web server on port 80, requesting the scope to write emails on behalf of the user.

1. Once the script is running, navigate your web browser to the chosen port (Or 8000 by default), on your local machine.

2. You will be redirected to Google's log in page, where you can either log in with an account (The account you wish to request the access token on behalf), or choose an already logged in account.

3. Once an account has been chosen, you will be asked to verify access to the scope listed, on behalf of the account.

4. If you confirm access, you will be redirected back to the local server, where you should see a confirmation page, this indicates the script was sent the access information, and the access token should be saved on the local machine.

5. This token can now be used by any script to access the scope selected, on behalf of the user.

### pygmail.py

The pygmail script is used to send emails using the gmail API, on behalf of the user to which a given OAuth2 token represents.

#### Usage

The pygmail script can be used in two ways, either to send emails directly from the command line, or as a function to call from a different script.

#### Command line

```
python pygmail.py [-h] [-s SUBJECT] [-c CREDENTIALS] message to [to ...]
```

##### Required arguments

Argument|Explenation
--------|-----------
message |The message text to send
to      |A list of email addresses to send the message to

##### Optional arguments

Argument|Explenation|Default
--------|-----------|-------
-s, --subject SUBJECT|The subject line of the email message|OEP Message
-c, --credentials CREDENTIALS|The OAuth2 credentials file to use|credentials.json

##### Example

```
python pygmail.py -s "Hello World!" "This is a test message from pygmail!" me@example.com you@example.com
```

#### Script

```
dispact_messages(to_list, message_body, subject, credentials_file)
```

##### Arguments

Argument|Explenation
--------|-----------
to_list |A python list of email address strings
message_body|A string containing the body text of the email message
subject|A string containing the subject line of the email message
creentials_file|The path to the OAuth2 credentials file - Can be a relative path

##### Example

```python
dispact_message(["me@example.com", "you@example.com"], "This is a test message from pygmail!", "Hello World!", "credentials.json")
```
