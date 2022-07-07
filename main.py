import requests
from urllib.parse import urlencode
import pandas as pd
import base64
import json
from pandas import json_normalize

j = open("./access.json", "r")
access = json.load(j)

#User Info
client_id = access['client_id']
client_secret = access['client_secret']

#Parsing user info B64encode
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

def main():
    #Getting access token from spotify
    token_url = 'https://accounts.spotify.com/api/token'
    params = {'grant_type':'client_credentials'}
    headers = {'Authorization': f'Basic {client_creds_b64.decode()}'}
    response_token = requests.post(token_url,data=params,headers=headers)
    access_token = response_token.json()['access_token']

    #Creating headers with authorization
    headers = {'Authorization' : f'Bearer {access_token}'}

    #Asking for an artist and formating the input
    search_input = str(input("ESCRIBE UN ARTISTA MUSICAL: ").replace(' ','+'))

    #Getting artist id    
    def get_artist_id():
        url_search='https://api.spotify.com/v1/search'
        search_params={'q':f"{search_input}",'type':'artist','market':'MX'}
        
        search=requests.get(url_search,headers=headers,params=search_params)
        raw_df = pd.DataFrame(search.json()['artists']['items'])

        return raw_df.iloc[0]['id']


    url_base = 'https://api.spotify.com/v1'


    def get_albums():
        
        ep_artist = '/artists/{artist_id}/albums'
        id_artist = get_artist_id()
        artist_url = url_base+ep_artist.format(artist_id=id_artist)
        response_artist = requests.get(artist_url,headers=headers,params={'country': 'MX','limit':50})
        #print('Se encontraron '+str(len(response_artist.json()['items']))+ ' Albums')
        return [ album['id'] for album in response_artist.json()['items']]


    def get_tracks(album_id):
        track_url = f'{url_base}/albums/{album_id}/tracks'
        response_tracks = requests.get(track_url,headers=headers, params={'market':'MX'})
        tracks = [track['id'] for track in response_tracks.json()['items']]
        return tracks


    def get_track_ids():
        tracks_ids = [] 
        print('🎵 Obteniendo y Procesando Canciones ...')
        for album in get_albums():
            album_id = album
            for track in get_tracks(album_id):
                try:
                    tracks_ids.append(track)
                except:
                    print(Exception)
                    continue
        return tracks_ids



    def get_all_track_info():
        data = []
        print('Buscando Información del Artista ...')
        print('🔎 Analizando Albums')
        for id in get_track_ids():
            try:
                track_url = f'{url_base}/tracks/{id}'
                response_track = requests.get(track_url,headers=headers,params={'market':'MX'})
                if 'error' in response_track.json():
                    pass
                else:
                    data.append(response_track.json())
            except Exception as e:
                print(e)
                continue
        return data

    raw_df= pd.DataFrame(get_all_track_info())
    raw_df['artist'] = search_input.replace('+',' ').title()
    file_name = search_input.replace('+','_')
    raw_df.to_csv(f'./data/{file_name}.csv',index=False,encoding='utf-8')
