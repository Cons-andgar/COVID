#VERSIÓN DE CONS de la mañana del domingo 09 de marzo

from flask import Flask, render_template

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html

import trabajo1
import pandas
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import diccionariosaida
import numpy
import numpy as np
import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, Axis, Grid, HBar, LinearAxis, Plot
from bokeh.models.tools import HoverTool
from bokeh.layouts import gridplot
from bokeh.models.glyphs import VBar


app = Flask(__name__)

@app.route('/')
def index():

    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    def incidencia_acumulada():
        dframe = trabajo1.get_dframe()

        #incidencia acumulada por semana
        dframe_fecha = dframe.groupby(by='fecha').sum().resample('7D').sum()
        num_casos_por_semana = dframe_fecha['num_casos']
        num_hosp_por_semana = dframe_fecha['num_hosp']
        num_def_por_semana = dframe_fecha['num_def']
        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        #figura casos
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height = 300, plot_width = 380,
                background_fill_color= '#EBF5FB',
                x_axis_type="datetime",
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                x_range=(xmin, xmax), y_range=(ymin, ymax),
                title = 'Casos semanales en España',
                x_axis_label = 'Fecha',
                y_axis_label = 'Numero de casos por semana')

        p_casos.xgrid.visible = False
        p_casos.line(num_casos_por_semana.index,num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4,
          color='darkgrey', alpha=0.2)

        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        #hover_casos=p_casos.select(dict(type=HoverTool))
        #hover_casos.tooltips=[("Nº casos","$num_casos_por_semana")]
        #hover_casos.mode='mouse'

        #figura hospitalizaciones
        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height = 300, plot_width = 380,
                x_axis_type="datetime",
                #ygrid.band_fill_color == "olive",
                background_fill_color= '#EBF5FB',
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                x_range=(xmin, xmax), y_range=(ymin, ymax),
                title = 'Hospitalizaciones semanales en España',
                x_axis_label = 'Fecha',
                y_axis_label = 'Numero de hospitalizaciones por semana')

        p_hosp.xgrid.visible = False
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4,
          color='darkgrey', alpha=0.2)
        p_hosp.line(num_hosp_por_semana.index,num_hosp_por_semana,color="#2980B9")

        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        #figura defunciones
        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height = 300, plot_width = 380,
                x_axis_type="datetime",
                background_fill_color= '#EBF5FB',
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                x_range=(xmin, xmax), y_range=(ymin, ymax),
                title = 'Número de defunciones por semana',
                x_axis_label = 'Fecha',
                y_axis_label = 'Defunciones semanales en España')

        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index,num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4,
          color='darkgrey', alpha=0.2)

        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return(p_casos,p_hosp,p_def,casos,defunciones)
    
    p_casos = incidencia_acumulada()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = incidencia_acumulada()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_def = incidencia_acumulada()[2]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos = incidencia_acumulada()[3]
    defunciones = incidencia_acumulada()[4]
    population_esp = sum(diccionariosaida._get_ca_population().values())
    porcentaje = round((casos / population_esp) * 100, 2)


    return render_template('index.html', 
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos=casos, defunciones=defunciones, porcentaje= porcentaje)




@app.route('/ccaa')
def ccaa(): 
    return render_template('ccaa.html')

@app.route('/infocovid')
def infocovid(): 
    return render_template('infocovid.html')

@app.route('/documentacion')
def documentacion(): 
    return render_template('documentacion.html')

@app.route('/estadisticas')
def estadisticas(): 
    return render_template('estadisticas.html')



#############################################################
# ARAGÓN 
#############################################################

@app.route('/aragon')
def aragon(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
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

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)


    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_aragon = graficas()[4]
    defunciones_aragon = graficas()[5]
    population_aragon =diccionariosaida._get_ca_population()['AR']
    porcentaje = round((casos_aragon/population_aragon)*100,2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['ZA', 'TE', 'HU']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['ZA', 'TE', 'HU']
        ca = 'AR'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('aragon.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos=casos_aragon, defunciones=defunciones_aragon, porcentaje = porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
                            
#############################################################
# ANDALUCÍA 
#############################################################

@app.route('/andalucia')
def andalucia(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['AL','CA','CO','GR','H','J','MA','SE']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_and = graficas()[4]
    defunciones_and = graficas()[5]
    population_and = diccionariosaida._get_ca_population()['AN']
    porcentaje = round((casos_and / population_and) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['AL','CA','CO','GR','H','J','MA','SE']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['AL','CA','CO','GR','H','J','MA','SE']
        ca = 'AN'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('andalucia.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_and, defunciones=defunciones_and, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
                            
#############################################################
# ASTURIAS 
#############################################################

@app.route('/asturias')
def asturias():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['O'] 
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_ast = graficas()[4]
    defunciones_ast = graficas()[5]
    population_as = diccionariosaida._get_ca_population()['AS']
    porcentaje = round((casos_ast / population_as) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['O']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['O']
        ca = 'AS'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('asturias.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_ast, defunciones= defunciones_ast, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)

#############################################################
# BALEARES 
#############################################################

@app.route('/baleares')
def baleares():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['PM'] 
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_bal= graficas()[4]
    defunciones_bal= graficas()[5]
    population_bal = diccionariosaida._get_ca_population()['IB']
    porcentaje = round((casos_bal / population_bal) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['PM']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['PM']
        ca = 'IB'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('baleares.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_bal, defunciones= defunciones_bal, porcentaje = porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
                            
#############################################################
# CANARIAS 
#############################################################

@app.route('/canarias')
def canarias(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['GC','TF']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()
        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_can= graficas()[4]
    defunciones_can= graficas()[5]
    population_can = diccionariosaida._get_ca_population()['CN']
    porcentaje = round((casos_can / population_can) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['GC','TF']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['GC','TF']
        ca = 'CN'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('canarias.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_can, defunciones= defunciones_can, porcentaje = porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# CANTABRIA
#############################################################

@app.route('/cantabria')
def cantabria(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['S'] 
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()
        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_cant= graficas()[4]
    defunciones_cant= graficas()[5]
    population_cant = diccionariosaida._get_ca_population()['CB']
    porcentaje = round((casos_cant / population_cant) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['S']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['S']
        ca = 'CB'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('cantabria.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_cant, defunciones= defunciones_cant, porcentaje = porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)

    
#############################################################
# CASTILLA LA MANCHA 
#############################################################

@app.route('/castillalamancha')
def castillalamancha():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['AB','CR','CU','GU','TO']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()
        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_cm= graficas()[4]
    defunciones_cm= graficas()[5]

    population_cm = diccionariosaida._get_ca_population()['CM']
    porcentaje = round((casos_cm / population_cm) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['AB','CR','CU','GU','TO']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['AB','CR','CU','GU','TO']
        ca = 'CM'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('castillalamancha.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_cm, defunciones= defunciones_cm, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# CASTILLA Y LEÓN
#############################################################

@app.route('/castillaleon')
def castillaleon():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['AV','BU','TF','LE','P','SA','SG','SO','VA','ZA']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_cl = graficas()[4]
    defunciones_cl = graficas()[5]
    population_cl = diccionariosaida._get_ca_population()['CL']
    porcentaje = round((casos_cl / population_cl) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['AV','BU','TF','LE','P','SA','SG','SO','VA','ZA']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['AV','BU','TF','LE','P','SA','SG','SO','VA','ZA']
        ca = 'CL'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]
    return render_template('castillaleon.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_cl, defunciones= defunciones_cl, porcentaje = porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# CATALUÑA
#############################################################

@app.route('/cataluna')
def cataluna(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['B','GI','L','T']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_cat = graficas()[4]
    defunciones_cat= graficas()[5]
    population_cat = diccionariosaida._get_ca_population()['CT']
    porcentaje = round((casos_cat / population_cat) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['B','GI','L','T']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['B','GI','L','T']
        ca = 'CT'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('cataluna.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_cat, defunciones= defunciones_cat, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)

#############################################################
# CEUTA
#############################################################

@app.route('/ceuta')
def ceuta():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['CE'] # MAL
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_ceu= graficas()[4]
    defunciones_ceu = graficas()[5]
    population_ceu = diccionariosaida._get_ca_population()['CE']

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['CE']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['CE']
        ca = 'CE'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    porcentaje = round((casos_ceu / population_ceu) * 100, 2)
    return render_template('ceuta.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_ceu, defunciones = defunciones_ceu, porcentaje=porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# EXTREMADURA 
#############################################################

@app.route('/extremadura')
def extremadura(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['BA','CC']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_ext= graficas()[4]
    defunciones_ext = graficas()[5]
    population_ext = diccionariosaida._get_ca_population()['EX']
    porcentaje = round((casos_ext / population_ext) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['BA','CC']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['BA','CC']
        ca = 'EX'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('extremadura.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_ext, defunciones = defunciones_ext, porcentaje=porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# GALICIA
#############################################################

@app.route('/galicia')
def galicia(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['C','LU','OR','PO']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_gal = graficas()[4]
    defunciones_gal = graficas()[5]
    population_gal = diccionariosaida._get_ca_population()['GA']
    porcentaje = round((casos_gal / population_gal) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['C','LU','OR','PO']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['C','LU','OR','PO']
        ca = 'GA'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('galicia.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_gal, defunciones = defunciones_gal, porcentaje=porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# MADRID 
#############################################################

@app.route('/madrid')
def madrid(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['M'] 
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_mad= graficas()[4]
    defunciones_mad = graficas()[5]
    population_mad = diccionariosaida._get_ca_population()['MD']
    porcentaje = round((casos_mad / population_mad) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['M']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['M']
        ca = 'MD'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('madrid.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_mad, defunciones = defunciones_mad, porcentaje=porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# MELILLA 
#############################################################

@app.route('/melilla')
def melilla(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['ML'] # MAL
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_mel = graficas()[4]
    defunciones_mel = graficas()[5]
    population_mel = diccionariosaida._get_ca_population()['ML']
    porcentaje = round((casos_mel / population_mel) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['ML']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['ML']
        ca = 'ML'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]


    return render_template('melilla.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_mel, defunciones= defunciones_mel, porcentaje=porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# MURCIA
#############################################################

@app.route('/murcia')
def murcia():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['MU'] # MAL
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        # GRAFICAS
        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_mur= graficas()[4]
    defunciones_mur= graficas()[5]
    population_mur = diccionariosaida._get_ca_population()['MC']
    porcentaje = round((casos_mur / population_mur) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['MU']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['MU']
        ca = 'MC'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]


    return render_template('murcia.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_mur, defunciones= defunciones_mur, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# NAVARRA
#############################################################

@app.route('/navarra')
def navarra():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['NC']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_nav= graficas()[4]
    defunciones_nav= graficas()[5]
    population_nav = diccionariosaida._get_ca_population()['NC']
    porcentaje = round((casos_nav / population_nav) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['NC']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['NC']
        ca = 'NC'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('navarra.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos= casos_nav, defunciones= defunciones_nav, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# PAÍS VASCO
#############################################################

@app.route('/paisvasco')
def paisvasco():
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['VI','BI','SS']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_pv = graficas()[4]
    defunciones_pv= graficas()[5]
    population_pv = diccionariosaida._get_ca_population()['PV']
    porcentaje = round((casos_pv / population_pv) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['VI','BI','SS']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['VI','BI','SS']
        ca = 'PV'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]

    return render_template('paisvasco.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_pv, defunciones= defunciones_pv, porcentaje= porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# LA RIOJA
#############################################################

@app.route('/rioja')
def rioja(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['LO']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height=250, plot_width=260,
                        x_axis_type="datetime",
                        background_fill_color='#EBF5FB',
                        border_fill_color='#EBF5FB',
                        outline_line_color='#EBF5FB',
                        x_range=(xmin, xmax), y_range=(ymin, ymax),
                        title='Hospitalizaciones por semana',
                        x_axis_label='Fecha',
                        y_axis_label='Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index, num_hosp_por_semana, color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
            tooltips=[
                ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       # ygrid.band_fill_color == "olive",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Pacientes en UCI por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index, num_uci_por_semana, color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
            tooltips=[
                ('UCI', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height=250, plot_width=260,
                       x_axis_type="datetime",
                       background_fill_color='#EBF5FB',
                       border_fill_color='#EBF5FB',
                       outline_line_color='#EBF5FB',
                       x_range=(xmin, xmax), y_range=(ymin, ymax),
                       title='Defunciones por semana',
                       x_axis_label='Fecha',
                       y_axis_label='Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index, num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return (p_casos, p_hosp, p_uci, p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_rio = graficas()[4]
    defunciones_rio = graficas()[5]
    population_rio = diccionariosaida._get_ca_population()['RI']
    porcentaje = round((casos_rio / population_rio) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['LO']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['LO']
        ca = 'RI'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]


    return render_template('rioja.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_rio, defunciones= defunciones_rio, porcentaje = porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)
    
#############################################################
# COMUNIDAD VALENCIANA
#############################################################

@app.route('/valenciana')
def valenciana(): 
    def graficas():
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        dframe = trabajo1.get_dframe()
        dframe.set_index('fecha', inplace=True)

        values = ['A','CS','V']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos']
        num_casos_por_semana = num_casos.groupby(by='fecha').sum().resample('7D').sum()
        num_hosp = dframe['num_hosp']
        num_hosp_por_semana = num_hosp.groupby(by='fecha').sum().resample('7D').sum()
        num_uci = dframe['num_uci']
        num_uci_por_semana = num_uci.groupby(by='fecha').sum().resample('7D').sum()
        num_def = dframe['num_def']
        num_def_por_semana = num_def.groupby(by='fecha').sum().resample('7D').sum()

        casos = dframe['num_casos'].sum()
        defunciones = dframe['num_def'].sum()

        source = ColumnDataSource(data={'x': num_casos_por_semana.index,
                                        'y': num_casos_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_casos_por_semana.index), max(num_casos_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_casos_por_semana), max(num_casos_por_semana)
        p_casos = figure(plot_height=250, plot_width=260,
                         background_fill_color='#EBF5FB',
                         x_range=(xmin, xmax), y_range=(ymin, ymax),
                         x_axis_type="datetime",
                         border_fill_color='#EBF5FB',
                         outline_line_color='#EBF5FB',
                         title='Casos por semana',
                         x_axis_label='Fecha',
                         y_axis_label='Número de casos')
        p_casos.xgrid.visible = False

        p_casos.line(num_casos_por_semana.index, num_casos_por_semana, color="#CB4335")
        p_casos.circle(num_casos_por_semana.index, num_casos_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_casos.add_tools(HoverTool(
            tooltips=[
                ('Casos', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_hosp_por_semana.index,
                                        'y': num_hosp_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_hosp_por_semana.index), max(num_hosp_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_hosp_por_semana), max(num_hosp_por_semana)
        p_hosp = figure(plot_height = 250, plot_width = 260, 
                x_axis_type="datetime",
                background_fill_color= '#EBF5FB',
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                x_range=(xmin, xmax), y_range=(ymin, ymax),
                title = 'Hospitalizaciones por semana',
                x_axis_label = 'Fecha', 
                y_axis_label = 'Numero de hospitalizaciones')
        p_hosp.xgrid.visible = False
        p_hosp.line(num_hosp_por_semana.index,num_hosp_por_semana,color="#2980B9")
        p_hosp.circle(num_hosp_por_semana.index, num_hosp_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_hosp.add_tools(HoverTool(
                tooltips=[
                    ('Hospitalizaciones', '@y'),  # use @{ } for field names with spaces
                    ('Fecha', '@x{%F}'), ],
                formatters={
                    '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_uci_por_semana.index,
                                        'y': num_uci_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_uci_por_semana.index), max(num_uci_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_uci_por_semana), max(num_uci_por_semana)
        p_uci = figure(plot_height = 250, plot_width = 260, 
                x_axis_type="datetime",
                #ygrid.band_fill_color == "olive",
                background_fill_color= '#EBF5FB',
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                x_range=(xmin, xmax), y_range=(ymin, ymax),
                title = 'Pacientes en UCI por semana',
                x_axis_label = 'Fecha', 
                y_axis_label = 'Numero de pacientes en la UCI')
        p_uci.xgrid.visible = False
        p_uci.line(num_uci_por_semana.index,num_uci_por_semana,color="#E67E22")
        p_uci.circle(num_uci_por_semana.index, num_uci_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_uci.add_tools(HoverTool(
                    tooltips=[
                    ('UCI', '@y'),  # use @{ } for field names with spaces
                    ('Fecha', '@x{%F}'), ],
                    formatters={
                        '@x': 'datetime', }, ))

        source = ColumnDataSource(data={'x': num_def_por_semana.index,
                                        'y': num_def_por_semana})

        # Save the minimum and maximum values of the date column: xmin, xmax
        xmin, xmax = min(num_def_por_semana.index), max(num_def_por_semana.index)

        # Save the minimum and maximum values of the cases column: ymin, ymax
        ymin, ymax = min(num_def_por_semana), max(num_def_por_semana)

        p_def = figure(plot_height = 250, plot_width = 260,
                x_axis_type="datetime", 
                background_fill_color= '#EBF5FB',
                border_fill_color= '#EBF5FB',
                outline_line_color= '#EBF5FB',
                x_range=(xmin, xmax), y_range=(ymin, ymax),
                title = 'Defunciones por semana',
                x_axis_label = 'Fecha', 
                y_axis_label = 'Numero de defunciones')
        p_def.xgrid.visible = False
        p_def.line(num_def_por_semana.index,num_def_por_semana, color="#212F3C")
        p_def.circle(num_def_por_semana.index, num_def_por_semana, size=4, color='darkgrey', alpha=0.2)
        p_def.add_tools(HoverTool(
            tooltips=[
                ('Defunciones', '@y'),  # use @{ } for field names with spaces
                ('Fecha', '@x{%F}'), ],
            formatters={
                '@x': 'datetime', }, ))

        return(p_casos,p_hosp,p_uci,p_def, casos, defunciones)

    p_casos = graficas()[0]
    script_casos, div_casos = components(p_casos)
    cdn_js_casos=CDN.js_files[0]
    cdn_css_casos=CDN.css_files[0]

    p_hosp = graficas()[1]
    script_hosp, div_hosp = components(p_hosp)
    cdn_js_hosp=CDN.js_files[0]
    cdn_css_hosp=CDN.css_files[0]

    p_uci = graficas()[2]
    script_uci, div_uci = components(p_uci)
    cdn_js_uci=CDN.js_files[0]
    cdn_css_uci=CDN.css_files[0]

    p_def = graficas()[3]
    script_def, div_def = components(p_def)
    cdn_js_def=CDN.js_files[0]
    cdn_css_def=CDN.css_files[0]

    casos_cv= graficas()[4]
    defunciones_cv= graficas()[5]
    population_cv = diccionariosaida._get_ca_population()['VC']
    porcentaje = round((casos_cv / population_cv) * 100, 2)

    def datos(date_range=None):
        dframe = trabajo1.get_dframe(date_range=date_range)
        dframe.set_index('fecha', inplace=True)

        values = ['A','CS','V']
        dframe = dframe[dframe.provincia_iso.isin(values)]

        num_casos = dframe['num_casos'].sum()
        num_hosp = dframe['num_hosp'].sum()
        num_uci = dframe['num_uci'].sum()
        num_def = dframe['num_def'].sum()

        # porcentaje de contagiados
        dframe2 = trabajo1.get_dframe(date_range=None)
        dframe2.set_index('fecha', inplace=True)
        pops_per_ca = diccionariosaida._get_ca_population()

        provin = ['A','CS','V']
        ca = 'VC'
        dframe2 = dframe2[
            dframe2.provincia_iso.isin(provin)]  # cogemos solo las filas de las provincias que nos interesan
        num_casos_por_provincia = dframe2.loc[:, ('provincia_iso', 'num_casos', 'num_def')].groupby(
            by='provincia_iso').sum()  # agrupamos por cada provincia

        num_casos_ca = num_casos_por_provincia['num_casos'].sum()
        num_def_ca = num_casos_por_provincia['num_def'].sum()
        porcentaje_contagiados = num_casos_ca * 100 / pops_per_ca[ca]

        return num_casos, num_hosp, num_uci, num_def, porcentaje_contagiados, num_casos_ca, num_def_ca
    # DATOS TABLA
    now = datetime.datetime.now() - datetime.timedelta(days=7)
    one_week = datetime.timedelta(days=7)
    first_day = now - one_week
    fechas = (first_day, now)
    num_casos = datos(fechas)[0]
    num_hosp = datos(fechas)[1]
    num_uci = datos(fechas)[2]
    num_def = datos(fechas)[3]


    return render_template('valenciana.html',
                            script_casos=script_casos, div_casos=div_casos,cdn_js_casos=cdn_js_casos,cdn_css_casos=cdn_css_casos,
                            script_hosp=script_hosp, div_hosp=div_hosp,cdn_js_hosp=cdn_js_hosp,cdn_css_hosp=cdn_css_hosp,
                            script_uci=script_uci, div_uci=div_uci,cdn_js_uci=cdn_js_uci,cdn_css_uci=cdn_css_uci,
                            script_def=script_def, div_def=div_def,cdn_js_def=cdn_js_def,cdn_css_def=cdn_css_def,
                            casos = casos_cv, defunciones= defunciones_cv, porcentaje=porcentaje,
                            num_casos=num_casos,num_hosp=num_hosp,num_uci=num_uci,num_def=num_def)





if __name__ == '__main__': 
    app.run(debug=True,port=5017)
