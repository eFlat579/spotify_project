import load_data
import api_extracter
import pandas as pd
import consts
import time

def get_track_genres(df, auth):
    batch_size = 50

    all_genres = []
    all_artists = []
    for i in range(0, len(df), batch_size):
        batch_num = i // batch_size + 1
        batch = df['trid'].iloc[i:i+batch_size].tolist()
        print("Processing batch {} / {}".format(batch_num, len(df) // batch_size + 1))

        time.sleep(1)
        artists = api_extracter.get_artist_ids_from_tracks(batch, auth)
        all_artists.extend(artists)

        time.sleep(1)
        genres = api_extracter.get_genres_from_artists(artists, auth)
        all_genres.extend(genres)

    return all_artists, all_genres
        

df = load_data.load_spotify_data_from_zip()
df = df[['ts', 'ms_played','master_metadata_track_name', 'master_metadata_album_artist_name', 'master_metadata_album_album_name', 'spotify_track_uri']]

df = df[df.notna().all(axis=1)]
df = df.reset_index(drop=True)
df['ts'] = pd.to_datetime(df['ts'])

df['trid'] = df['spotify_track_uri'].str.replace("spotify:track:", "")
df = df.drop('spotify_track_uri', axis=1)

year = 2012
df = df[df['ts'].dt.year == year]

auth = consts.auth
artist_ids, genres = get_track_genres(df, auth)

df['arid'] = artist_ids

df['genres'] = genres
df['genres'] = df['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
df['genres'] = df['genres'].replace("", "undefined")

# Save DataFrame to CSV
df.to_csv('export/{}_listening_data.csv'.format(year), index=False)