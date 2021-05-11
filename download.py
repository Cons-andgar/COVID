
from jinja2 import Template
import datetime 
from pathlib import Path
import requests
import pandas
import numpy
from pprint import pprint

URL_ISCIII = 'https://cnecovid.isciii.es/covid19/resources/casos_hosp_uci_def_sexo_edad_provres.csv'
BASE_DIR = Path()
CACHE_DIR = BASE_DIR/'cache'
CACHE_DIR.mkdir(exist_ok=True) # Si ya está creado no hace nada
ORIG_DATE_COL = 'fecha' 
ORIG_CASES_COL = 'num_casos'
ORIG_HOSP_COL = 'num_hosp'
ORIG_UCI_COL = 'num_def'
ORIG_DEF_COLS = 'num_def'
DATA_COLS = [ORIG_CASES_COL, ORIG_HOSP_COL, ORIG_UCI_COL, ORIG_DEF_COLS] 
PROV_ISO_COL = 'provincia_iso'

EVOLUTION_PLOT_DIR = BASE_DIR/'evolutions'


def download_iscii_data(): 

    fname = URL_ISCIII.split('/')[-1]# -1 para quedarme con el último elemento de la lista
    now = datetime.datetime.now()

    fname = f'{now.year}_{now.month}_{now.day}_{fname}'
    path = CACHE_DIR / fname #creamos un directorio en el que guardaremos los ficheros de cada día que se ejecute

    if path.exists(): 
        return path # se sale de la función y devuleve el valor
 
    print('no existo')

    response = requests.get(URL_ISCIII)

    if response.status_code != 200:
        raise RuntimeError(f'Error downloading file: {URL_ISCIII}')

    fpath = 'datos.cv'
    fhand = path.open('wb')
    for chunk in response.iter_content(chunk_size=128): # descarga los datos en trozos y los guarda en el fichero creado 
        fhand.write(chunk)

    return path
   
def get_dframe(date_range=None): 
    path = download_iscii_data()
    
    dframe = pandas.read_csv(path, header = 0, parse_dates = [ORIG_DATE_COL]) #devuelve un dataframe = array con las columnas y filas nombradas
    # las columnas pueden tener tipos distintos
    
    if date_range is not None:
        mask = numpy.logical_and(dframe[ORIG_DATE_COL] >=date_range[0],
                                dframe[ORIG_DATE_COL] <=date_range[1]) 
        #serie de booleanos que nos dice las fechas superiores a la primera fecha e inferiores a la segunda
        dframe = dframe.loc[mask,:]

    print(dframe)

    return dframe 


def region_evolution(date_range=None):
    dframe = get_dframe(date_range=date_range)

    # Diccionario: 
    dframes_by_param = {} 
    for param in DATA_COLS: 
        result = dframe.groupby(by = [ORIG_DATE_COL, PROV_ISO_COL]).sum()

        evol_per_region_for_param = result[param].unstack(level=1)

        dframes_by_param[param] = evol_per_region_for_param

    return dframes_by_param
        

    



if __name__ == '__main__':

    last_date = datetime.datetime.now()
    two_weeks = datetime.timedelta(days=14)
    first_date = last_date - two_weeks
    dates = (first_date,last_date)
    plot_evolution_per_region(date_range=dates)


    








