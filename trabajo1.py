import requests
import datetime
import pandas
from pathlib import Path
import numpy

# url donde hay que descargar los datos
URL_ISCIII = 'https://cnecovid.isciii.es/covid19/resources/casos_hosp_uci_def_sexo_edad_provres.csv'
# creamos directorio donde se guarda los datos
CACHE_DIR = Path() / 'cache'
CACHE_DIR.mkdir(exist_ok=True) #si existe no lo vuelve a crear

def download_iscii_data():

    # para que solo descargue uno al día
    fname = URL_ISCIII.split('/')[-1]
    now = datetime.datetime.now()
    fname = f'{now.year}_{now.month}_{now.day}_{fname}'
    path = CACHE_DIR / fname

    # si el path existe no lo volvemos a descargar
    if path.exists():
        return path # devuelve el path y se sale de la función

    #si no existe
    #leemos los datos
    response = requests.get(URL_ISCIII) 

    # vemos si el status code es que la respuesta es correcta
    if response.status_code != 200:
        raise RuntimeError(f'Error downloading file: {URL_ISCIII}')

    # vamos escribiendo los datos en el fichero fhand poco a poco
    fhand = path.open('wb') # 'wb' es para escribir en binario
    for chunk in response.iter_content(chunk_size=128):
        fhand.write(chunk)

    return path

def get_dframe(date_range=None):
    path = download_iscii_data() 
    dframe = pandas.read_csv(path, header = 0, parse_dates = ['fecha'])
    if date_range is not None: 
        mask = numpy.logical_and(dframe['fecha'] >= date_range[0],dframe['fecha'] <= date_range[1])
        dframe = dframe.loc[mask,:]

    return dframe