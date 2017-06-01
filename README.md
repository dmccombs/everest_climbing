# Mount Everest Value

Given an activity ID, print the elevation gain and percent of Everest climb.

Usage:
* Edit `everest_climbing.py`, and set the client ID and secret to valid strava
  API credentials
* Run `make up` to bring up a docker container with necessary Python modules,
  and `make shell` to shell into it
* Run `./everest_climbing.py <activity_id>` to fetch the activity and print out
  values

Example:
```
root@0ef03eb0aa93:/docker# ./activity_climbing.py 675131908
Grabbing activity Leadville 100 MTB
This activity had 11197.50692 feet of elevation gain.
That's 38.57% of the height of Mount Everest
```
