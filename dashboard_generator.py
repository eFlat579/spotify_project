import os

import listening_patterns_by_year
import genre_patterns
import get_recommendations
import song_suggestions

# pressume all pre processing is already done.

year = 2021

# Specify the path for the new folder
folder_path = 'export/graphs/{}'.format(year)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

listening_patterns_by_year.build_minutes_listened(year)
genre_patterns.build_top_genres(year)
get_recommendations.build_recommendations(year)
song_suggestions.visualise_genres_by_tod_yearly(year)