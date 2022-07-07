from pandas.io import gbq
from clean import clean


def send(data):
    print('🚀 Enviando información...')
    data.to_gbq(destination_table='spotify.songs',
    project_id='general-project-352815',
    if_exists='replace')