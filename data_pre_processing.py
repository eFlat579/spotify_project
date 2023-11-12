import load_data
import api_extracter

df = load_data.load_spotify_data_from_zip()
df = df[['ts', 'ms_played','master_metadata_track_name', 'master_metadata_album_artist_name', 'master_metadata_album_album_name', 'spotify_track_uri']]

df = df[df.notna().all(axis=1)]
df = df.reset_index(drop=True)

# Save DataFrame to CSV
df.to_csv('export/listening_data.csv', index=False)