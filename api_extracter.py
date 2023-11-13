import requests

def get_artist_ids_from_tracks(track_ids, auth):
    suffix = '?ids=' + ','.join(track_ids)
    api_url = "https://api.spotify.com/v1/tracks{}".format(suffix)
    custom_headers = {
        'Authorization' : auth
    }
    response = requests.get(api_url, headers=custom_headers)

    if response.status_code != 200:
        print(response)
        raise Exception('Something went wrong :(')
    
    json = response.json()
    artist_ids = []

    for track in json['tracks']:
        artist_ids.append(track['album']['artists'][0]['id'])

    return artist_ids

def get_genres_from_artists(artist_ids, auth):
    suffix = '?ids=' + ','.join(artist_ids)
    api_url = "https://api.spotify.com/v1/artists{}".format(suffix)
    custom_headers = {
        'Authorization' : auth
    }

    response = requests.get(api_url, headers=custom_headers)

    if response.status_code != 200:
        print(response)
        raise Exception('Something went wrong :(')
    
    json = response.json()

    genres = []

    for track in json['artists']:
        genres.append(track['genres'])

    return genres
