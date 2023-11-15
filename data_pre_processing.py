import load_data
import api_extracter
import pandas as pd
import consts
import time

def get_extended_track_info(year, df, auth):
    batch_size = 50

    all_genres = []
    all_artists = []
    all_artworks = []
    for i in range(0, len(df), batch_size):
        batch_num = i // batch_size + 1
        batch = df['trid'].iloc[i:i+batch_size].tolist()
        print("Processing {}, batch {} / {}".format(year, batch_num, len(df) // batch_size + 1))

        time.sleep(0.5)
        artists, artworks = api_extracter.get_track_data(batch, auth)
        all_artists.extend(artists)
        all_artworks.extend(artworks)

        time.sleep(0.5)
        genres = api_extracter.get_genres_from_artists(artists, auth)
        all_genres.extend(genres)

    return all_artists, all_genres, all_artworks

def combine_dataframes(years):
    dfs = []
    for year in years:
        df = load_data.load_spotify_data_from_csv("export/{}_listening_data.csv".format(year))
        dfs.append(df)
    all_data = pd.concat(dfs, axis=0)
    all_data.to_csv('export/all_listening_data.csv', index=False)

        

df = load_data.load_spotify_data_from_zip()
df = df[['ts', 'ms_played','master_metadata_track_name', 'master_metadata_album_artist_name', 'master_metadata_album_album_name', 'spotify_track_uri']]

df = df[df.notna().all(axis=1)]
df = df.reset_index(drop=True)
df['ts'] = pd.to_datetime(df['ts'])

df['trid'] = df['spotify_track_uri'].str.replace("spotify:track:", "")
df = df.drop('spotify_track_uri', axis=1)

years = df['ts'].dt.year.unique()

for year in years:
    df_y = df[df['ts'].dt.year == year]

    auth = consts.auth
    artist_ids, genres, artworks = get_extended_track_info(year, df_y, auth)

    df_y['arid'] = artist_ids

    df_y['genres'] = genres
    df_y['genres'] = df_y['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    df_y['genres'] = df_y['genres'].replace("", "undefined")

    df_y['artwork'] = artworks

    df_y.to_csv('export/{}_listening_data.csv'.format(year), index=False)

combine_dataframes(years)