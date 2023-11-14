import requests

def get_track_data(track_ids, auth):
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
    artworks = []

    for track in json['tracks']:
        artist_ids.append(track['album']['artists'][0]['id'])
        if len(track['album']['images']) > 0:
            artworks.append(track['album']['images'][0]['url'])
        else:
            artworks.append('')

    return artist_ids, artworks

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


def get_recommended_tracks(track_ids, artist_ids, limit, auth):
    suffix = '?seed_artists=' + ','.join(artist_ids) + '&seed_tracks=' + ','.join(track_ids) + '&limit={}'.format(limit)
    api_url = "https://api.spotify.com/v1/recommendations{}".format(suffix)
    custom_headers = {
        'Authorization' : auth
    }
    
    response = requests.get(api_url, headers=custom_headers)
    if response.status_code != 200:
        print(response)
        raise Exception('Something went wrong :(')
    
    json = response.json()

    recommendations = []
    for track in json['tracks']:
        #id = track['id']
        name = track['name']
        #artist_id = track['artists'][0]['id']
        artist = track['artists'][0]['name']
        image = track['album']['images'][0]['url']

        recommendations.append([name, artist, image])

    return recommendations