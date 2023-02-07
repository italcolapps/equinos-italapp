import pandas as pd
from datetime import date
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def salidas(dt, criadero, equino, etapa, especialista = '', contacto = '', obs = '', tipo = '', pais = ''):

    if tipo == 'tabla_1':
        tbl_1 = go.Figure(data = [go.Table(
                header = dict(values = ['Fecha', 'Criadero', 'Equino', 'Etapa', 'Sexo', 'Raza'],
                              align = 'center'),
                cells = dict(values = [[date.today()],
                                       [criadero], [equino], [etapa], [dt['Sexo'].unique()], [dt['Raza'].unique()]],
                             align = 'center',
                             height=35))
                                      ],
                layout = go.Layout(margin = dict(t = 0, b = 0, l = 0, r = 0),
                                   height = 60)
                            )
        return tbl_1

    if tipo == 'tabla_2':
        dt2 = dt[['Fecha', 'Días entre visitas', 'GPD (g)', 'Alzada (cm)']].copy()
        dt2.sort_values(by = 'Fecha', axis = 0, inplace = True)
        #total_dias = dt2['Días entre visitas'].apply(lambda x: int(x) if x != '' else 0).sum()
        total_dias = dt2['Días entre visitas'].sum()
        #total_gdp = dt2['GPD (g)'].apply(lambda x: float(x) if x != '' else 0).sum()
        total_gdp = round(dt2['GPD (g)'].sum()/dt2.shape[0], 2)
        dt2['Crecimiento (cm)'] = dt2['Alzada (cm)'].diff()
        del dt2['Alzada (cm)']
        dt2['Crecimiento (cm)'] = dt2['Crecimiento (cm)'].fillna(0)
        dt2['GPD (g)'] = dt2['GPD (g)'].fillna(0)
        dt2['Días entre visitas'] = dt2['Días entre visitas'].fillna(0)
        dt2 = dt2.append({'Fecha': 'Total', 'Días entre visitas': total_dias,
                    'GPD (g)': total_gdp, 'Crecimiento (cm)': '-'}, ignore_index = True)
        tbl_2 = go.Figure(data = [go.Table(
                header = dict(values = ['Fecha de visita', 'Días entre visita', 'Ganancia diaria de peso (g)', 'Crecimiento (cm)'],
                              align = 'center'),
                cells = dict(values = [dt2['Fecha'],
                                       dt2['Días entre visitas'],
                                       dt2['GPD (g)'],
                                       dt2['Crecimiento (cm)']],
                             align = 'center',
                             height=25))
                                      ],
                #layout = go.Layout(margin = dict(t = 20, b = 20, l = 20, r = 20),
                 #                  height = 100 + 20 * dt2.shape[0])
                layout = go.Layout(margin = dict(t = 0, b = 0, l = 0, r = 0),
                                   height = 60 + 25 * dt2.shape[0])
                            )
        return tbl_2

    if tipo == 'fig_1':
        dt3 = dt[['Fecha', 'Condicion Corporal', 'GPD (g)', 'Peso (Kg)']].copy()
        dt3.sort_values(by = 'Fecha', axis = 0, inplace = True)

        fig_1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig_1.add_trace(
            go.Bar(x = dt3['Fecha'], y = dt3['Condicion Corporal'], name = 'Condición corporal',
                   text = dt3['Condicion Corporal'], textposition='auto',
                   marker_color = 'rgb(84, 105, 200)', width = 0.6, opacity = 0.6),
            secondary_y=False)
        fig_1.add_trace(
            go.Scatter(x = dt3['Fecha'], y = dt3['Peso (Kg)'], name = 'Peso (Kg)',
                       text = dt3['Peso (Kg)'], textposition = 'top left',
                       marker_color = 'rgb(247, 121, 16)',
                       mode='lines+markers+text'),
            secondary_y=True)

        fig_1.update_yaxes(title_text="Condición corporal", secondary_y=False)
        fig_1.update_yaxes(title_text="Peso (Kg)", secondary_y=True)
        #fig_1.update_layout(
         #   title_text="Peso y condición corporal")
        fig_1.update_layout(xaxis = {'type': 'category'},
                            margin = dict(t = 20, b = 20, l = 20, r = 20),
                            legend=dict(orientation="v"))
        #legend=dict(orientation="h", xanchor = 'center', x = 1/2))

        return fig_1

    if tipo == 'fig_2':
        dt4 = dt[['Fecha', 'Alzada (cm)', 'Referencia Alzada (cm)', 'Raza']].copy()
        dt4.sort_values(by = 'Fecha', axis = 0, inplace = True)


        fig_2 = go.Figure(layout = go.Layout(margin = dict(t = 25, b = 25, l = 25, r = 25),
                                             title = dict(text = 'Alzada'),
                                             #yaxis_title = dict(text = 'Alzada (cm)'),
                                             xaxis = {'type': 'category'},
                                             legend=dict(orientation="v")))
                                             #legend=dict(orientation="h", xanchor = 'center', x = 1/2)))
        fig_2.add_trace(
            go.Scatter(x = dt4['Fecha'], y = dt4['Alzada (cm)'], name = 'Alzada (cm)',
                       text = dt4['Alzada (cm)'],
                       textposition = 'top left',
                       mode='lines+markers+text'))

        if dt4['Raza'].unique() == 'Criollo Colombiano':
            fig_2.add_trace(
                go.Scatter(x = dt4['Fecha'], y = dt4['Referencia Alzada (cm)'], name = 'Referencia Alzada (cm)',
                       text = dt4['Referencia Alzada (cm)'],
                       textposition = 'top left',
                       mode='lines+markers+text'))
        #fig_1.update_yaxes(title_text="<b>Condición corporal</b>", secondary_y=False)
        #fig_1.update_yaxes(title_text="<b>Ganancia de peso diaria (g)</b>", secondary_y=True)

        return fig_2

    if tipo == 'tabla_4':
        tbl_4 = go.Figure(data = [go.Table(
                header = dict(values = ['Nombre', 'Celular/Correo'],
                              align = 'center'),
                cells = dict(values = [[especialista], [contacto],],
                             align = 'center',
                             height=35))
                                      ],
                layout = go.Layout(margin = dict(t = 0, b = 0, l = 0, r = 0),
                                   height = 100)
                            )
        return tbl_4

    if tipo == 'tabla_3':
        tbl_3 = go.Figure(data = [go.Table(
                header = dict(values = ['Observaciones Generales'],
                              align = 'center'),
                cells = dict(values = [[obs]],
                             align = 'center',
                             height=35))
                                      ],
                layout = go.Layout(margin = dict(t = 0, b = 0, l = 0, r = 0),
                                   height = 120)
                            )
        return tbl_3
