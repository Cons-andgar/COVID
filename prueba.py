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


#cargamos el diccionario y datos
provinces_per_ca = diccionariosaida._get_provinces_per_ca()
pops_per_ca = diccionariosaida._get_ca_population()
ccaa_names = diccionariosaida._get_ccaa_names()
dframe = trabajo1.get_dframe()

#incidencia por ccaa
num_casos_por_provincia = dframe.loc[:,('provincia_iso','num_casos')].groupby(by='provincia_iso').sum()
ccaa = pd.DataFrame(columns=('CCAA','num_casos','num_casos_densidad','incidencia_acumulada_100mil'))
ca = provinces_per_ca.keys()
ca = sorted(ca)
ccaa['CCAA'] = ca

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

casos = dframe['num_casos'].sum()

print(casos)



  def incidencia_acumulada_ccaa():
        #cargamos el diccionario y datos
        provinces_per_ca = diccionariosaida._get_provinces_per_ca()
        pops_per_ca = diccionariosaida._get_ca_population()
        ccaa_names = diccionariosaida._get_ccaa_names()
        dframe = trabajo1.get_dframe()

        #incidencia por ccaa
        num_casos_por_provincia = dframe.loc[:,('provincia_iso','num_casos')].groupby(by='provincia_iso').sum()
        ccaa = pd.DataFrame(columns=('CCAA','num_casos','num_casos_densidad','incidencia_acumulada_100mil'))
        ca = provinces_per_ca.keys()
        ca = sorted(ca)
        ccaa['CCAA'] = ca

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

        x = ccaa['CCAA']
        y=ccaa['incidencia_acumulada_100mil']
        #y=ccaa['incidencia_acumulada_100mil'].max().round()
        source = ColumnDataSource(dict(x=x,top=y))

        ccaa_inac = Plot(title=None, plot_width=300, plot_height=300,min_border=0, toolbar_location=None)

        glyph = VBar(x="x", top="top", bottom=0, width=0.01, fill_color= "#2471A3")
        ccaa_inac.add_glyph(source, glyph)

        xaxis = LinearAxis()
        ccaa_inac.add_layout(xaxis, 'below')

        yaxis = LinearAxis()
        ccaa_inac.add_layout(yaxis, 'left')

        #ccaa_inac.xlabel('Comunidades autónomas')
        #ccaa_inac.ylabel('Incidencia acumulada')
        #ccaa_inac.title('Incidencia acumulada por comunidad autónoma')

        #ccaa_inac.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        ccaa_inac.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

        return ccaa_inac

    ccaa_inac = incidencia_acumulada_ccaa()
    script_inac, div_inac = components(ccaa_inac)
    cdn_js_inac=CDN.js_files[0]
    cdn_css_inac=CDN.css_files[0]





    script_inac=script_inac, div_inac=div_inac,cdn_js_inac=cdn_js_inac,cdn_css_inac=cdn_css_inac, 



    <p>Aquí va un texto sobre información de qué es la incidencia acumulada</p>