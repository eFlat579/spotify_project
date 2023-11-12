import pandas as pd
import api_extracter

"""
Get the total listening minutes for a particular year.
"""
def get_yearly_listening_minutes(df, year):
    # Convert the 'Timestamp' column to datetime objects
    df['ts'] = pd.to_datetime(df['ts'])

    # Group the DataFrame by year and count the number of rows in each group
    yearly_ms_played = df[df['ts'].dt.year == year]['ms_played'].sum() / 1000
    return yearly_ms_played

"""
Get the top tracks for a given year.
"""
def get_top_tracks(df, year):
    # Convert the 'Timestamp' column to datetime objects
    df['ts'] = pd.to_datetime(df['ts'])

    df = df[df['ts'].dt.year == year]

    # Count the occurrences of each track
    track_counts = df.groupby(['master_metadata_track_name', 'master_metadata_album_artist_name']).size().reset_index(name='listen_count')

    # Extract the top N tracks
    top_tracks = track_counts.sort_values(by='listen_count', ascending=False).head(10)

    return top_tracks

"""
Get the top artists for a given year.
"""
def get_top_artists(df, year):
    # Convert the 'Timestamp' column to datetime objects
    df['ts'] = pd.to_datetime(df['ts'])

    df = df[df['ts'].dt.year == year]

    # Count the occurrences of each track
    track_counts = df.groupby(['master_metadata_album_artist_name']).size().reset_index(name='listen_count')

    # Extract the top N tracks
    top_tracks = track_counts.sort_values(by='listen_count', ascending=False).head(10)

    return top_tracks

"""
Get hourly listening patterns for an average day in given year
"""
def get_daily_listening_pattern(df, year):
    # Convert the 'Timestamp' column to datetime objects
    df['ts'] = pd.to_datetime(df['ts']).dt.hour
    hourly_ms_played = df.groupby('ts')['ms_played'].sum() / (1000 * 60)
    return hourly_ms_played

# UTIL -----------------------------------

"""
Uses spotify api to grab genres of tracks (based upon artist)"""
def get_track_genre(track_uri):
    track_id = track_uri.replace('spotify:track:', '')
    artist_id = api_extracter.get_artist_id_from_track(track_id)
    genres = api_extracter.get_genres_from_artist(artist_id)
    return genres
    



