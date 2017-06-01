#!/usr/bin/env python3
"""
Given an activity ID, print the elevation gain and percent of Everest climb.
"""

import argparse
import json
import os
import time

from requests_oauthlib import OAuth2Session


CLIENT_ID = r''  # Straa API client ID
CLIENT_SECRET = r''  # Strava API client secret
REDIRECT_URI = 'https://localhost'


class Strava(object):
    def __init__(self):
        self.strava_url = 'https://www.strava.com/'
        self.strava_api = self.strava_url + 'api/v3/'
        self.init_strava_session()

    def init_strava_session(self):
        """
        Uses an existing token or retrieves a new one via oauth and returns
        a session to the Strava API.
        """
        # Read a previously saved token from file
        if os.path.exists('token.txt'):
            with open('token.txt') as f:
                token = {'token_type': 'Bearer', 'access_token': f.read()}
                self.oauth = OAuth2Session(CLIENT_ID, token=token)
        else:
            self.oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
            authorization_url, state = self.oauth.authorization_url(
                self.strava_url + 'oauth/authorize',
                access_type="offline", approval_prompt="force")

            print('Please go to %s and authorize access.' % authorization_url)
            authorization_response = input("Enter the full callback URL: ")

            token = self.oauth.fetch_token(
                self.strava_url + 'oauth/token',
                authorization_response=authorization_response,
                client_secret=CLIENT_SECRET,
                token_type='Bearer')

            # Save the token to a file
            with open('token.txt', 'w') as f:
                f.write(token['access_token'])

    def call_strava(self, request, params={}):
        """
        Make a call to the Strava API and handle rate limiting as necessary.
        """
        r = self.oauth.get(self.strava_api + request, params=params)
        decoded = json.loads(r.content.decode('UTF-8'))

        if 'message' in decoded and \
                decoded['message'] == 'Rate Limit Exceeded':
            print("Strava API rate limit exceeded, pausing for 15 minutes.")
            time.sleep(15 * 60)
            return self.call_strava(request, params)

        return decoded

    def fetch_athlete_name(self, athlete):
        """
        Returns the display name for a given athlete id.
        """
        decoded = self.call_strava('athletes/%s' % athlete)

        return '%s %s' % (decoded['firstname'], decoded['lastname'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('id',
                        help='Activity ID')

    args = parser.parse_args()

    # The event id should be a number at least...
    try:
        int(args.id)
    except:
        parser.print_help()
        raise ValueError("activity id must be a number")

    strava = Strava()
    decoded = strava.call_strava('activities/%s' % args.id)
    total_feet = decoded['total_elevation_gain'] * 3.28084
    everest_percent = (total_feet / 29029) * 100

    print("Grabbing activity %s" % decoded['name'])
    print("This activity had %s feet of elevation gain." % total_feet)
    print("That's %.2f%% of the height of Mount Everest" % everest_percent)
