import pandas as pd
import json
import ast
import os
from main import main
import glob
import os

#Select file in console
# def select_file():
#     files = os.listdir('./data')
#     text = []
#     count = 0
#     for i in files:
#         f = f'{count} = {i}/'
#         text.append(f)
#         count += 1
#     text_str = ''.join(text).replace('/','\n\n')
#     user_input = int(input(f"\n SELECCIONA EL ARCHIVO QUE QUIERES LIMPIAR \n\n {text_str}"))
#     return files[user_input]


def clean():
    try:
        #Creating dataframe from file selected
        #df = pd.read_csv(f'./data/{file}')
        list_of_files = glob.glob('./data/*')
        latest_file = max(list_of_files, key=os.path.getctime)

        df = pd.read_csv(latest_file)

        #Adding Key
        df['key'] = df.index

        #Casting album values in dict
        df['album'] = df['album'].apply(lambda x: ast.literal_eval(x))

        #Unnesting values from a column
        def unnest_values(column):
            n = 0
            a_values = []  
            for row in column:
                new_value = {'key':n}
                row.update(new_value)
                a_values.append(row)
                n += 1
            nest_df = pd.DataFrame(a_values)
            return nest_df

        #Mergin original dataframe with album unnested values
        df = df.merge(unnest_values(df['album']), on='key',how='left')

        #Renaming columnns
        df.columns = df.columns.str.replace(r'_x','_track')
        df.columns = df.columns.str.replace(r'_y','_album')

        #Casting column values in a list
        df['artists_track'] = df['artists_track'].apply(lambda x: ast.literal_eval(x))
        df['artists_track'] = df['artists_track'].apply(lambda x: x[0])

        #Getting first image of the album
        df['images'] = df['images'].apply(lambda x: x[0])

        #Mering values with image and artist unnested values
        df = df.merge(unnest_values(df['images']), on='key',how='left')
        df = df.merge(unnest_values(df['artists_track']), on='key',how='left')

        #Drop Columns !!NOT NECESARY
        df.drop(['album','external_ids','artists_track','width','height','images','external_urls_track','external_urls_album','artists_album','external_ids','href_track','href_album','uri_album','key','type_album','type_track','type','uri'],axis=1,inplace=True)

        #Renaming and casting column
        df.rename(columns={'url': 'image_url'},inplace=True)
        df.rename(columns={'name':'author'})
        df[['duration_ms','popularity','total_tracks']] = df[['duration_ms','popularity','total_tracks']].astype(int)
        df['release_date'] = pd.to_datetime(df['release_date'])

        df = df[[
        'artist',
        'id_track',
        'name_track',
        'name',
        'duration_ms',
        'explicit',
        'popularity',
        'preview_url',
        'id_album',
        'name_album',
        'release_date',
        'total_tracks',
        'album_type',
        'image_url'
        ]]

        print('🟢 Dataset Limpio!')

        return df

    except Exception as e:
        print('ERROR CLEANING DATASET')
        print(e)