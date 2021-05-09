import trabajo1
import pandas
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import diccionarios
import numpy
import datetime

DIR_FIG = Path() / 'figurasTrabajo'
DIR_FIG.mkdir(exist_ok=True)

def incidencia_acumulada():

    out_dir = DIR_FIG

    #obtenemos el dataframe
    dframe = trabajo1.get_dframe()

    #incidencia acumulada por semana
    num_casos = dframe['num_casos']
    num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()

    #creamos y guardamos la figura
    plt.plot(num_casos_por_semana.index, num_casos_por_semana) 
    plt.ylabel('Número de casos por semana')
    plt.xlabel('Fechas')
    plot_path = out_dir / 'numero_casos_por_semana.png'
    plt.savefig(plot_path)

def incidencia_acumulada_14(date_range=None):

    out_dir = DIR_FIG
    dframe = trabajo1.get_dframe(date_range=date_range)
    dframe.set_index('fecha', inplace=True)
    
    num_casos = dframe['num_casos']
    num_casos_por_semana = num_casos.groupby(by='fecha').sum()

    plt.plot(num_casos_por_semana.index, num_casos_por_semana) 
    plt.ylabel('Número de casos - últimos 14 días')
    plt.xlabel('Fechas')
    plot_path = out_dir / 'numero_casos_14dias.png'
    plt.savefig(plot_path)


def incidencia_acumulada_ccaa_simple():

    out_dir = DIR_FIG

    #cargamos el diccionario y datos
    provinces_per_ca = diccionarios._get_provinces_per_ca()
    dframe = trabajo1.get_dframe()


    # incidencia por ccaa
    num_casos_por_provincia = dframe.loc[:,('provincia_iso','num_casos')].groupby(by='provincia_iso').sum()
    ccaa = pd.DataFrame(columns=('CCAA','num_casos'))
    ca = provinces_per_ca.keys()
    ccaa['CCAA'] = ca
    numero_casos = numpy.zeros((len(ca),1))
    n=0
    for ca, province in provinces_per_ca.items():
        mask = num_casos_por_provincia.loc[province]
        num_casos = mask.sum()
        numero_casos[n] = num_casos
        n=n+1
    ccaa['num_casos'] = numero_casos

    #creamos y guardamos la figura
    plt.bar(ccaa['CCAA'], ccaa['num_casos'])
    plt.ylabel('Comunidades autónomas')
    plt.xlabel('Número de casos por CCAA')
    plot_path = out_dir / 'numero_casos_por_ccaa.png'
    plt.savefig(plot_path)


def incidencia_acumulada_ccaa(date_range=None):

    out_dir = DIR_FIG

    #cargamos el diccionario y datos
    provinces_per_ca = diccionarios._get_provinces_per_ca()
    pops_per_ca = diccionarios._get_ca_population()
    ccaa_names = diccionarios._get_ccaa_names()
    #ccaa_names = sorted(ccaa_names.items())
    dframe = trabajo1.get_dframe(date_range=date_range)
    dframe.set_index('fecha', inplace=True)

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

    # creamos y guardamos la figura
    # numero de casos por ccaa
    plt.figure(1)
    plt.bar(ccaa['CCAA'], ccaa['num_casos'])
    plt.xlabel('Comunidades autónomas')
    plt.ylabel('Número de casos por CCAA')
    plot_path = out_dir / 'numero_casos_por_ccaa.png'
    plt.savefig(plot_path)
    #incidencia acumulada por 100mil habitantes
    plt.figure(2)
    plt.bar(ccaa['CCAA'], ccaa['incidencia_acumulada_100mil'])
    plt.xlabel('Comunidades autónomas')
    plt.ylabel('Incidencia acumulada')
    plt.title('Incidencia acumulada por comunidad autónoma')
    plot_path = out_dir / 'incidencia_acumulada_100mil.png'
    plt.savefig(plot_path)

    return ccaa


if __name__ == '__main__':

    last_day = datetime.datetime.now() - datetime.timedelta(days=7)
    two_weeks = datetime.timedelta(days = 14)
    first_day = last_day - two_weeks

    dates = (first_day, last_day)
    incidencia_acumulada_ccaa(date_range=dates)