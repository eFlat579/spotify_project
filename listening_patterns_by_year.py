import load_data
import matplotlib.pyplot as plt
import pandas as pd

"""
For each day in a year get the total ms_played
"""
def get_daily_ms_listened_by_year(df, year):
    df['ts'] = pd.to_datetime(df['ts'])
    df = df[df['ts'].dt.year == year]

    # Create a complete date range for the entire year with UTC timezone
    date_range = pd.date_range(start='{}-01-01'.format(year), end='{}-12-31'.format(year), tz='UTC')

    to_ret = []
    for dt in date_range:
        daily_sum = df[df['ts'].dt.date == dt.date()]['ms_played'].sum()
        to_ret.append([dt, daily_sum / (1000 * 60)])
    
    return to_ret

"""
Create plot for daily listening across the year.
"""
def build_minutes_listened(year):
    df = load_data.load_spotify_data_from_csv('export/{}_listening_data.csv'.format(year))

    # get daily sums over year span
    daily_sums = get_daily_ms_listened_by_year(df, year)
    df = pd.DataFrame(daily_sums, columns=["date", "sum"])
    df["date"] = pd.to_datetime(df["date"])

    # plot formatting
    plt.style.use('dark_background')
    _, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('#1d1d1d')  # Set the background color of the plot area to light gray
    plt.gcf().set_facecolor('#000000') 

    # scatter sums
    plt.scatter(df["date"], df["sum"], c=df["sum"], s=75, cmap="inferno", edgecolors="w", linewidths=0.1)
    # plot monthly average
    monthly_avg = df.groupby(df["date"].dt.to_period('M')).mean()
    plt.plot(monthly_avg.index.to_timestamp(), monthly_avg["sum"], color='orange', linewidth=4)

    # title axis / ticks
    plt.title("Daily minutes listened throughout {}".format(year))
    plt.ylabel("Minutes Listened")
    xticks = pd.date_range(start=df["date"].min().replace(day=1), end=df["date"].max().replace(day=1), freq='MS')
    plt.xticks(xticks, [x.strftime('%b') for x in xticks])

    # save
    plt.savefig('export/graphs/{}/minutes_listened.png'.format(year), bbox_inches='tight', pad_inches=0.2)

