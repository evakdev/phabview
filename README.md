# Phabby

Phabby is a bot that gets Phabricator revision updates from webhook
and translates them to nice, readable notifications in
your company messaging app.

### What does Phabby notify about?
Phabby will notify your users in DM when there are:

- New updates on a revision they created (reviews, comments)
- New revisions where their review is requested
- Updates on revisions on which they have engaged as reviewers

Subscribers will also be notified about all of the above.

### On what messaging apps can I receive the notifications?
Currently only rocketchat is supported. 

Contributions for any other messaging apps are welcome!

## How to Use

### 1. Create a Phabricator Webhook

Go here in your Phabricator instance and create a 'Firehose' webhook:

   ```
   https://{my_phabricator}/herald/webhook/
   ```

You need Admin permissions to do so. After creation,
grab the hmac_key and add it to your envs as `PHABRICATOR_WEBHOOK_HMAC_KEY`

### 2. Create a Phabricator Bot User

Or you can use your own user to experiment.
Go to the address below and create an API Token:

   ```
   https://{my_phabricator}/settings/user/{username}/page/apitokens/
   ```

Add the following envs:

- PHABRICATOR_HOST
- PHABRICATOR_USERNAME
- PHABRICATOR_TOKEN

### 3. Connect to Messaging Service

Currently only rocketchat is available.

Login to your Rocketchat Instance as an admin user, and create a bot user here:

   ```
   Administration > Workspace > Users
   ```

Add the following envs:

- ROCKETCHAT_HOST
- ROCKETCHAT_USERNAME
- ROCKETCHAT_PASSWORD

### 4. Setup Notifiable Users

Phabby is designed to notify in DMs. 
If you want all of your users to receive phabricator updates, set `NOTIFY_ANY_USER` to `True`

Otherwise, you can go with an opt-in method an add interested users' usernames in `NOTIFIABLE_USERS` env like this:
```python
NOTIFIABLE_USERS="mary,emma,jack"
```

**Note:** Phabby currently assumes same usernames for Phabricator and Rocketchat.

## Docker Image

You can find the docker images provided for the project here.

## Contribution Guide

1. Install Rye as package manager:

    ```bash
    curl -sSf https://rye.astral.sh/get | bash
    ```

2. Install dependencies with `rye sync`

3. Add a .env file with any envs needed in `config.py`

4. Start the project:
   ```bash
   python src/phabby/main.py
   ```