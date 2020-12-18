# pollingapp
This is a Django project, which expands on Django's official 'polling app' tutorial (https://docs.djangoproject.com/en/3.1/intro/tutorial01/).

## Functionality
In addition to the functionality of voting on polls, this polling app includes:
- A user profile and authentication system (only authenticated users can create polls and vote),
- Visual representations of poll results,
- A threaded comment system for each poll,
- Visual styling using Javascript and Bulma CSS (https://bulma.io/).

## Preview
### Overall functionality
![previewgif](/screenshots/awsumpolls.gif)
### Home screen
![home](/screenshots/homescreen.png)
### Voting view
![voting](/screenshots/votingview.png)
### Home screen
![results](/screenshots/results.png)
### Create polls
![createpoll](/screenshots/createpoll.png)

## Requirements

Python: 3.8.1 <
Django: 3.1.2 <

Plus all the packages for Python, as specified in `requirements.txt`

To run this app, perform the following steps:

1. Download this repository,
2. Install all the Python packages needed from the `requirements.txt` file,
3. In the `pollingapp` folder, apply database migrations using `python manage.py makemigrations`, and then `python manage.py migrate`,
4. Still in the `pollingapp` folder, run the following command: `python manage.py runserver`.

### Password reset functionality on localhost
To make sure the password reset email works:

1. Make sure you performed the steps from the Requirements section,
2. Follow the instructions on this page to configure a local SMTP server: https://aiosmtpd.readthedocs.io/en/latest/aiosmtpd/docs/cli.html
3. after you have started up the server, whenever a password reset email is sent, it will appear on the command line of the terminal which you used to set up the server.
From there you can copy the reset link and continue in the webapp.

An alternative to this is to set up your own email server remotely, e.g. using Gmail. More info here: (https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882). Note that this will require some tinkering with the `settings.py` file in the main Django application folder.