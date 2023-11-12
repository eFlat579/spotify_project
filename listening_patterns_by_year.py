import load_data
import insight_extraction
import matplotlib.pyplot as plt
import pandas as pd

"""
For each day in a year get the total ms_played
"""
def get_daily_ms_listened_by_year(df, year):
    # Convert the 'Timestamp' column to datetime objects
    df['ts'] = pd.to_datetime(df['ts'])
    df = df[df['ts'].dt.year == year] # only keep rows from given year

    # Create a complete date range for the entire year with UTC timezone
    date_range = pd.date_range(start='{}-01-01'.format(year), end='{}-12-31'.format(year), freq='D', tz='UTC')

    for dt in date_range:
        print(dt.date())
        daily_sum = df[df['ts'].dt.date() == dt.date()]['ms_played'].sum()
        print(daily_sum)


df = load_data.load_spotify_data_from_csv()
get_daily_ms_listened_by_year(df, 2013)

