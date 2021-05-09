import trabajo1
import diccionariosaida
from pathlib import Path
import pandas
import numpy
import datetime

DIR_FIG = Path() / 'figurasTrabajo/figurasIncidenciaComunidades'
DIR_FIG.mkdir(exist_ok=True)

def graficas():

    provinces_per_ca = diccionarios._get_provinces_per_ca()
    dframe = trabajo1.get_dframe()
    dframe.set_index('fecha', inplace=True)

    values = ['ZA','TE','HU']
    dframe = dframe[dframe.provincia_iso.isin(values)]

    num_casos = dframe['num_casos']
    num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
    num_hosp = dframe['num_hosp']
    num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
    num_uci = dframe['num_uci']
    num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
    num_def = dframe['num_def']
    num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

    # GRAFICAS

    p_casos = figure(plot_height = 300, plot_width = 380, 
            background_fill_color= '#EBF5FB',
            x_axis_type="datetime",
            border_fill_color= '#EBF5FB',
            outline_line_color= '#EBF5FB',
            title = 'Número de casos por semana',
            x_axis_label = 'Fecha', 
            y_axis_label = 'Numero de casos por semana',
            tools='hover')
    p_casos.xgrid.visible = False
    p_casos.line(num_casos_por_semana.index,num_casos_por_semana, color="#CB4335")
    hover=p_casos.select(dict(type=HoverTool))
    hover.tooltips=[("Nº casos","$num_casos_por_semana")]
    hover.mode='mouse'

    p_hosp = figure(plot_height = 300, plot_width = 380, 
            x_axis_type="datetime",
            #ygrid.band_fill_color == "olive",
            background_fill_color= '#EBF5FB',
            border_fill_color= '#EBF5FB',
            outline_line_color= '#EBF5FB',
            title = 'Número de hospitalizaciones por semana',
            x_axis_label = 'Fecha', 
            y_axis_label = 'Numero de hospitalizaciones por semana',
            tools='hover')
    p_hosp.xgrid.visible = False
    p_hosp.line(num_hosp_por_semana.index,num_hosp_por_semana,color="#2980B9")
    hover=p_hosp.select(dict(type=HoverTool))
    hover.tooltips=[("Nº hospitalizaciones","$num_hosp_por_semana")]
    hover.mode='mouse'

    p_uci = figure(plot_height = 300, plot_width = 380, 
            x_axis_type="datetime",
            #ygrid.band_fill_color == "olive",
            background_fill_color= '#EBF5FB',
            border_fill_color= '#EBF5FB',
            outline_line_color= '#EBF5FB',
            title = 'Número de pacientes en la UCI por semana',
            x_axis_label = 'Fecha', 
            y_axis_label = 'Numero de pacientes en la UCI por semana',
            tools='hover')
    p_hosp.xgrid.visible = False
    p_hosp.line(num_uci_por_semana.index,num_uci_por_semana,color="#2980B9")
    hover=p_hosp.select(dict(type=HoverTool))
    hover.tooltips=[("Nº pacientes UCI","$num_uci_por_semana")]
    hover.mode='mouse'

    p_def = figure(plot_height = 300, plot_width = 380,
            x_axis_type="datetime", 
            background_fill_color= '#EBF5FB',
            border_fill_color= '#EBF5FB',
            outline_line_color= '#EBF5FB',
            title = 'Número de defunciones por semana',
            x_axis_label = 'Fecha', 
            y_axis_label = 'Numero de defunciones por semana',
            tools='hover')
    p_def.xgrid.visible = False
    p_def.line(num_def_por_semana.index,num_def_por_semana, color="#212F3C")
    hover=p_def.select(dict(type=HoverTool))
    hover.tooltips=[("Nº defunciones","$num_def_por_semana")]
    hover.mode='mouse'

    return(p_casos,p_hosp,p,uci,p_def)

def datos(date_range=None):
    
    dframe = trabajo1.get_dframe(date_range = date_range)
    dframe.set_index('fecha', inplace=True)
    
    values = ['ZA','TE','HU']
    dframe = dframe[dframe.provincia_iso.isin(values)]

    num_casos = dframe['num_casos'].sum()
    num_hosp = dframe['num_hosp'].sum()
    num_uci = dframe['num_uci'].sum()
    num_def = dframe['num_def'].sum()

    #porcentaje de contagiados
    dframe2 = trabajo1.get_dframe(date_range=None)
    dframe2.set_index('fecha', inplace=True)
    pops_per_ca = diccionariosaida._get_ca_population()

    provin = ['ZA','TE','HU']
    ca = 'AR'
    dframe2 = dframe2[dframe2.provincia_iso.isin(provin)] #cogemos solo las filas de las provincias que nos interesan
    num_casos_por_provincia = dframe2.loc[:,('provincia_iso','num_casos','num_def')].groupby(by='provincia_iso').sum() #agrupamos por cada provincia

    num_casos_ca = num_casos_por_provincia['num_casos'].sum()
    num_def_ca = num_casos_por_provincia['num_def'].sum()
    porcentaje_contagiados = num_casos_ca*100/pops_per_ca[ca]

    return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca

def incidencia_acumulada(date_range=None):

    out_dir = DIR_FIG

    provinces_per_ca = diccionariosaida._get_provinces_per_ca() 
    print(provinces_per_ca)
    assert False
    pops_per_pro = diccionariosaida._get_province_population()
    dframe = trabajo1.get_dframe(date_range=date_range)
    dframe.set_index('fecha', inplace=True)

    provin = ['ZA','TE','HU']
    dframe = dframe[dframe.provincia_iso.isin(provin)] 
    num_casos_por_provincia = dframe.loc[:,('provincia_iso','num_casos')].groupby(by='provincia_iso').sum()

    inc_acumulada_100 = numpy.zeros((len(provin),1), dtype=int)
    n=0

    for i in provin:
        num_casos = num_casos_por_provincia.loc[i]
        inc_acumul_100 = (num_casos*100000)/pops_per_pro[i]
        inc_acumulada_100[n] = inc_acumul_100
        n=n+1

    num_casos_por_provincia['incidencia_acumulada_100mil'] = inc_acumulada_100
    num_casos_ordenado = num_casos_por_provincia.sort_values('incidencia_acumulada_100mil', ascending=False)
    nombres_ca = ['País Vasco', 'Madrid', 'Melilla', 'Aragón', 'Cataluña','La Rioja','Cantabria','Castilla la Mancha','Andalucia','Castilla y León','Ceuta','Asturias','Extremadura','Canarias','Galicia','Murcia','Islas Baleares','Comunidad Valenciana','Navarra']

    print(num_casos_ordenado)
    assert False
    
    #incidencia acumulada por 100mil habitantes
    fig, ax = plt.subplots()
    fig.set_size_inches(15,8)
    ax.bar(num_casos_ordenado['provincia_iso'], num_casos_ordenado['incidencia_acumulada_100mil'], width=0.8)
    ax.set_xlabel('Comunidades autónomas', fontsize = 18)
    ax.set_ylabel('Incidencia acumulada', fontsize = 18)
    ax.set_title('Incidencia acumulada por comunidad autónoma por cada 100mil habitantes', fontsize = 20)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize = 14)


    plot_path = out_dir / 'incidencia_acumulada_aragon.png'
    plt.savefig(plot_path)


if __name__ == '__main__':
    
    #graficas()

    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    #datos(date_range = fechas)

    two_weeks = datetime.timedelta(days=14)
    first_date = now - two_weeks
    dates = (first_date, now)
    incidencia_acumulada(date_range=dates)