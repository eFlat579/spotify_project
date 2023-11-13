import zipfile
import pandas as pd
import json

def load_spotify_data_from_zip() -> pd.DataFrame:
    with zipfile.ZipFile('import/extended_streaming_data.zip') as zf:
        files = [
            'endsong_0.json',
            'endsong_1.json',
            'endsong_2.json',
            'endsong_3.json',
            'endsong_4.json',
            'endsong_5.json',
            'endsong_6.json',
            'endsong_7.json',
            'endsong_8.json',
            'endsong_9.json',
            ]

        data_list = []
        for name in files:
            # Load the JSON data from the file
            with zf.open('MyData/%s' % name, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            data_list.append(df)
        # Concatenate the data from all the files into a single NumPy array
        df = pd.concat(data_list)
        df = df.sort_values(by='ts')
        return df

def load_spotify_data_from_csv(filepath):
    df = pd.read_csv(filepath)
    return df