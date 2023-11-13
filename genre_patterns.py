import load_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter

"""
For each day in a year get the total ms_played
"""
def get_genre_counts(df, year):
    # Convert the 'Timestamp' column to datetime objects
    df['ts'] = pd.to_datetime(df['ts'])
    df = df[df['ts'].dt.year == year] # ammend this line

    # split each string and flatten the list
    raw_genres = df['genres'].tolist()
    all_genres = [genre.strip() for genres in raw_genres for genre in genres.split(',')]

    # get and return counts
    genre_counts = Counter(all_genres)
    return genre_counts

def build_top_genres(year):
    df = load_data.load_spotify_data_from_csv('export/{}_listening_data.csv'.format(year))

    # get top 10 counts
    genre_counts = get_genre_counts(df, year)
    top_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    # calculate percentages
    total_count = sum(top_genres.values())
    percentages = [count / total_count * 100 for count in top_genres.values()]

    # plot formatting
    plt.style.use('dark_background')
    _, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('#1d1d1d')  # Set the background color of the plot area to light gray
    plt.gcf().set_facecolor('#000000') 

    # plot bars
    colors = plt.cm.inferno(np.linspace(1, 0, len(top_genres)))
    bars = plt.bar(top_genres.keys(), percentages, color=colors, edgecolor='w', linewidth=0.1)

    # set title and ticks
    plt.title('Top 10 Genres in {}'.format(year))
    plt.yticks(np.arange(0, round(percentages[0] + 7), 5))
    plt.xticks(rotation=45, ha='right')
    plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

    # add bar labels
    for bar, percentage in zip(bars, percentages):
        plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 1, f'{percentage:.1f}%', ha='center', color='w')

    # save
    plt.savefig('export/graphs/{}/top_genres.png'.format(year), bbox_inches='tight', pad_inches=0.2)