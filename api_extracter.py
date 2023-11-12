import requests
import consts


def get_artist_ids_from_tracks(track_ids):
    # Replace the URL and headers with the actual API endpoint and headers you want to use

    suffix = '?ids=' + ','.join(track_ids)
    api_url = "https://api.spotify.com/v1/tracks{}".format(suffix)
    custom_headers = {
        'Authorization' : consts.auth_token
    }

    # Make a GET request with headers
    response = requests.get(api_url, headers=custom_headers)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(response)
        return -1
    
    json = response.json()
    artist_ids = []

    for track in json['tracks']:
        artist_ids.append = track['album']['artists'][0]['id']

    return artist_ids
