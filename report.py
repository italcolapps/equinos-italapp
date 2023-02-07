# -*- coding: UTF-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from jinja2 import Environment, FileSystemLoader
#from weasyprint import HTML
import pandas as pd
import numpy as np
import datetime
# import chart_studio
# chart_studio.tools.set_credentials_file(username='josecastellanosc', api_key='SWgst0jsRKAPvOXZgF1y')
# from chart_studio.plotly import image as PlotlyImage
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from PIL import Image as PILImage
import io
import os
import tempfile
import shutil
from time import sleep
from dash_extensions.snippets import send_file
from dash import no_update


# 'file:///Users/josecastellanos/Documentos/italcol/App Equinos/Reporte/Brio.png'
def pdf_report(data, pais, criadero, equino, etapa, persona, contacto, obs, data_ps):
    with tempfile.TemporaryDirectory() as dir_:
        shutil.copy('Reporte/Brio.png', dir_ + '/Brio.png')
        # dt = data.loc[(data['Nombre Criadero'] == criadero) &
        #                 (data['Nombre Equino'] == equino)]
        data_ps['Próxima vacunación'] = data_ps['Próxima vacunación'].apply(lambda x: x.split('T')[0])
        data['Fecha'] = data['Fecha'].apply(lambda x: x.split('T')[0])
        dt = data.sort_values(by = 'Fecha').copy()
        #print(pd.datetime(dt['Fecha'])) 
        dt_tbl1 = pd.DataFrame({'Fecha': [datetime.date.today()],
                    'Criadero': dt['Nombre Criadero'].unique()[0],
                    'Equino': dt['Nombre Equino'].unique()[0],
                    'Etapa': [etapa],
                    'Sexo': dt['Sexo'].unique(),
                    'Raza': dt['Raza'].unique()}) 

    
        dt_1 = dt_tbl1.to_html(index = False)
        dt_1 = dt_1.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
        dt_1 = dt_1.replace('<td>', '<td style="text-align: center;">')

        dt_2 = dt[['Fecha', 'Días entre visitas', 'GPD (g)', 'Alzada (cm)']].copy()
        dt_2.sort_values(by = 'Fecha', axis = 0, inplace = True)
        #
        #total_dias = dt_2['Días entre visitas'].apply(lambda x: int(x) if x != ''  else 0).sum()
        total_dias = dt_2['Días entre visitas'].sum()
        #
        #total_gdp = dt_2['GPD (g)'].apply(lambda x: float(x) if x != '' else 0).sum()/dt_2.shape[0]
        total_gdp = round(dt_2['GPD (g)'].sum()/dt_2.shape[0], 2)
        dt_2['Crecimiento (cm)'] = dt_2['Alzada (cm)'].diff()
        del dt_2['Alzada (cm)']
        dt_2['Crecimiento (cm)'] = dt_2['Crecimiento (cm)'].fillna(0)

        dt_2 = dt_2.append({'Fecha': 'Total', 'Días entre visitas': total_dias,
                            'GPD (g)': total_gdp, 'Crecimiento (cm)': '-'}, ignore_index = True)
        dt_2['GPD (g)'] = dt_2['GPD (g)'].fillna(0)
        dt_2['Días entre visitas'] = dt_2['Días entre visitas'].fillna(0)

        dt_2 = dt_2.to_html(index = False)
        dt_2 = dt_2.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
        dt_2 = dt_2.replace('<td>', '<td style="text-align: center;">')


        dt3 = dt[['Fecha', 'Condicion Corporal', 'GPD (g)', 'Peso (Kg)']].copy()
        dt3.sort_values(by = 'Fecha', axis = 0, inplace = True)

        fig_1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig_1.add_trace(
            go.Bar(x = dt3['Fecha'], y = dt3['Condicion Corporal'], name = 'Condición corporal',
                text = dt3['Condicion Corporal'], textposition='auto',
                marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6),
            secondary_y=False)
        fig_1.add_trace(
            go.Scatter(x = dt3['Fecha'], y = dt3['Peso (Kg)'], name = 'Peso (Kg)',
                    text = dt3['Peso (Kg)'], textposition = 'top left',
                    marker = {'size': 15,
                                'color': 'rgb(255, 44, 44)'},
                    line = {'width': 3},
                    opacity = .7,
                    mode='lines+markers+text'),
                    secondary_y=True)

        fig_1.update_yaxes(title_text="Condición corporal", secondary_y=False)
        fig_1.update_yaxes(title_text="Peso (Kg)", secondary_y=True)
        fig_1.update_layout(xaxis = {'type': 'category'},
                                margin = dict(t = 35, b = 35, l = 35, r = 35),
                                legend=dict(orientation="h", xanchor = 'center', x = 1/2),
                                title_text="Condición Corporal y Peso",
                                height=600,
                                width = 800,
                                font = {'size': 16})

        pio.write_image(fig_1, dir_ + '/fig_1.png')
        #img_bytes = PlotlyImage.get(fig_1, format = 'png', scale = 1)
        #image = PILImage.open(io.BytesIO(img_bytes))
        #image.save(dir_ + '/fig_1.png')

        dt4 = dt[['Fecha', 'Alzada (cm)', 'Referencia Alzada (cm)', 'Raza']].copy()
        dt4.sort_values(by = 'Fecha', axis = 0, inplace = True)


        fig_2 = go.Figure(layout = go.Layout(margin = dict(t = 35, b = 35, l = 35, r = 35),
                                            title = dict(text = 'Alzada'),
                                            #yaxis_title = dict(text = 'Alzada (cm)'),
                                            xaxis = {'type': 'category'},
                                            legend=dict(orientation="h", xanchor = 'center', x = 1/2),
                                            height=600,
                                            width = 800,
                                            font = {'size': 16}))

        #legend=dict(orientation="h", xanchor = 'center', x = 1/2)))
        fig_2.add_trace(
            go.Scatter(x = dt4['Fecha'], y = dt4['Alzada (cm)'], name = 'Alzada (cm)',
                    text = dt4['Alzada (cm)'],
                    textposition = 'top left',
                    mode='lines+markers+text',
                    marker = {'size': 15},
                    line = {'width': 3},
                    opacity = .7),
                        )

        if dt4['Raza'].unique() == 'Criollo Colombiano':
            fig_2.add_trace(
                go.Scatter(x = dt4['Fecha'], y = dt4['Referencia Alzada (cm)'], name = 'Referencia Alzada (cm)',
                    text = dt4['Referencia Alzada (cm)'],
                    textposition = 'top left',
                    marker = {'size': 15},
                    mode='lines+markers+text',
                    line = {'width': 3},
                    opacity = .7)
                )
        pio.write_image(fig_2, dir_ + '/fig_2.png')
        #img_bytes = PlotlyImage.get(fig_2, format = 'png', scale = 1)
        #image = PILImage.open(io.BytesIO(img_bytes))
        #image.save(dir_ + '/fig_2.png')


        dt_3 = pd.DataFrame()
        dt_3['Observaciones Generales'] = [obs]
        dt_3 = dt_3.to_html(index = False)
        dt_3 = dt_3.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
        dt_3 = dt_3.replace('<td>', '<td style="text-align: center;">')

        dt_ps = data_ps.to_html(index = False)
        dt_ps = dt_ps.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
        dt_ps = dt_ps.replace('<td>', '<td style="text-align: center;">')

        dt_4 = pd.DataFrame()
        dt_4['Nombre Especialista'] = [persona]
        dt_4['Contacto'] = [contacto]
        dt_4 = dt_4.to_html(index = False)
        dt_4 = dt_4.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
        dt_4 = dt_4.replace('<td>', '<td style="text-align: center;">')

        env = Environment(loader = FileSystemLoader('Reporte'))

        template = env.get_template('Reporte.html')
        template_vars = {'Logo': 'file://' + dir_ + '/Brio.png',
                        'Tabla_1': dt_1,
                        'Tabla_2': dt_2,
                        'Fig_1': 'file://' + dir_ + '/fig_1.png',
                        'Fig_2': 'file://' + dir_ + '/fig_2.png',
                        'Tabla_3': dt_3,
                        'Tabla_ps': dt_ps,
                        'Tabla_4': dt_4}

        html_out = template.render(template_vars)

        try:
            HTML(string = html_out).write_pdf(os.path.join(dir_,'Reporte_' + dt['Nombre Equino'].unique()[0] + '.pdf'), stylesheets = ['Reporte/style.css'])
            return send_file(os.path.join(dir_,'Reporte_' + dt['Nombre Equino'].unique()[0] + '.pdf'))
        except Exception as e:
            print(e)
            return no_update

def entrenamiento_pdf(datos_equino, estado_equino, entrenamiento, data_rhemo, otros, image_ = ''):
    path_image = os.getcwd()
    with tempfile.TemporaryDirectory() as dir_:
        try:
            equino = pd.DataFrame(datos_equino, index = [0])
            estado = pd.DataFrame(estado_equino, index = [0])
            entrenamiento_ = pd.DataFrame(entrenamiento)
            entrenamiento_['Tiempo (minutos)'] = entrenamiento_['Tiempo (minutos)'][0:].apply(lambda x: int(x) if x != '' else 0)
            total_freq = entrenamiento_['Frecuencia por semana'][1:].apply(lambda x: int(x) if x != '' else 0).sum()
            total_tiempo = entrenamiento_['Tiempo (minutos)'][1:].sum()

            entrenamiento_ = entrenamiento_.append({'Realiza': '-',
                                                    'Frecuencia por semana': total_freq,
                                                    'Tiempo (minutos)': total_tiempo},
                                                    ignore_index = True)
            entrenamiento_.index = ['Calentamiento', 'Piscina', 'Piso Duro', 'Torno', 'Campo', 'Total']
            dt_rhemo = pd.DataFrame(data_rhemo, index = [0])
            otros = pd.DataFrame(otros, index = [0])
            esp = otros['Observaciones'][0]
            del otros['Observaciones']

            shutil.copy('Reporte/Brio.png', dir_ + '/Brio.png')
            try:
                shutil.copy('Reportes/'+image_, dir_ + '/' + image_)
                os.remove(os.path.join(path_image, 'Reportes', image_))
            except Exception as e:
                print(e)
            

            equino_h = equino.to_html(index = False)
            equino_h = equino_h.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
            equino_h = equino_h.replace('<td>', '<td style="text-align: center;">')
            equino_h = equino_h.replace('<th>', '<th style="text-align: center;">')


            estado_h = estado.to_html(index = False)
            estado_h= estado_h.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
            estado_h = estado_h.replace('<td>', '<td style="text-align: center;">')
            estado_h = estado_h.replace('<th>', '<th style="text-align: center;">')

            x = entrenamiento_.T
            entrenamiento_h = x.to_html()
            entrenamiento_h = entrenamiento_h.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
            entrenamiento_h = entrenamiento_h.replace('<td>', '<td style="text-align: center;">')
            entrenamiento_h = entrenamiento_h.replace('<th>', '<th style="text-align: center;">')

            dt_rhemo_h = dt_rhemo.to_html(index = False)
            dt_rhemo_h = dt_rhemo_h.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
            dt_rhemo_h = dt_rhemo_h.replace('<td>', '<td style="text-align: center;">')
            dt_rhemo_h = dt_rhemo_h.replace('<th>', '<th style="text-align: center;">')

            otros_h = otros.to_html(index = False)
            otros_h = otros_h.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
            otros_h = otros_h.replace('<td>', '<td style="text-align: center;">')
            otros_h = otros_h.replace('<th>', '<th style="text-align: center;">')

            recomendacion = pd.DataFrame(columns = ['Item', 'Observación'])
            recomendacion = recomendacion.append({'Item': 'Frecuencia de Entrenamiento',
                                'Observación': 'Para lograr optimo desempeño en los animales de competecia los equinos deben entrenar entre 5-6 dias a la semana y combinar diferentes ejercicios. Siempre incluir al menos 1 dia de descanso.'},
                                ignore_index = True)

            if entrenamiento_['Realiza'][1] == 'Si':
                recomendacion = recomendacion.append({'Item': 'Piscina',
                                    'Observación': 'Si va a utilizar la natacion como entrenamiento, evitar el entrenamiento en piso el mismo dia.'},
                                    ignore_index = True)

            if entrenamiento_['Tiempo (minutos)'][5] < 30:
                recomendacion = recomendacion.append({'Item': 'Duración Entrenamiento',
                                    'Observación': 'Es importante que el caballo consuma agua fresca antes durante y despues del entrenamiento o la actividad física y acceso a BRIO SALES a disposicion para mantener el balance de electrolitos'},
                                    ignore_index = True)

            if entrenamiento_['Tiempo (minutos)'][5] > 30:
                recomendacion = recomendacion.append({'Item': 'Duración Entrenamiento',
                                    'Observación': 'Es importante que el caballo consuma agua fresca antes durante y despues del entrenamiento o la actividad física y aceeso a BRIO SALES a disposicion y es recomendable suplementar con BRIO EQBALANCE para reponer las perdidas electroliticas por el entrenamiento.'},
                                    ignore_index = True)
            if entrenamiento_['Tiempo (minutos)'][0] < 10 or entrenamiento['Realiza'][0] == 'No':
                recomendacion = recomendacion.append({'Item': 'Calentamiento',
                                    'Observación': 'Un buen entrenamiento comprende de 10-15 min de calentamiento, que se puede realizar estirando o simplemente caminando al ejemplar. Si se requiere fortalecer tendones se recomienda realizar el calentamiento cuesta abajo.'},
                                    ignore_index = True)

            recomendacion = recomendacion.append({'Item': 'Consumo de Agua',
                                'Observación': 'Consumo Promedio de consumo de agua al dia referencia 450Kg de peso y temperatura (15-21°C) Evans J, 2002. En descanso 17-23 litros. Trabajo Media 41-63 litros. Trabajo Pesado 53-63.'},
                                ignore_index = True)
            if otros['Consumo Sal a Voluntad'][0] == 'No':
                recomendacion = recomendacion.append({'Item': 'Consumo de Sal',
                                    'Observación': 'La oferta de BRIO SALES debe ser a voluntad para que el caballo regule sus necesidades de macro y micro elementos, se debe ofrecer en saladeros protegidos del viento y el agua.'},
                                    ignore_index = True)

            if otros['Índice de Recuperación Cardiaca'][0] <= 50:
                recomendacion = recomendacion.append({'Item': 'Índice de Recuperación Cardiaca',
                                    'Observación': 'Este valor se refiere a la proporcion en la cual el corazon pudo recuperarse durante 1 minuto de descanso. Si es menor al 50% se debe dar al caballo mas tiempo de descanso entre las etapas de ejercicio. La intencion con el entrenamiento deportivo es que este indice cada vez sea mas alto.'},
                                    ignore_index = True)

            if otros['Índice de Recuperación Cardiaca'][0] > 50:
                recomendacion = recomendacion.append({'Item': 'Índice de Recuperación Cardiaca',
                                    'Observación': 'Este valor se refiere a la proporcion en la cual el corazon pudo recuperarse durante 1 minuto de descanso, el valor ideal es 50 o mayor, indica un buen protocolo de entrenamiento La intencion con el entrenamiento deportivo es que este indice cada vez sea mas alto.'},
                                    ignore_index = True)
            recomendacion = recomendacion.append({'Item': 'Observaciones especialista',
                                                'Observación': esp},
                                                ignore_index = True)

            recomendacion_h = recomendacion.to_html(index = False)
            recomendacion_h = recomendacion_h.replace('class="dataframe"', 'class="dataframe" style = "margin-left: auto; margin-right: auto"')
            recomendacion_h = recomendacion_h.replace('<td>', '<td style="text-align: center;">')
            recomendacion_h = recomendacion_h.replace('<th>', '<th style="text-align: center;">')

            env = Environment(loader = FileSystemLoader('Reporte'))

            template = env.get_template('Reporte_entrenamiento.html')
            template_vars = {'Logo': 'file://' + dir_ + '/Brio.png',
                            'Tabla_1': equino_h,
                            'Tabla_2': estado_h,
                            'Tabla_3': entrenamiento_h,
                            'Tabla_4': dt_rhemo_h,
                            'Tabla_5': otros_h,
                            'Tabla_6': recomendacion_h,
                            'Imagen': 'file://' + dir_ + '/' + image_}

            html_out = template.render(template_vars)

            HTML(string = html_out).write_pdf(os.path.join(dir_,'Reporte_entrenamiento_' + str(datos_equino['Nombre']) + '.pdf'), stylesheets = ['Reporte/style.css'])
            return send_file(os.path.join(dir_,'Reporte_entrenamiento_' + str(datos_equino['Nombre']) + '.pdf'))
        except Exception as e:
            print(e) 
            return no_update