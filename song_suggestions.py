import load_data
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from collections import Counter

def visualise_genres_by_tod_yearly(year):
    df = load_data.load_spotify_data_from_csv('export/{}_listening_data.csv'.format(year))

    # filter out skipped songs (listened for less than 10 seconds)
    df = df[df['ms_played'] >= 10000]
    # also filter out songs that have no genre
    df = df[df['genres'] != 'undefined']
    df['genres'] = [genre.split(', ') for genre in df['genres'].tolist()]
    df = df.explode('genres')
    df['hour'] = pd.to_datetime(df['ts']).dt.hour

    hourly_totals = df.groupby('hour')['ms_played'].sum().reset_index()
    hourly_totals['minutes_played'] = (hourly_totals['ms_played'] / 60000).round().astype(int)

    # plot formatting
    plt.style.use('dark_background')
    _, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('#1d1d1d')  # Set the background color of the plot area to light gray
    plt.gcf().set_facecolor('#000000') 

    # scatter sums
    plt.scatter(hourly_totals["hour"], hourly_totals['minutes_played'], c=hourly_totals["minutes_played"], s=75, cmap="inferno", edgecolors="w", linewidths=0.1)

    for hour in hourly_totals['hour'].tolist():
        all_genres = df[df['hour'] == hour]['genres'].tolist()
        if len(all_genres) > 0:
            genre_counts = Counter(all_genres)
            top_genre = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        else:
            top_genre = 'none'
        
        plt.text(hour, hourly_totals[hourly_totals['hour'] == hour]['minutes_played'].values[0], top_genre,
             horizontalalignment='center', verticalalignment='bottom', fontsize=8, color='orange', rotation=45)

    # title axis / ticks
    plt.ylim(bottom=0, top=1.2 * hourly_totals['minutes_played'].max())
    plt.xticks(hourly_totals['hour'])
    plt.title("Hourly minutes listened throughout {}".format(year))
    plt.ylabel("Minutes Listened")
    
    plt.savefig('export/graphs/{}/hourly_listening_patterns.png'.format(year), bbox_inches='tight', pad_inches=0.2)

def visualise_genres_by_tod():
    df = load_data.load_spotify_data_from_csv('export/all_listening_data.csv')

    # filter out skipped songs (listened for less than 10 seconds)
    df = df[df['ms_played'] >= 10000]
    # also filter out songs that have no genre
    df = df[df['genres'] != 'undefined']
    df['genres'] = [genre.split(', ') for genre in df['genres'].tolist()]
    df = df.explode('genres')
    df['hour'] = pd.to_datetime(df['ts']).dt.hour

    hourly_totals = df.groupby('hour')['ms_played'].sum().reset_index()
    hourly_totals['minutes_played'] = (hourly_totals['ms_played'] / 60000).round().astype(int)

    # plot formatting
    plt.style.use('dark_background')
    _, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('#1d1d1d')  # Set the background color of the plot area to light gray
    plt.gcf().set_facecolor('#000000') 

    # scatter sums
    plt.scatter(hourly_totals["hour"], hourly_totals['minutes_played'], c=hourly_totals["minutes_played"], s=75, cmap="inferno", edgecolors="w", linewidths=0.1)

    for hour in hourly_totals['hour'].tolist():
        all_genres = df[df['hour'] == hour]['genres'].tolist()
        if len(all_genres) > 0:
            genre_counts = Counter(all_genres)
            top_genre = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        else:
            top_genre = 'none'
        
        plt.text(hour, hourly_totals[hourly_totals['hour'] == hour]['minutes_played'].values[0], top_genre,
             horizontalalignment='center', verticalalignment='bottom', fontsize=8, color='orange', rotation=45)

    # title axis / ticks
    plt.ylim(bottom=0, top=1.2 * hourly_totals['minutes_played'].max())
    plt.xticks(hourly_totals['hour'])
    plt.title("Hourly minutes listened")
    plt.ylabel("Minutes Listened")
    
    plt.savefig('export/graphs/hourly_listening_patterns.png', bbox_inches='tight', pad_inches=0.2)

visualise_genres_by_tod()

def model_genres_by_tod():
    df = load_data.load_spotify_data_from_csv("export/all_listening_data.csv")
    # filter out skipped songs (listened for less than 10 seconds)
    df = df[df['ms_played'] >= 10000]
    # also filter out songs that have no genre
    df = df[df['genres'] != 'undefined']
    df['genres'] = [genre.split(', ') for genre in df['genres'].tolist()]
    df = df.explode('genres')
    df['hour'] = pd.to_datetime(df['ts']).dt.hour

    print('Formatting genres...')
    all_genres = df['genres'].tolist()
    genre_counts = Counter(all_genres)
    top_genres = list(dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:50]).keys())
    df = df[df['genres'].isin(top_genres)]

    for genre in top_genres:
        df[genre] = df['genres'].apply(lambda x: 1 if genre in x else 0)

    features = df[top_genres].values.tolist()
    labels = df['hour'].values.tolist()

    print('Spliting Data...')
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.4, random_state=64)

    print('Training model...')
    model = RandomForestClassifier(n_estimators=50, random_state=64)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    print('Accuracy: {}'.format(accuracy))