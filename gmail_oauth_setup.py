import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["", "", "",]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client.json', SCOPES)
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    creds = flow.run_local_server(
        port=8888,
        prompt='consent'
    )
    # Save the credentials to token.json
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("token.json created successfully!")

if __name__ == '__main__':
    main()
