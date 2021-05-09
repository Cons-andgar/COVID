import requests
import datetime
import pandas
from pathlib import Path

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

def get_dframe():
    path = download_iscii_data() 
    dframe = pandas.read_csv(path, parse_dates = ['fecha'], index_col=['fecha'])
    return dframe



def incidencia_acumulada_ccaa():

        #cargamos el diccionario y datos
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        pops_per_ca = diccionariosaida._get_ca_population()
        ccaa_names = diccionariosaida._get_ccaa_names()
        #ccaa_names = sorted(ccaa_names.items())
        dframe = trabajo1.get_dframe()

        #incidencia por ccaa
        num_casos_por_provincia = dframe.loc[:,('provincia_iso','num_casos')].groupby(by='provincia_iso').sum()
        ccaa = pd.DataFrame(columns=('CCAA','num_casos','num_casos_densidad','incidencia_acumulada_100mil'))
        ca = provinces_per_ca.keys()
        ca = sorted(ca)
        ccaa['CCAA'] = ca
        #ccaa['nombre'] = ccaa_names

        numero_casos = numpy.zeros((len(ca),1))
        numero_casos_densidad = numpy.zeros((len(ca),1))
        inc_acumulada_100 = numpy.zeros((len(ca),1))

        n=0
        for ca, province in provinces_per_ca.items():
            mask = num_casos_por_provincia.loc[province]
            num_casos = mask.sum()
            num_casos_densidad = num_casos/pops_per_ca[ca]
            inc_acumul_100 = (num_casos*100000)/pops_per_ca[ca]
            numero_casos[n] = num_casos
            numero_casos_densidad[n] = num_casos_densidad
            inc_acumulada_100[n] = inc_acumul_100
            n=n+1


        ccaa['num_casos'] = numero_casos
        ccaa['num_casos_densidad'] = numero_casos_densidad
        ccaa['incidencia_acumulada_100mil'] = inc_acumulada_100

        source = ColumnDataSource(data=ccaa)
        neighborhoods = source.data['index'].tolist()
        
        # creamos y guardamos la figura
        # numero de casos por ccaa
        p_ccaa = figure(plot_height = 300, plot_width = 380, 
                background_fill_color= '#EBF5FB',
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                title = 'Incidencia acumulada por comunidad autónoma en los últimos 14 días',
                x_axis_label = 'Incidencia acumulada cada 100.000 habitantes', 
                y_axis_label = 'Comunidades Autónomas',
                tools='hover',
                y_range = (len(ca)),
                toolbar_location = None)
        #p = figure(plot_height = 300, plot_width = 380,
                    #y_range = (len(ca)), toolbar_location = None)


        p.hbar(y=y_range, right=source.data['num_casos'], source=source, height=0.95, line_color='white', color ="#DF8F44")

        p.x_range.start = 0  # start value of the x-axis
        hover = HoverTool()  # initiate hover tool
        hover.tooltips = [("Neighborhood","@index"),   ## define the content of the hover tooltip
                        ("Number of killnings","@neighborhood")]
        hover.mode = 'hline' # set the mode of the hover tool
        p.add_tools(hover)   # add the hover tooltip to the plot
        # style the plot
        p.xaxis.major_label_text_font = 'IBM Plex Mono'
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font = 'IBM Plex Mono'
        p.yaxis.major_label_text_font_size = '13pt'

        return(p_ccaa)

    p_ccaa = incidencia_acumulada_ccaa()
    script_inac, div_inac = components(p_ccaa)
    cdn_js_inac=CDN.js_files[0]
    cdn_css_inac=CDN.css_files[0]




