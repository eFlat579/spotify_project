import load_data
import api_extracter
import consts
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd

def build_recommendations(year):
    df = load_data.load_spotify_data_from_csv('export/{}_listening_data.csv'.format(year))
    
    # get seeds for request, top 3 tracks, top 2 artists
    top_artists = df['arid'].value_counts().reset_index(name='count').nlargest(2, 'count')['index'].tolist()
    top_tracks = df['trid'].value_counts().reset_index(name='count').nlargest(3, 'count')['index'].tolist()

    recommendations = api_extracter.get_recommended_tracks(top_tracks, top_artists, 5, consts.auth)

    # create blank canvas
    image = Image.new('RGB', (400, 330), '#1d1d1d')
    draw = ImageDraw.Draw(image)

    # draw recommended tracks
    text_y = 20
    for track, artist, image_url in recommendations:
        # add image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((50, 50))
        image.paste(img, (20, text_y))

        # add track / artist text
        draw.text((100, text_y + 15), track, fill='white')
        draw.text((100, text_y + 25), artist, fill='white')

        # add padding
        text_y += 60

    # save
    image.save('export/graphs/{}/recommended_tracks.png'.format(year))