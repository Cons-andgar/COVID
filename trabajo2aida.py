import trabajo1
import diccionariosaida

import pandas
import pandas as pd
import numpy
from pathlib import Path
import datetime

import matplotlib.pyplot as plt


DIR_FIG = Path() / 'figurasTrabajo'
DIR_FIG.mkdir(exist_ok=True)

def incidencia_acumulada_subplot():

    out_dir = DIR_FIG

    #obtenemos el dataframe
    dframe = trabajo1.get_dframe()

    #incidencia acumulada por semana
    num_casos = dframe['num_casos']
    num_hosp = dframe['num_hosp']
    num_def = dframe['num_def']
    num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
    num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
    num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

    #creamos y guardamos la figura
    
    #plt.grid()
    fig, (axs1, axs2, axs3) = plt.subplots(nrows=1, ncols=3)
    fig.set_size_inches(18,8)
    fig.autofmt_xdate(rotation=45)

    axs1.plot(num_casos_por_semana.index, num_casos_por_semana) 
    axs1.set_title('Casos semanales en España')
    axs1.grid(axis='y')
    axs1.spines['top'].set_visible(False) 
    axs1.spines['right'].set_visible(False)
    axs1.spines['left'].set_visible(False)    

    axs2.plot(num_hosp_por_semana.index, num_hosp_por_semana, color='orange') 
    axs2.set_title('Hospitalizaciones semanales en España')
    axs2.grid(axis='y')
    axs2.spines['top'].set_visible(False)
    axs2.spines['right'].set_visible(False)
    axs2.spines['left'].set_visible(False)  

    axs3.plot(num_def_por_semana.index, num_def_por_semana, color='k') 
    axs3.set_title('Defunciones semanales en España')
    axs3.grid(axis='y')
    axs3.spines['top'].set_visible(False)
    axs3.spines['right'].set_visible(False)
    axs3.spines['left'].set_visible(False)  

    #plot.set_x_ticks_format(num_casos_por_semana.index, 45, ha='right')
    plot_path = out_dir / 'numero_casos_por_semana_subplot.png'
    plt.savefig(plot_path)

    return num_casos_por_semana

def incidencia_acumulada_ccaa():

    out_dir = DIR_FIG

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

    last_date = datetime.datetime.now()
    two_weeks = datetime.timedelta(days=14)
    first_date = last_date - two_weeks


    dates = (first_date, last_date)

    incidencia_acumulada_subplot()
    #incidencia_acumulada_ccaa()