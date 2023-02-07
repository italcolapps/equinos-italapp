# package imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
import dash_table
from flask import session, copy_current_request_context
from datetime import datetime
import pandas as pd
from time import sleep
import os
import base64
from dash_extensions import Download
from dateutil import relativedelta as rdelta
from random import randint
from numpy import nan
# local imports
from auth import authenticate_user, validate_login_session
from server import app, server, port
from Datos.db import get_data, change_pw, crear_gerente, crear_usuario, add_row_entrenamiento
from Datos.insert_dataframe import insert_dataframe
from logo import logo_encoded
from Tablas import dashtable, render_table
from utils import *
from campos import *
from report import pdf_report, entrenamiento_pdf
from salidas import salidas

# local variables
labelstyle = {'color': 'white', 'background': '#E8850E', 'border-color': 'white'}
activelabelstyle = {'color': 'white', 'background': '#464443', 'border-color': '#E8850E', 'border-width': '2px'}


# login layout content
def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url',pathname='/login',refresh=False),
            dbc.Container([
                html.Br(),
                html.Center(
                    dbc.Row(
                        dbc.Col([
                            html.Img(src='data:image/png;base64,{}'.format(logo_encoded.decode()),
                                    style={'max-width': '100%', 'height': 'auto'})
                        ], xl=12, lg=12, md=12, sm=12, xs=12)
                )),
                dbc.Row(
                    dbc.Col([
                        html.Br(),
                        dbc.Card([
                            html.Center(
                                html.H5('Seguimiento de alzadas y entrenamiento Equinos Brio',className='card-title'),),
                            dbc.Input(id='login-email',placeholder='Nombre de usuario'),
                            html.Br(),
                            dbc.Input(id='login-password',placeholder='Contraseña',type='password'),
                            html.Br(),
                            dbc.Button('Iniciar sesión',id='login-button',color='warning',block=True),
                            html.Br(),
                            dcc.Store(id = 'user_info', storage_type = 'session'),
                            dbc.Spinner(html.Div(id='login-alert'))
                            ], body=True
                            )
                        ], xl = 6, lg = 5, md = 8, sm = 10, xs = 10), justify='center'
                    )
                ]
            )
        ]
    )

# cuerpo de la app con ingreso exitoso
@validate_login_session
def app_layout():
    return \
        html.Div([
            dcc.Location(id='home-url',pathname='/home'),
            dbc.Container([
                dcc.ConfirmDialog(
                    id='confirm',
                    message='¿Enviar Información Ingresada?'),
                dcc.ConfirmDialog(
                    id='confirm_pw',
                    message='¿Desea cambiar la contraseña? Esta acción no se puede revertir.'),
                dcc.ConfirmDialog(
                    id='confirm_crear_gerente',
                    message='¿Desea crear un gerente nuevo?'),
                # dcc.ConfirmDialog(
                #     id='confirm_crear_cliente',
                #     message='¿Desea crear un cliente nuevo?'),
                # dcc.ConfirmDialog(
                #     id='confirm_crear_cliente_ng',
                #     message='¿Desea crear un cliente nuevo?'),                    
                # dcc.ConfirmDialog(
                #     id='confirm_crear_granja',
                #     message='¿Desea crear un criadero nuevo?'),
                dcc.ConfirmDialog(
                    id='confirm_crear_granja_no_cliente',
                    message='¿Desea crear un criadero nuevo?'),  
                dcc.ConfirmDialog(
                    id='confirm_p1',
                    message='¿Enviar Información Ingresada?'),
                dcc.ConfirmDialog(
                    id='confirm_p2',
                    message='¿Enviar Información Ingresada?'),                                    
        
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Center(
                        html.Img(src='data:image/png;base64,{}'.format(logo_encoded.decode()),
                                    style = {'max-width': '100%', 'height': 'auto'})                        
                    ),
                    ], xl = 12, lg = 12, md = 12, sm = 12, xs = 12,),
            ], align='center', no_gutters = True),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Salir',id='logout-button',color='danger',block=True,size='sm',
                                style = {'background': '#F59828', 'color': 'white', 'border-color': 'white'})
                    ], xl = 2, lg = 2, md = 4, sm = 4, xs = 4)                
            ], justify="end"),
            dcc.Store(id = 'user_info', storage_type = 'session'),
            html.Div(children = [dbc.Input(id = 'fake_input')], style = {'display': 'none'}),
            html.Br(),
            titulo(texto = '-', id_ = 'test'),

            dbc.Tabs(children = [
                dbc.Tab(label = 'Ingreso de información', id = 'ingreso_datos', tab_id = 'tab_ingreso_datos',
                        active_label_style = activelabelstyle, label_style = labelstyle),
                dbc.Tab(label = 'Entrenamiento deportivo', id = 'entrenamiento_deportivo', tab_id = 'tab_entrenamiento_deportivo',
                        active_label_style = activelabelstyle, label_style = labelstyle),
                dbc.Tab(label = 'Consultar información', id = 'consultar_informacion', tab_id = 'tab_consultar_informacion',
                        active_label_style = activelabelstyle, label_style = labelstyle),
                dbc.Tab(label = 'Gerentes', id = 'gerentes_zona', tab_id = 'tab_gerentes_zona',
                        active_label_style = activelabelstyle, label_style = labelstyle),
                dbc.Tab(label = 'Criaderos', id = 'administrar_granjas', tab_id = 'tab_administrar_granjas',
                        active_label_style = activelabelstyle, label_style = labelstyle),
                dbc.Tab(label = 'Configuración', id = 'configuracion', tab_id = 'tab_configuracion',
                        active_label_style = activelabelstyle, label_style = labelstyle)
                ], id = 'tabs'),
            html.Div(id = 'contenido')
            ],

            )
        ]
    )


# main app layout
app.layout = html.Div(
    [
        dcc.Location(id='url',refresh=False),
        html.Div(
            login_layout(),
            id='page-content'
        ),
    ]
)


###############################################################################
# utilities
###############################################################################
# router
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def router(url):
    if url=='/home':
        return app_layout()
    elif url=='/login':
        return login_layout()
    else:
        return login_layout()

# authenticate
@app.callback(
    [Output('url','pathname'),
     Output('login-alert','children'),
     Output('user_info', 'data')],
    [Input('login-button','n_clicks')],
    [State('login-email','value'),
     State('login-password','value')])
def login_auth(n_clicks,email,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update,no_update, no_update
    credentials = {'user':email,"password":pw}
    user = authenticate_user(credentials)
    if user[0]:
        session['authed'] = True
        usuario = user[1].to_json(date_format = 'iso', orient = 'split')
        return ['/home','', usuario]
    session['authed'] = False
    return [no_update, dbc.Alert('Usuario o contraseña incorrectas.',color='danger',dismissable=True), no_update]

@app.callback(
    Output('home-url','pathname'),
    [Input('logout-button','n_clicks')],
    State('user_info', 'data'))
def logout_(n_clicks, data):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        raise dash.exceptions.PreventUpdate()
        return no_update, no_update
    session['authed'] = False
    return '/login', None

###############################################################################
# callbacks
###############################################################################
## confirm p1
# @app.callback([Output('confirm', 'displayed')],
#               [Input('enviar_p1', 'n_clicks')])
# def display_confirm(value):
#     if value:
#         return [True]
#     else:
#         return [False]

## confirm cambio_pw
@app.callback([Output('confirm_pw', 'displayed')],
              [Input('cambiar_pw', 'n_clicks')])
def display_confirm(value):
    if value:
        return [True]
    else:
        return [False]

## confirm crear_gerente
@app.callback([Output('confirm_crear_gerente', 'displayed')],
              [Input('crear_gerente', 'n_clicks')])
def display_confirm(value):
    if value:
        return [True]
    else:
        return [False]

# ## confirm crear_criadero
# @app.callback([Output('confirm_crear_granja', 'displayed')],
#               [Input('crear_granja', 'n_clicks')])
# def display_confirm(value):
#     if value:
#         return [True]
#     else:
#         return [False]

## confirm crear_granja no cliente
@app.callback([Output('confirm_crear_granja_no_cliente', 'displayed')],
              [Input('crear_granja_no_cliente', 'n_clicks')])
def display_confirm(value):
    if value:
        return [True]
    else:
        return [False]



# confirm enviar seguimiento de alzadas
@app.callback(Output('confirm_p1', 'displayed'),
              Input('enviar_p1', 'n_clicks'))
def display_confirm(value):
    # global enviar
    if value:
        # enviar = True
        return True
    else:
        # enviar = False
        return False

## confirm enviar entrenamiento deportivo
@app.callback([Output('confirm_p2', 'displayed')],
              [Input('enviar_p2', 'n_clicks')])
def display_confirm(value):
    #global enviar
    if value:
        #enviar = True
        return [True]
    else:
       # enviar = False
        return [False]

### callback inicial en funcion del rol del usuario
@app.callback([Output('test', 'children'),
               Output('ingreso_datos', 'disabled'),
               Output('ingreso_datos', 'tab_style')],
              Input('fake_input', 'value'),
              State('user_info', 'data'))
def nombre(n, data):
    usuario = pd.read_json(data, orient = 'split')
    if usuario['rol_usuario'].values[0] == 'administrador':
        return [f'Bienvenido {usuario["nombre"].values[0]}',
                False, no_update] #{'display': 'none'}
    elif usuario['rol_usuario'].values[0] == 'cliente':
        return [f'Bienvenido criadero {usuario["nombre"].values[0]}',
                False, no_update] #{'display': 'none'}
    else:
        return [f'Bienvenido {usuario["nombre"].values[0]}',
        no_update, no_update]

### ocultar pestaña gerentes
@app.callback([Output('gerentes_zona', 'disabled'),
               Output('gerentes_zona', 'tab_style')],
              Input('fake_input', 'value'),
              State('user_info', 'data'))
def gerenteszona(value, data):
    usuario = pd.read_json(data, orient = 'split')
    if usuario['rol_usuario'].values[0] in ['gerente', 'cliente']:
        return [True, {'display': 'none'}]
    return [no_update, no_update]

## ocultar pestaña criaderos
@app.callback([Output('administrar_granjas', 'disabled'),
               Output('administrar_granjas', 'tab_style')],
              Input('fake_input', 'value'),
              State('user_info', 'data'))
def gerenteszona(value, data):
    usuario = pd.read_json(data, orient = 'split')
    if usuario['rol_usuario'].values[0] in ['cliente']:
        return [True, {'display': 'none'}]
    return [no_update, no_update]   

# callback pestaña inicial
@app.callback(Output('tabs', 'active_tab'),
              Input('fake_input', 'value'),
              State('user_info', 'data'))
def active_tab(value, data):
    usuario = pd.read_json(data, orient = 'split')
    if usuario['rol_usuario'].values[0] == 'administrador':
        return 'tab_gerentes_zona' 
    elif usuario['rol_usuario'].values[0] == 'gerente':
        return 'tab_ingreso_datos'
    elif usuario['rol_usuario'].values[0] == 'cliente':
        return 'tab_ingreso_datos'
    else:
        return no_update

### calback contenido cambio de pestaña 
@app.callback(Output('contenido', 'children'),
              Input('tabs', 'active_tab'),
              State('user_info', 'data'))
def contenido(active_tab, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if active_tab == 'tab_ingreso_datos':
        if rol == 'administrador':
            gerentes = get_data('SELECT doc_id, nombre_gerente FROM gerentes')
            gerentes.sort_values(by = ['nombre_gerente'], inplace = True)
            gerentes.reset_index(inplace = True, drop = True)
            criaderos = pd.DataFrame({'id_criadero': ['-'],
                                      'nombre_criadero': ['-']})
            style_gerente = {'display': 'inline'}
            style_criadero = {'display': 'inline'}
        if rol == 'gerente':
            gerentes = pd.DataFrame({'doc_id': [doc_id],
                                     'nombre_gerente': [user]})
            criaderos = get_data(f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {doc_id}')
            if criaderos.empty:
                criaderos = pd.DataFrame({'id_criadero': [None],
                                          'nombre_criadero': ['Sin registros']})
            else:
                criaderos.drop_duplicates(inplace=True)
                criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
                criaderos.reset_index(inplace = True, drop = True)                
            style_gerente = {'display': 'none'}
            style_criadero = {'display': 'inline'}
        if rol == 'cliente':
            gerentes = pd.DataFrame({'doc_id': ['-'],
                                     'nombre_gerente': ['-']})
            criaderos = pd.DataFrame({'id_criadero': [doc_id],
                                      'nombre_criadero': [user]})
            style_gerente = {'display': 'none'}
            style_criadero = {'display': 'none'}   
        return [
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5('Calculadora de tiempo')
                ], xl = 5, lg = 5, md = 6, sm = 10, xs = 10)
            ], no_gutters = False),
            dbc.Row([
                fecha_actual_p1, fecha_u_v_p1, fecha_nac_p1,
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label('Calcular edad y días'),
                        dbc.Button('Calcular', color = 'warning', id = 'calc_p1', block = True),
                        dbc.FormText('-')
                    ], style = {'padding-left': '5px'})
                ], xl = 2, lg = 2, md = 3, sm = 5, xs = 5)
            ], no_gutters = False),
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'edad_p1_1_sal', children = [
                            dbc.FormGroup(
                                [
                                dbc.Label('Edad'),
                                dbc.Input(id = 'edad_p1_1',
                                            type = 'number',
                                            debounce = True),
                                dbc.FormText('Meses')
                                ], style = {'padding-left': '5px'})
                    ])
                ], xl = 2, lg = 2, md = 4, sm = 4, xs = 4),
                dbc.Col([
                    html.Div(id = 'dias_p1_1_sal', children = [
                            dbc.FormGroup(
                                [
                                dbc.Label('Días'),
                                dbc.Input(id = 'dias_p1_1',
                                            type = 'number',
                                            debounce = True),
                                dbc.FormText('Entre visita')
                                ], style = {'padding-left': '5px'})
                    ])
                ], xl = 2, lg = 2, md = 4, sm = 4, xs = 4),
            ], no_gutters = False),
            dbc.Row([
                dbc.Col([
                    html.H5('Formato de ingreso')
                ], xl = 5, lg = 5, md = 6, sm = 10, xs = 10)
            ], no_gutters = False),
            dbc.Row([
                campos(id_ = 'gerente_p1', label = 'Gerente de zona', ayuda = '-',tipo = 'seleccion',
                       valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])], 
                       style_col = style_gerente, xl = 4, lg = 4, md = 6, sm = 10, xs = 10)
                #pais_p1, depto_p1, mun_p1
            ], no_gutters = False),
            dbc.Row([
                campos(id_ = 'criadero_p1', label = 'Criadero', ayuda = '-',tipo = 'seleccion',
                       valor = [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])], 
                       style_col = style_criadero, xl = 3, lg = 3, md = 6, sm = 8, xs = 8),
                nuevo_e_p1, nombre_p1, mun_p1, raza_p1, planta_p1,
                #criadero_p1, nombre_p1, raza_p1, planta_p1,
                ref_p1
            ], no_gutters = False),
            dbc.Row([
                etapa_p1, sexo_p1, peso_p1, peso_a_p1,
            ], no_gutters = False),
            dbc.Row([
                alzada_p1, condicion_p1, calidad_p1,
                dbc.Col(id = 'andar_p1_col', children = [
                    html.Div(id = 'andar_p1_sal', children = [
                            dbc.FormGroup(
                                [
                                dbc.Label('Andar'),
                                dbc.Select(id = 'andar_p1',
                                            options = [{'label': i, 'value': i} for i in ['P1 Trote y Galape',
                                                                                            'P2 Trocha y Galope',
                                                                                            'P3 Trocha Pura',
                                                                                            'P4 Paso Fino']]),
                                dbc.FormText('-')
                                ], style = {'padding-left': '5px'})
                    ])
                ], xl = 2, lg = 2, md = 4, sm = 5, xs = 5),
                obs_p1
            ], no_gutters = False),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5('Plan sanitario')
                ])
            ], no_gutters = False),
            dbc.Row([
                influenza_t, fecha_influenza_t, prx_influenza_t
            ]),
            dbc.Row([
                obs_influenza_t
            ]),            
            html.Hr(),
            dbc.Row([
                tetano, fecha_tetano, prx_tetano
            ]),
            dbc.Row([
                obs_tetano
            ]),
            html.Hr(),
            dbc.Row([
                encefalitis, fecha_encefalitis, prx_encefalitis
            ]),
            dbc.Row([
                obs_encefalitis
            ]),
            html.Hr(),
            dbc.Row([
                desparasitacion, fecha_desparasitacion, prx_desparasitacion
            ]),
            dbc.Row([
                obs_desparasitacion
            ]),            
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Validar información', color = 'warning', id = 'validar_p1', block = True)
                ], xl = 3, lg = 3, md = 5, sm = 6, xs = 6, style = {'padding-top': '5px'}),
                dbc.Col([
                dbc.Spinner(dbc.Alert(id = 'salida_val_p1', is_open = False, duration = 4000))
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})
            ], no_gutters = False, align = 'center'),
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader('Resumen Seguimiento Alzadas'),
                    dbc.ModalBody(id = 'modal_sa_c', children = [
                        html.Div(id = 'div_validacion_ss'),
                        html.Br(),
                        html.Div(id = 'div_validacion_plan', style = {'overflow': 'auto', 'white-space': 'nowrap'}),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button('Enviar seguimiento alzadas', id = 'enviar_p1', color = 'success')
                            ], xl = 4, lg = 4, md = 5, sm = 6, xs = 6),
                            dbc.Col([
                                dbc.Spinner(dbc.Alert(id = 'salida_p1', dismissable=True, is_open = False))
                            ], xl = 8, lg = 8, md = 8, sm = 8, xs = 8)
                        ])                        
                    ]),
                ], id = 'modal_sa', scrollable = True, is_open = False, size = 'lg'),
            ]),
            dcc.Store(id = 'val_sa_data'),
            dcc.Store(id = 'val_plan_data'),
            html.Br(),
            html.Br()          
        ]
 
    if active_tab == 'tab_entrenamiento_deportivo':
        return [
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5('Datos de ingreso')
                ], xl = 5, lg = 5, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Row([
                criadero_p2, nombre_p2, raza_p2, edad_p2,
                peso_p2, condicion_p2, calidad_p2, alzada_p2, etapa_p2,
                ref_p2
            ], no_gutters = False),
            dbc.Row([
                dbc.Col([
                    html.H5('Entrenamiento')
                ], xl = 5, lg = 5, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Row([
                piscina_p2, freq_ps, tiempo_ps
            ], no_gutters = False),
            dbc.Row([
                pisod_p2, freq_pd, tiempo_pd
            ], no_gutters = False),
            dbc.Row([
                torno_p2, freq_tr, tiempo_tr
            ], no_gutters = False),
            dbc.Row([
                campo_p2, freq_cp, tiempo_cp
            ], no_gutters = False),
            dbc.Row([
                calen_p2, tiempo_cl
            ], no_gutters = False),
            dbc.Row([
                dbc.Col([
                    html.H5('Datos italcol')
                ], xl = 5, lg = 5, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Row([
                fc_max_p2, fc_min_p2, fc_prom_p2, horain_p2,
                horafn_p2,
            ], no_gutters = False),
            dbc.Row([
                dbc.Col([
                    html.H5('Otros datos')
                ], xl = 5, lg = 5, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Row([
                grado_p2, agua_p2, consumo_p2, fc_fn_p2, fc_fn_1_p2, ind_rc_p2
            ], no_gutters = False),
            dbc.Row([
                obs_p2,
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label('-'),
                        dcc.Upload(id = 'upload_p2', children = [
                            dbc.Button('Imagen', color = 'warning', id = 'img_p2', block = True),
                        ]),
                        dbc.FormText('-')
                    ], style = {'padding-left': '10px'})
                ], xl = 3, lg = 3, md = 4, sm = 6, xs = 6)
            ], no_gutters = False),
            dcc.Store(id = 'imagen_rhemo', storage_type = 'session'),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Generar reporte', color = 'warning', id = 'enviar_p2', block = True)
                ], xl = 3, lg = 3, md = 5, sm = 6, xs = 6),
                # dbc.Col([
                #     dbc.Button('Descargar reporte', color = 'success', id = 'download_p2', block = True)
                # ], xl = 3, lg = 3, md = 5, sm = 6, xs = 6,
                # style = {'padding-left': '5px'}),
                dbc.Col([
                dbc.Spinner(dbc.Alert(id = 'salida_p2', is_open = False, duration = 4000))
                ], xl = 6, lg = 6, md = 8, sm = 10, xs = 10,
                style = {'padding-top': '0px', 'padding-left': '15px'})
            ], no_gutters = False),
            Download(id="download_p2_"),
            html.Br()

        ]
    
    if active_tab == 'tab_configuracion':
        return [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Cambio de contraseña', id = 'collapse_button_pw',
                                outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            html.Br(),
            dbc.Collapse(id = 'collapse_pw', children = [
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Contraseña actual'),
                            dbc.Input(id = 'old_pw', type = 'password', placeholder = '******'),
                            ]),
                     ], xl = 4, lg = 4, md = 5, sm = 10, xs = 10)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Contraseña nueva'),
                            dbc.Input(id = 'new_pw', type = 'password', placeholder = '******'),
                            dbc.FormText('Recuerde que debe contar con al menos 8 caracteres')
                        ]),
                    ], xl = 4, lg = 4, md = 5, sm = 10, xs = 10)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Cambiar', id = 'cambiar_pw', color = 'warning')
                    ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
                    dbc.Col([
                        dbc.Spinner(dbc.Alert(id = 'alert_pw', duration = 4000, is_open = False))
                    ], xl = 8, lg = 8, md = 8, sm = 8, xs = 8)
                ]),
            ]),
        ]

    if active_tab == 'tab_consultar_informacion':
        if rol == 'administrador':
            gerentes = get_data('SELECT doc_id, nombre_gerente FROM gerentes')
            gerentes.sort_values(by = ['nombre_gerente'], inplace = True)
            gerentes.reset_index(inplace = True, drop = True)
            criaderos = pd.DataFrame({'id_criadero': [None],
                                      'nombre_criadero': ['-']})
            equinos = pd.DataFrame({'id_equino': [None],
                                      'nombre_equino': ['-']})                                      
            style_gerente = {'display': 'inline'}
            style_criadero = {'display': 'inline'}
        if rol == 'gerente':
            gerentes = pd.DataFrame({'doc_id': [doc_id],
                                     'nombre_gerente': [user]})
            criaderos = get_data(f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {doc_id}')
            equinos = pd.DataFrame({'id_equino': [None],
                                      'nombre_equino': ['Sin registros']})              
            if criaderos.empty:
                criaderos = pd.DataFrame({'id_criadero': [None],
                                          'nombre_criadero': ['Sin registros']})
            else:
                criaderos.drop_duplicates(inplace=True)
                criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
                criaderos.reset_index(inplace = True, drop = True)                
            style_gerente = {'display': 'none'}
            style_criadero = {'display': 'inline'}
        if rol == 'cliente':
            gerentes = pd.DataFrame({'doc_id': ['-'],
                                     'nombre_gerente': ['-']})
            criaderos = pd.DataFrame({'id_criadero': [doc_id],
                                      'nombre_criadero': [user]})
            equinos = get_data(f'SELECT DISTINCT id_equino, nombre_equino FROM equinos WHERE id_criadero = {doc_id}')
            if equinos.empty:
                equinos = pd.DataFrame({'id_equino': [None],
                                        'nombre_equino': ['Sin registros']}) 
            else:
                equinos.drop_duplicates(inplace=True)
                equinos.sort_values(by = ['nombre_equino'], inplace = True)
                equinos.reset_index(inplace = True, drop = True) 
            style_gerente = {'display': 'none'}
            style_criadero = {'display': 'inline'}

        return [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Reporte Seguimiento de Alzadas', id = 'collapse_button_reporte_sa',
                                outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_reporte_sa', children = [
                html.Br(),
                dbc.Row([
                    campos(id_ = 'gerente_p3_ra', label = 'Gerente de zona', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])], 
                        style_col = style_gerente, xl = 4, lg = 4, md = 6, sm = 10, xs = 10),
                    campos(id_ = 'criadero_p3_ra', label = 'Criadero', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])], 
                        style_col = style_criadero, xl = 3, lg = 3, md = 6, sm = 8, xs = 8,
                        vl = user if rol == 'cliente' else None),
                    campos(id_ = 'equino_p3_ra', label = 'Equino', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])], 
                        xl = 4, lg = 4, md = 6, sm = 10, xs = 10),
                ]),
                dbc.Row([
                    especialista_ra, contacto_ra, observaciones_ra
                ]),
            dcc.Store(id = 'info_ra', storage_type = 'session'),
            dcc.Store(id = 'info_ps_', storage_type = 'session'),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Generar reporte', color = 'warning', id = 'generar_p3_ra', block = True)
                ], xl = 2, lg = 2, md = 4, sm = 5, xs = 5, style = {'padding-top': '5px'}),
                dbc.Col([
                dbc.Spinner(dbc.Alert(id = 'salida_p3_ra', is_open = False, duration = 4000))
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})
            ], no_gutters = False, align = 'center'),
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader('Reporte Seguimiento Alzadas'),
                    dbc.ModalBody(id = 'modal_ra_c', children = [
                        form_sal,
                        dbc.Row([
                            dbc.Col([
                                dbc.Button('Descargar reporte', color = 'success', id = 'descargar_p3_ra', block = True)
                            ], xl = 4, lg = 4, md = 6, sm = 10, xs = 10, style = {'padding-top': '5px'}),
                            dbc.Col([
                                dbc.Spinner(dbc.Alert(id = 'download_p3_ra', is_open = False, duration = 4000))
                            ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})                            
                        ])
                    ]),
                ], id = 'modal_ra', scrollable = True, is_open = False, size = 'lg'),
                ]),
            Download(id="download_p4_"),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Historico alzadas', id = 'collapse_button_historicos',
                                outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_reporte_historicos', children = [
                html.Br(),
                dbc.Row([
                    campos(id_ = 'gerente_p3_ha', label = 'Gerente de zona', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])], 
                        style_col = style_gerente, xl = 4, lg = 4, md = 6, sm = 10, xs = 10),
                    campos(id_ = 'criadero_p3_ha', label = 'Criadero', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])], 
                        style_col = style_criadero, xl = 3, lg = 3, md = 6, sm = 8, xs = 8,
                        vl = user if rol == 'cliente' else None),
                    campos(id_ = 'año_p3_ha', label = 'Año', tipo = 'seleccion_m', ayuda = '-', 
                           valor = [{'label': 'Sin registros', 'value': '-'}]),
                    campos(id_ = 'mes_p3_ha', label = 'Mes', tipo = 'seleccion_m', ayuda = '-',
                           valor = [{'label': 'Sin registros', 'value': '-'}])
                ]),
            dcc.Store(id = 'info_ha', storage_type = 'session'),
            dcc.Store(id = 'año_mes_ha', storage_type = 'session'),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Generar reporte', color = 'warning', id = 'generar_p3_ha', block = True)
                ], xl = 2, lg = 2, md = 4, sm = 5, xs = 5, style = {'padding-top': '5px'}),
                dbc.Col([
                dbc.Spinner(dbc.Alert(id = 'salida_p3_ha', is_open = False, duration = 4000))
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})
            ], no_gutters = False, align = 'center'),
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader('Datos Seguimiento Alzadas'),
                    dbc.ModalBody(id = 'modal_ha_c', children = [
                        html.Div(id = 'tabla_ha', style = {'overflow': 'auto', 'white-space': 'nowrap',}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button('Descargar reporte', color = 'success', id = 'descargar_p3_ha', block = True)
                            ], xl = 4, lg = 4, md = 6, sm = 10, xs = 10, style = {'padding-top': '5px'}),
                            dbc.Col([
                                dbc.Spinner(dbc.Alert(id = 'download_p3_ha', is_open = False, duration = 4000))
                            ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})                            
                        ])
                    ]),
                ], id = 'modal_ha', scrollable = True, is_open = False, size = 'xl'),
            ]),
            Download(id="download_ha"),
            ]),         
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Mis equinos' if rol == 'cliente' else 'Equinos', id = 'collapse_button_equinos',
                                outline = True, color = 'dark') 
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_reporte_equinos', children = [
                html.Br(),
                dbc.Row([
                    campos(id_ = 'gerente_p3_eq', label = 'Gerente de zona', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])], 
                        style_col = style_gerente, xl = 4, lg = 4, md = 6, sm = 10, xs = 10),
                    campos(id_ = 'criadero_p3_eq', label = 'Criadero', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])], 
                        style_col = style_criadero, xl = 3, lg = 3, md = 6, sm = 8, xs = 8,
                        vl = user if rol == 'cliente' else None)
                ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Cargar', color = 'warning', id = 'generar_p3_eq', block = True)
                ], xl = 2, lg = 2, md = 4, sm = 5, xs = 5, style = {'padding-top': '5px'}),
                dbc.Col([
                dbc.Spinner(dbc.Alert(id = 'salida_p3_eq', is_open = False, duration = 4000))
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})
            ], no_gutters = False, align = 'center'),
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader('Equinos registrados en el criadero'),
                    dbc.ModalBody(id = 'modal_eq_c', children = []),
                ], id = 'modal_eq', scrollable = True, is_open = False, size = 'lg'),
                ]),                
            ]),



            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Plan sanitario', id = 'collapse_button_ps',
                                outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_ps', children = [
                html.Br(),
                dbc.Row([
                    campos(id_ = 'gerente_p3_ps', label = 'Gerente de zona', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])], 
                        style_col = style_gerente, xl = 4, lg = 4, md = 6, sm = 10, xs = 10),
                    campos(id_ = 'criadero_p3_ps', label = 'Criadero', ayuda = '-',tipo = 'seleccion',
                        valor = [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])], 
                        style_col = style_criadero, xl = 3, lg = 3, md = 6, sm = 8, xs = 8,
                        vl = user if rol == 'cliente' else None),
                ]),
            dcc.Store(id = 'info_ps', storage_type = 'session'),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Generar reporte', color = 'warning', id = 'generar_p3_ps', block = True)
                ], xl = 2, lg = 2, md = 4, sm = 5, xs = 5, style = {'padding-top': '5px'}),
                dbc.Col([
                dbc.Spinner(dbc.Alert(id = 'salida_p3_ps', is_open = False, duration = 4000))
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})
            ], no_gutters = False, align = 'center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Spinner(
                        dbc.Alert(id = 'alerta_ps', is_open = False, dismissable=True, color="light")
                    )
                ])
            ]),
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader('Datos plan sanitario'),
                    dbc.ModalBody(id = 'modal_ps_c', children = [
                        html.Div(id = 'tabla_ps', style = {'overflow': 'auto', 'white-space': 'nowrap',}),
                        # dbc.Row([
                        #     dbc.Col([
                        #         dbc.Button('Descargar reporte', color = 'success', id = 'descargar_p3_ps', block = True)
                        #     ], xl = 4, lg = 4, md = 6, sm = 10, xs = 10, style = {'padding-top': '5px'}),
                        #     dbc.Col([
                        #         dbc.Spinner(dbc.Alert(id = 'download_p3_ps', is_open = False, duration = 4000))
                        #     ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10, style = {'padding-left': '15px', 'padding-top': '15px'})
                        # ])
                    ]),
                ], id = 'modal_ps', scrollable = True, is_open = False, size = 'xl'),
            ]),
            Download(id="download_ps"),
            ]), 
            html.Br()                
        ]

    elif active_tab == 'tab_gerentes_zona':
        return [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Gerentes de zona', id = 'callapse_button_ver_gerentes',
                               outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_ver_gerentes', children = [
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.H5('Ver gerentes'),
                    ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
                    dbc.Col([
                        dbc.Button('Cargar', id = 'ver_gerentes', color = 'warning')
                    ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
                    dbc.Col([
                        dbc.Spinner(dbc.Alert(id = 'alert_ver_gerentes', duration = 4000, is_open = False))
                    ], xl = 8, lg = 8, md = 8, sm = 8, xs = 8),              
                ], align = 'center'),
                html.Div([
                    dbc.Modal([
                        dbc.ModalHeader('Gerentes de zona'),
                        dbc.ModalBody(id = 'modal_gerentes_c', children = []),
                    ], id = 'modal_gerentes', scrollable = True, is_open = False, size = 'xl'),
                ]),                
                html.Br()           
                            
            ]),

            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Crear Gerente', id = 'callapse_button_crear_gerente',
                               outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_crear_gerente', children = [
                html.Br(),
                dbc.Row([
                    documento_gerente
                ]),
                dbc.Row([
                    nombre_gerente, pais_gerente, zona_gerente
                ]),
                dbc.Row([
                    usuario_gerente, pw_gerente
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Crear gerente', id = 'crear_gerente', color = 'warning')
                    ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
                    dbc.Col([
                        dbc.Spinner(dbc.Alert(id = 'alert_crear_gerente', duration = 4000, is_open = False))
                    ], xl = 8, lg = 8, md = 8, sm = 8, xs = 8)
                ]),
                html.Br()                             
            ]),
            html.Br(),
        ]

    elif active_tab == 'tab_administrar_granjas' and rol != 'cliente':
        if rol == 'administrador':
            gerentes = get_data('SELECT nombre_gerente, doc_id  FROM gerentes')
            gerentes.sort_values(by = ['nombre_gerente'], inplace = True, axis = 0)
            gerentes.reset_index(drop = True, inplace = True)
        elif rol == 'gerente':
            gerentes = usuario[['nombre', 'doc_id']]
            gerentes['nombre'] = [gerentes['nombre'].values[0].upper()]
            gerentes.columns = ['nombre_gerente', 'doc_id']
            gerentes.reset_index(drop = True, inplace = True)
        else:
            gerentes = ['-']

        return [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Criaderos', id = 'callapse_button_mis_granjas',
                               outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_mis_granjas', children = [
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.H5('Ver criaderos')
                    ], xl = 2, lg = 2, md = 4, sm = 5, xs = 5),
                ]),
                dbc.Row([
                    campos(id_ = 'gerente_ver_granjas_nc', label = 'GERENTE DE ZONA', ayuda = '-', tipo = 'seleccion_m',
                      valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])],
                      xl = 4, lg = 5, md = 8, sm = 8, xs = 10),
                    # campos(id_ = 'nit_cliente_ver_granjas', label = 'NIT DEL CLIENTE', ayuda = '-', tipo = 'seleccion',
                    #  xl = 3, lg = 4, md = 6, sm = 6, xs = 6, valor = [{'label': '-', 'value': '-'}]),                    
                    # campos(id_ = 'nombre_clientes_ver_granjas', label = 'NOMBRE DEL CRIADERO', ayuda = '-', tipo = 'text',
                    #     xl = 3, lg = 4, md = 6, sm = 6, xs = 6),
                    dbc.Col([
                        dbc.Button('Cargar', id = 'cargar_mis_granjas_nc', color = 'warning')
                    ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
                    dbc.Col([
                        dbc.Spinner(dbc.Alert(id = 'alert_cargar_mis_granjas_nc', duration = 4000, is_open = False))
                    ], xl = 6, lg = 6, md = 6, sm = 8, xs = 8)                    
                ], align = 'center'),
                html.Div([
                    dbc.Modal([
                        dbc.ModalHeader('Criaderos'),
                        dbc.ModalBody(id = 'modal_criaderos_c', children = []),
                    ], id = 'modal_criaderos', scrollable = True, is_open = False, size = 'xl'),
                ]),                   
                #html.Br(),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Crear criadero', id = 'callapse_button_crear_granja',
                               outline = True, color = 'dark')
                ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            ]),
            dbc.Collapse(id = 'collapse_crear_granja', children = [
                html.Br(),
                dbc.Row([
                    campos(id_ = 'gerente_nc', label = 'GERENTE DE ZONA', ayuda = '-', tipo = 'seleccion',
                      valor = [{'label': gerentes['nombre_gerente'][i], 'value': gerentes['doc_id'][i]} for i in range(gerentes.shape[0])],
                      xl = 3, lg = 4, md = 6, sm = 6, xs = 6)                    
                ]),
                dbc.Row([
                    #nit_clientes_nc, 
                    nombre_clientes,
                    campos(id_ = 'depto_granja', label = 'DEPARTAMENTO/PROVINCIA', ayuda = '-', tipo = 'depto',
                           xl = 3, lg = 4, md = 6, sm = 12, xs = 12, pais = pais.title()),
                     municipio_granja
                    #campos(tipo = 'number', label = 'Número de granjas', ayuda = 'Ingrese el número de granjas a crear', id_ = 'numero_granjas_nc'),
                ]),
                dbc.Row([
                    usuario_cliente, pw_cliente
                ]),
                # dbc.Row([                    
                #     campos(tipo = 'boton', valor = 'Cargar tabla de ingreso', id_ = 'cargar_tabla_ingreso_granjas_nc',
                #            xl = 3, lg = 4, md = 5, sm = 5, xs = 6)
                # ]),
                # html.Br(),
                # dbc.Row([
                #     dbc.Col([
                #         html.Div(id = 'tabla_ingreso_granjas_nc', style = {'overflow': 'auto', 'white-space': 'nowrap'})
                #     ])
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Alert(id = 'tabla_ingreso_granjas_nc_sal', is_open = False, dismissable = True)
                #     ])
                # ]),
                # html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Crear criadero', id = 'crear_granja_no_cliente', color = 'warning')
                    ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
                    dbc.Col([
                        dbc.Spinner(dbc.Alert(id = 'alert_crear_granja_nc', duration = 4000, is_open = False))
                    ], xl = 8, lg = 8, md = 8, sm = 8, xs = 8)
                ]),
                html.Br()
            ]),
            html.Hr(),
            # dbc.Row([
            #     dbc.Col([
            #         dbc.Button('Agregar galpón', id = 'callapse_button_agregar_galpon',
            #                    outline = True, color = 'dark')
            #     ], xl = 6, lg = 6, md = 6, sm = 10, xs = 10)
            # ]),
            # dbc.Collapse(id = 'collapse_agregar_galpon', children = [
            #     html.Br(),
            #     dbc.Row([
            #         campos(id_ = 'gerente_galpon_nc', label = 'GERENTE DE ZONA', ayuda = '-', tipo = 'seleccion',
            #           valor = [{'label': i, 'value': i} for i in get_data('SELECT nombre_gerente FROM gerentes')['nombre_gerente']] if rol == 'administrador' else [{'label': i, 'value': i} for i in get_data(f"SELECT nombre_gerente FROM gerentes WHERE nombre_gerente = '{user.upper()}'")['nombre_gerente']],
            #           xl = 3, lg = 4, md = 6, sm = 6, xs = 6)                     
            #     ]),
            #     dbc.Row([
            #         nit_clientes_galpon_nc, nombre_clientes_galp,
            #     ]),
            #     dbc.Row([
            #         granja_galpon_nc,
            #         campos(tipo = 'number', label = 'Número de galpones', ayuda = 'Ingrese el número de galpones a crear', id_ = 'numero_galpones_nc'),
            #     ]),
            #     dbc.Row([                    
            #         campos(tipo = 'boton', valor = 'Cargar tabla de ingreso', id_ = 'cargar_tabla_ingreso_galpones_nc',
            #                xl = 3, lg = 4, md = 5, sm = 5, xs = 6)
            #     ]),
            #     html.Br(),
            #     dbc.Row([
            #         dbc.Col([
            #             html.Div(id = 'tabla_ingreso_galpones_nc', style = {'overflow': 'auto', 'white-space': 'nowrap'})
            #         ])
            #     ]),
            #     dbc.Row([
            #         dbc.Col([
            #             dbc.Alert(id = 'tabla_ingreso_galpones_nc_sal', is_open = False, dismissable = True)
            #         ])
            #     ]),
            #     html.Br(),              
            #     # dbc.Row([
            #     #     nombre_galpon_nc
            #     # ]),
            #     # dbc.Row([
            #     #     temperatura_galpon_nc, humedad_galpon_nc
            #     # ]),
            #     # dbc.Row([
            #     #     tipo_galpon_nc, tipo_comedero_nc, tipo_bebedero_nc
            #     # ]),
            #     dbc.Row([
            #         dbc.Col([
            #             dbc.Button('Agregar galpón', id = 'agregar_galpon_nc', color = 'warning')
            #         ], xl = 2, lg = 2, md = 3, sm = 4, xs = 4),
            #         dbc.Col([
            #             dbc.Spinner(dbc.Alert(id = 'alert_agregar_galpon_nc', duration = 4000, is_open = False))
            #         ], xl = 8, lg = 8, md = 8, sm = 8, xs = 8)
            #     ]),
            # ]),
            html.Hr(),
        ]

### CALLBACKS PESTAÑA SEGUIMIENTO DE ALZADAS
# calculo de tiempo_cp
@app.callback([Output('edad_p1_1_sal', 'children'),
               Output('dias_p1_1_sal', 'children')],
               Input('calc_p1', 'n_clicks'),
               [State('fecha_ac_p1', 'date'),
                State('fecha_u_v_p1', 'date'),
                State('fecha_nac_p1', 'date')])
def calc_p1(n, fecha_actual, fecha_ult_v, fecha_nac):
    f1 = datetime.strptime(fecha_nac, '%Y-%m-%d')
    f2 = datetime.strptime(fecha_actual, '%Y-%m-%d')
    f3 = datetime.strptime(fecha_ult_v, '%Y-%m-%d')
    edad = rdelta.relativedelta(f2, f1)
    dias = f2 - f3
    edad = edad.years*12 + edad.months
    dias = dias.days

    c_edad = dbc.FormGroup([
        dbc.Label('Edad'),
        dbc.Input(id = 'edad_p1_1',
                    type = 'number',
                    debounce = True,
                    value = edad),
        dbc.FormText('Meses')
    ], style = {'padding-left': '5px'})

    c_dias = dbc.FormGroup([
        dbc.Label('Días'),
        dbc.Input(id = 'dias_p1_1',
                    type = 'number',
                    debounce = True,
                    value = dias),
        dbc.FormText('Entre visita')
    ], style = {'padding-left': '5px'})
    return [[c_edad], [c_dias]]

# criadero
@app.callback(Output('criadero_p1', 'options'),
              Input('gerente_p1', 'value'),
              State('user_info', 'data'))
def criaderop1(gerente, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'administrador':
        if gerente is None:
            return [{'label': 'Debe seleccionar un gerente', 'value': None}]
        sql = f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {gerente}'
        try:
            criaderos = get_data(sql)
        except Exception as e:
            print(e)
            return [{'label': 'Error al consultar criaderos', 'value': None}]
        if criaderos.empty:
            return [{'label': 'Sin registros', 'value': None}]
        else:
            criaderos.drop_duplicates(inplace=True)
            criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
            criaderos.reset_index(inplace = True, drop = True)
            return [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])]
    else:
        return no_update

# nombre equino p1
@app.callback(Output('nombre_p1_col', 'children'),
              [Input('nuevo_e_p1', 'value'),
              Input('criadero_p1', 'value')],
             [State('user_info', 'data'),
              State('gerente_p1', 'value')])
def nom_p1(nuevo, criadero, data, gerente):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'administrador':
        if gerente is None:
            return no_update
        if criadero is None:
            return no_update
        if nuevo == 'No':
            try:
                sql = f'''SELECT id_equino, nombre_equino FROM equinos WHERE id_gerente = {gerente} AND id_criadero = {criadero};'''
                equinos = get_data(sql)
            except Exception as e:
                print(e)
                return no_update
            if equinos.empty:
                equinos = pd.DataFrame({'id_equino': [None],
                                        'nombre_equino': ['Sin registros']})
            equinos.sort_values(by = ['nombre_equino'], inplace = True)
            equinos.drop_duplicates(inplace = True)
            equinos.reset_index(drop = True, inplace = True)
            options = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])]
            campo = [dbc.FormGroup([
                    dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
                    dbc.Select(id = 'nombre_p1', 
                            options = options),
                    dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
                    ], style = {'padding-left': '5px'})]
            return campo         
        elif nuevo == 'Si':
            campo = [dbc.FormGroup([
                    dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
                    dbc.Input(id = 'nombre_p1', placeholder = 'Ingrese el nombre del equino', type = 'text',
                            debounce = True),
                    dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
                    ], style = {'padding-left': '5px'})]
            return campo
    elif rol == 'gerente':
        if criadero == None:
            return no_update
        if nuevo == 'No':
            try:
                sql = f'''SELECT id_equino, nombre_equino FROM equinos WHERE id_gerente = {doc_id} AND id_criadero = {criadero};'''
                equinos = get_data(sql)
            except Exception as e:
                print(e)
                return no_update
            if equinos.empty:
                equinos = pd.DataFrame({'id_equino': [None],
                                        'nombre_equino': ['Sin registros']})
            equinos.sort_values(by = ['nombre_equino'], inplace = True)
            equinos.drop_duplicates(inplace = True)
            equinos.reset_index(drop = True, inplace = True)
            options = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])]
            campo = [dbc.FormGroup([
                    dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
                    dbc.Select(id = 'nombre_p1', 
                            options = options),
                    dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
                    ], style = {'padding-left': '5px'})]
            return campo         
        elif nuevo == 'Si':
            campo = [dbc.FormGroup([
                    dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
                    dbc.Input(id = 'nombre_p1', placeholder = 'Ingrese el nombre del equino', type = 'text',
                            debounce = True),
                    dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
                    ], style = {'padding-left': '5px'})]
            return campo
        
    elif rol == 'cliente':
        if nuevo == 'No':
            try:
                sql = f'''SELECT id_equino, nombre_equino FROM equinos WHERE id_criadero = {doc_id};'''
                equinos = get_data(sql)
            except Exception as e:
                print(e)
                return no_update
            if equinos.empty:
                equinos = pd.DataFrame({'id_equino': [None],
                                        'nombre_equino': ['Sin registros']})
            equinos.sort_values(by = ['nombre_equino'], inplace = True)
            equinos.drop_duplicates(inplace = True)
            equinos.reset_index(drop = True, inplace = True)
            options = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])]
            campo = [dbc.FormGroup([
                    dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
                    dbc.Select(id = 'nombre_p1', 
                            options = options),
                    dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
                    ], style = {'padding-left': '5px'})]
            return campo         
        elif nuevo == 'Si':
            campo = [dbc.FormGroup([
                    dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
                    dbc.Input(id = 'nombre_p1', placeholder = 'Ingrese el nombre del equino', type = 'text',
                            debounce = True),
                    dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
                    ], style = {'padding-left': '5px'})]
            return campo


# planta de alimento
@app.callback(Output('planta_p1', 'options'),
              Input('tabs', 'active_tab'),
              State('user_info', 'data'))
def plantap1(t, data):
    if t == 'tab_ingreso_datos':
        usuario = pd.read_json(data, orient = 'split')
        rol = usuario['rol_usuario'].values[0]
        user = usuario['nombre'].values[0]
        doc_id = usuario['doc_id'].values[0]
        pais = usuario['pais'].values[0]
        df_plantas = pd.DataFrame({'pais': {0: 'Panamá', 1: 'Colombia', 2: 'Colombia', 3: 'Colombia', 4: 'Colombia', 5: 'Colombia', 6: 'Colombia', 7: 'Colombia', 8: 'Colombia', 9: 'Colombia', 10: 'Colombia', 11: 'Colombia', 12: 'Colombia', 13: 'Colombia', 14: 'Ecuador'}, 
                                'planta': {0: 'Panamá', 1: 'Barranquilla', 2: 'Cota', 3: 'Funza', 4: 'Girardota', 5: 'Giron 1', 6: 'Giron 2', 7: 'Ibague', 8: 'Palermo', 9: 'Palmira', 10: 'Pereira', 11: 'Santa Rosa', 12: 'Villavicencio', 13: 'Yarumal', 14: 'Ecuador'}})
        plantas = df_plantas.loc[df_plantas['pais'] == pais.title(), 'planta']
        return [{'label': i, 'value': i} for i in plantas]
    else:
        return no_update

# etapa fisiologca
@app.callback(Output('etapa_p1', 'value'),
              Input('edad_p1_1', 'value'))
def actEtapa(edad):
    if isinstance(edad, str) or edad is None:
        return no_update
    if edad > 40:
        return 'Adulto'
    elif edad <= 40:
        return 'Potro'
    else:
        return no_update

# cargar datos equino
@app.callback([Output('raza_p1', 'value'),
               Output('planta_p1', 'value'),
               Output('sexo_p1', 'value'),
               Output('peso_a_p1', 'value'),
               Output('andar_p1', 'value')],
               Input('nombre_p1', 'value'),
               [State('user_info', 'data'),
                State('criadero_p1', 'value'),
                State('nuevo_e_p1', 'value')])
def cargarDatosEquino(nombre, data, criadero, nuevo):
    if nombre is None:
        return [None]*5
    if nuevo == 'Si':
        raise dash.exceptions.PreventUpdate()
    else:
        usuario = pd.read_json(data, orient = 'split')
        rol = usuario['rol_usuario'].values[0]
        user = usuario['nombre'].values[0]
        doc_id = usuario['doc_id'].values[0]
        pais = usuario['pais'].values[0]
        sql = f'''SELECT seguimiento_alzadas.fecha, equinos.raza, equinos.sexo, equinos.andar, seguimiento_alzadas.planta_alimento, seguimiento_alzadas.peso_kg FROM equinos INNER JOIN seguimiento_alzadas ON equinos.id_equino =  seguimiento_alzadas.id_equino WHERE equinos.id_equino = {nombre}'''
        try:
            dt_equino = get_data(sql)
        except Exception as e:
            print(e)
            return [None]*5
        if dt_equino.empty:
            return [None]*5
        else:
            dt_equino['fecha'] = pd.to_datetime(dt_equino['fecha'])
            datos_ = dt_equino.loc[(dt_equino['fecha'] == dt_equino['fecha'].max()) &
                                   (dt_equino['andar'] != '')]
            if datos_.empty:
                return [None]*5
            datos = datos_.iloc[-1,:]
            return [datos['raza'], datos['planta_alimento'], datos['sexo'], datos['peso_kg'], datos['andar']]

# ocultar andar
@app.callback(Output('andar_p1_col', 'style'),
              Input('raza_p1', 'value'))
def verAndar(raza):
    if raza is None or raza == 'Criollo Colombiano':
        return {'display': 'inline'}
    elif raza != 'Criollo Colombiano':
        return {'display': 'none'}        

# ocultar peso anterior
@app.callback(Output('peso_a_p1_col', 'style'),
              Input('nuevo_e_p1', 'value'))
def verPesoA(nuevo):
    if nuevo == 'No':
        return {'display': 'inline'}
    else:
        return {'display': 'none'}

# mostrar campos depto/mun crear equino
@app.callback([Output('mun_p1_col', 'style'),
               Output('mun_p1', 'options')],
               Input('nuevo_e_p1', 'value'),
               [State('criadero_p1', 'value'),
                State('user_info', 'data')])
def ubicacion(nuevo, criadero, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'cliente':
        criadero = doc_id
    if nuevo == 'No' or criadero is None:
        style = {'display': 'none'}
        return [style, no_update]
    elif nuevo == 'Si':
        style = {'display': 'inline'}
        sql = f'SELECT departamento_provincia, municipio FROM criaderos WHERE id_criadero = {criadero}'
        deptos = get_data(sql)
        ubicacion = [{'label': deptos['municipio'][i], 'value': deptos['departamento_provincia'][i]+'-'+deptos['municipio'][i]} for i in range(deptos.shape[0])]
        return [style, ubicacion]

# influenza + tetano
@app.callback([Output('fecha_influenza_t_col', 'style'),
               Output('prx_influenza_t_col', 'style'),
               Output('obs_influenza_t_col', 'style')],
              Input('influenza_t', 'value'))
def hidenInfluenza(n):
    print(n)
    if n is None or n == 'No':
        return [{'display': 'none'}]*3
    else:
        return [{'display': 'inline'}]*3


# tetano
@app.callback([Output('fecha_tetano_col', 'style'),
               Output('prx_tetano_col', 'style'),
               Output('obs_tetano_col', 'style')],
              Input('tetano', 'value'))
def hidenTetano(n):
    if n is None or n == 'No':
        return [{'display': 'none'}]*3
    else:
        return [{'display': 'inline'}]*3

# encefalitis
@app.callback([Output('fecha_encefalitis_col', 'style'),
               Output('prx_encefalitis_col', 'style'),
               Output('obs_encefalitis_col', 'style')],
              Input('encefalitis', 'value'))
def hidenTetano(n):
    if n is None or n == 'No':
        return [{'display': 'none'}]*3
    else:
        return [{'display': 'inline'}]*3

# desparacitacion
@app.callback([Output('fecha_desparasitacion_col', 'style'),
               Output('prx_desparasitacion_col', 'style'),
               Output('obs_desparasitacion_col', 'style')],
              Input('desparasitacion', 'value'))
def hidenTetano(n):
    if n is None or n == 'No':
        return [{'display': 'none'}]*3
    else:
        return [{'display': 'inline'}]*3

# validar p1
@app.callback([Output('salida_val_p1', 'children'),
               Output('salida_val_p1', 'is_open'),
               Output('salida_val_p1', 'color'),
               Output('modal_sa', 'is_open'),
               Output('div_validacion_ss', 'children'),
               Output('val_sa_data', 'data'),
               Output('div_validacion_plan', 'children'),
               Output('val_plan_data', 'data')],
              Input('validar_p1', 'n_clicks'),
              [State(i, 'value') for i in ids_p1] + 
              [State('user_info', 'data')] + 
              [State(i, 'date') for i in ids_plan_s[:8]] + 
              [State(i, 'value') for i in ids_plan_s[8:]])
def validar_p1(n,edad, dias, gerente, criadero, nuevo, nombre, raza, planta, ref,
               etapa, sexo, peso, peso_a, alzada, condicion, calidad, andar, obs,
               municipio, data, fecha_influenza_t, prx_influenza_t, fecha_tetano, prx_tetano, 
               fecha_encefalitis, prx_encefalitis, fecha_desparasitacion, prx_desparasitacion, 
               influenza_t, obs_influenza_t, tetano, obs_tetano, encefalitis, obs_encefalitis, 
               desparasitacion,  obs_desparasitacion):

    if n is None:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if isinstance(edad, str) or edad == None or edad < 0:
        return [['Edad equino no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if dias != None:
        if isinstance(dias, str) or dias < 0:
            return [['Días entre visita no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [['Gerente de zona no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
        if criadero == None or criadero == '':
            return [['Criadero no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]            
    if rol == 'gerente':
        gerente = doc_id
        if criadero == None or criadero == '':
            return [['Criadero no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if rol == 'cliente':
        criadero = doc_id
    if nombre == None or nombre == '':
        return [['Nombre de equino no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if nuevo == 'Si':
        if municipio is None:
            return [['Municipio no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
        mun = municipio.split('-')[1]
        depto = municipio.split('-')[0]
    if raza == None:
        return [['Raza del equino no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if planta == None or planta == '-':
        return [['Planta de alimento no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if ref == None or ref == '':
        return [['Referencia de alimento no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if etapa == None:
        return [['Etapa fisiológica no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if sexo == None:
        return [['Sexo no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if peso != None and peso < 0:
        return [['Peso del equino no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if (isinstance(peso_a, str) or peso_a == None or peso_a < 0) and dias > 0 and nuevo == 'No':
        return [['Peso anterior no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if  alzada != None and alzada < 0:
        return [['Alzada del equino no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if condicion == None or condicion == '':
        return [['Condición corporal no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if calidad == None or calidad == '':
        return [['Calidad de pelaje no valida'], True, 'warning', False, no_update, no_update, no_update, no_update]
    if andar == None and raza == 'Criollo Colombiano':
        return [['Andar no valido'], True, 'warning', False, no_update, no_update, no_update, no_update]

    if influenza_t is None:
        return ['Vacuna Influenza + tétano no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
    elif influenza_t == 'Si':
        if fecha_influenza_t is None:
            return ['Fecha vacunación  Influenza + tétano no valido', True, 'warning', False, no_update, no_update, no_update, no_update]
        if prx_influenza_t is None:
            return ['Fecha próxima vacunación  Influenza + tétano no valido', True, 'warning', False, no_update, no_update, no_update, no_update]
    if tetano is None:
        return ['Vacuna Tétano no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
    elif tetano == 'Si':
        if fecha_tetano is None:
            return ['Fecha vacunación tétano no valido', True, 'warning', False, no_update, no_update, no_update, no_update]
        if prx_tetano is None:
            return ['Fecha próxima vacunación  tétano no valido', True, 'warning', False, no_update, no_update, no_update, no_update]        
    if encefalitis is None:
        return ['Vacuna encefalitis equina venezolana no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
    elif encefalitis == 'Si':
        if fecha_encefalitis is None:
            return ['Fecha vacunación encefalitis equina venezolana no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
        if prx_encefalitis is None:
            return ['Fecha proxima vacunación encefalitis equina venezolana no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
    if desparasitacion is None:
        return ['Desparasitación no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
    elif desparasitacion == 'Si':
        if fecha_desparasitacion is None:
            return ['Fecha desparacitación no valida', True, 'warning', False, no_update, no_update, no_update, no_update]
        if prx_desparasitacion is None:
            return ['Fecha próxima desparacitación no valida', True, 'warning', False, no_update, no_update, no_update, no_update]        


    and_ = andar if raza == 'Criollo Colombiano' else ''
    peso_A = peso_a if dias > 0 or nuevo == 'No' else ''
    if isinstance(peso, str) or peso is None:
        gpd = nan
    else:
        gpd = 0 if dias == 0 or nuevo == 'Si' else round(1000*(peso-peso_A)/dias)
    if isinstance(alzada, str) or alzada is None:
        alzada = nan

    if rol == 'cliente':
        try:
            gerente_dt = get_data(f'SELECT id_gerente FROM criaderos WHERE id_criadero = {criadero}')
            gerente = gerente_dt['id_gerente'].values[0]
        except Exception as e:
            print(e)
            return [['Error al consultar la información'], True, 'warning', False, no_update, no_update, no_update]
    if nuevo == 'No':
        sql = f'SELECT DISTINCT criaderos.nombre_criadero, equinos.nombre_equino, equinos.departamento_provincia, equinos.municipio, gerentes.nombre_gerente FROM criaderos LEFT JOIN equinos ON criaderos.id_criadero = equinos.id_criadero LEFT JOIN gerentes ON gerentes.doc_id = equinos.id_gerente WHERE equinos.id_equino = {nombre} AND criaderos.id_criadero = {criadero} AND gerentes.doc_id = {gerente}'
    else:
        sql = f'SELECT DISTINCT criaderos.nombre_criadero, gerentes.nombre_gerente FROM criaderos LEFT JOIN gerentes ON gerentes.doc_id = criaderos.id_gerente WHERE criaderos.id_gerente = {gerente} AND criaderos.id_criadero = {criadero}'
    try:
        faltantes = get_data(sql)
    except Exception as e:
        print(e)
        return [['Error al consultar la información'], True, 'warning', False, no_update, no_update, no_update]
    if nuevo == 'Si':
        equino_id = randint(100000, 999999)
        if equino_id in get_data('SELECT id_equino FROM equinos')['id_equino']:
            return [['Por favor intente nuevamente'], True, 'warning', False, no_update, no_update, no_update]
    db = {'Fecha': datetime.today().date().strftime('%Y/%m/%d'),
            'Pais': pais.title(),
            'id_gerente': gerente,
            'Gerente de Zona': faltantes['nombre_gerente'].values[0].title(),
            'Departamento/Provincia': faltantes['departamento_provincia'].values[0] if nuevo == 'No' else depto,
            'Municipio': faltantes['municipio'].values[0] if nuevo == 'No' else mun,
            'id_criadero': criadero,
            'Nombre Criadero': faltantes['nombre_criadero'].values[0],
            'id_equino': nombre if nuevo == 'No' else equino_id,
            'Nombre Equino': faltantes['nombre_equino'].values[0] if nuevo == 'No' else nombre.title(),
            'Raza': raza,
            'Planta de alimento': planta,
            'Referencia Alimento': ref,
            'Etapa Fisiológica': etapa,
            'Edad (Meses)': edad,
            'Sexo': sexo,
            'Andar': and_,
            'Peso (Kg)': peso,
            'Pesaje Anterior (Kg)': peso_A,
            'Días entre visitas': dias if nuevo == 'No' else 0,
            'GPD (g)': gpd,
            'Alzada (cm)': alzada,
            'Referencia Alzada (cm)': '',
            'Diferencia (cm)': '',
            'Condicion Corporal': condicion,
            'Calidad del Pelaje': calidad,
            'Observaciones': obs}

    if db['Raza'] == 'Criollo Colombiano':
        sql = 'SELECT * FROM referencia_alzada;'
        ref = get_data(sql)
        andar = db['Andar']
        sexo = db['Sexo']
        meses = db['Edad (Meses)'] if db['Edad (Meses)'] <= 41 else 41

        if sexo == 'Macho' and ('P1' in andar or 'P2' in andar):
            db['Referencia Alzada (cm)'] = ref.loc[ref['MESES'] == meses]['MACHOS: P1, P2'].values[0]
            db['Diferencia (cm)'] = round(db['Alzada (cm)'] - db['Referencia Alzada (cm)'], 2)

        if sexo == 'Hembra' and ('P3' in andar or 'P4' in andar):
            db['Referencia Alzada (cm)'] = ref.loc[ref['MESES'] == meses]['HEMBRAS: P3,P4'].values[0]
            db['Diferencia (cm)'] = round(db['Alzada (cm)'] - db['Referencia Alzada (cm)'], 2)

        if (sexo == 'Hembra') and ('P1' in andar or 'P2' in andar):
            db['Referencia Alzada (cm)'] = ref.loc[ref['MESES'] == meses]['HEMBRAS: P1,P2  MACHOS: P3,P4'].values[0]
            db['Diferencia (cm)'] = round(db['Alzada (cm)'] - db['Referencia Alzada (cm)'], 2)

        if (sexo == 'Macho') and ('P3' in andar or 'P4' in andar):
            db['Referencia Alzada (cm)'] = ref.loc[ref['MESES'] == meses]['HEMBRAS: P1,P2  MACHOS: P3,P4'].values[0]
            db['Diferencia (cm)'] = round(db['Alzada (cm)'] - db['Referencia Alzada (cm)'], 2)  
    db = pd.DataFrame(db, index = [0])
    db.columns = ['fecha', 'pais', 'id_gerente', 'gerente_zona',
                'departamento_provincia', 'municipio', 'id_criadero', 'nombre_criadero',
                'id_equino', 'nombre_equino', 'raza', 'planta_alimento',
                'referencia_alimento', 'etapa_fisiologica', 'edad_meses', 'sexo',
                'andar', 'peso_kg', 'peso_anterior_kg', 'dias_entre_visita', 'gpd_g',
                'alzada_cm', 'referencia_alzada_cm', 'diferencia_cm',
                'condicion_corporal', 'calidad_pelaje', 'observaciones']
    
    if nuevo == 'Si':
        try:
            equino_nuevo = pd.DataFrame({'fecha': [datetime.today().date().strftime('%Y/%m/%d')],
                                         'id_equino': [equino_id],
                                         'nombre_equino': [nombre.title()],
                                         'raza': [raza],
                                         'sexo': [sexo],
                                         'andar': [andar],
                                         'departamento_provincia': [depto],
                                         'municipio': [mun],
                                         'pais': [pais.title()],
                                         'id_gerente': [gerente],
                                         'id_criadero': [criadero]})
            insert_dataframe(equino_nuevo, 'equinos')
        except Exception as e:
            print(e)
            return [['Error al crear nuevo equino'], True, 'warning', no_update, no_update, no_update, no_update]
    
    data_plan_sanitario = pd.DataFrame({'fecha': [],
                                        'tipo': [],
                                        'aplica': [],
                                        'fecha_vacunacion': [],
                                        'fecha_proxima_vacunacion': [],
                                        'observaciones':[],
                                        'id_criadero': [],
                                        'id_equino': []})
    if influenza_t == 'Si':
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Vacuna Influenza + tétano',
                                                          'Si', fecha_influenza_t, prx_influenza_t, obs_influenza_t,
                                                          db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)
    else:
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Vacuna Influenza + tétano',
                                                          'No', nan, nan, nan, db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)
    
    if tetano == 'Si':
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Vacuna Tétano',
                                                          'Si', fecha_tetano, prx_tetano, obs_tetano,
                                                          db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)
    else:
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Vacuna Tétano',
                                                          'No', nan, nan, nan, db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)    
    
    if encefalitis == 'Si':
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Vacuna encefalitis equina venezolana',
                                                          'Si', fecha_encefalitis, prx_encefalitis, obs_encefalitis,
                                                          db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)
    else:
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Vacuna encefalitis equina venezolana',
                                                          'No', nan, nan, nan, db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)    

    if desparasitacion == 'Si':
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Desparasitación',
                                                          'Si', fecha_desparasitacion, prx_desparasitacion, obs_desparasitacion,
                                                          db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)
    else:
        data_plan_sanitario = data_plan_sanitario.append(pd.DataFrame([[db['fecha'].values[0], 'Desparasitación',
                                                          'No', nan, nan, nan, db['id_criadero'].values[0], db['id_equino'].values[0]]], columns=data_plan_sanitario.columns), ignore_index=True)    

    try:
        data_resumen = db.copy()
        data_resumen = data_resumen.drop(['id_gerente', 'id_criadero', 'id_equino'], axis = 1)
        data_resumen.columns = ['Fecha', 'Pais', 'Gerente',
                                'Departamento', 'Municipio', 'Criadero',
                                'Equino', 'Raza', 'Planta Alimento',
                                'Referencia Alimento', 'Etapa Fisiologica', 'Edad Meses', 'Sexo',
                                'Andar', 'Peso kg', 'Peso anterior Kg', 'Dias entre visita', 'GPD g',
                                'Alzada cm', 'Referencia Alzada cm', 'Diferencia cm',
                                'Condición Corporal', 'Calida Pelaje', 'Observaciones']
        data_resumen = data_resumen.transpose()
        data_resumen['Variable'] = data_resumen.index
        data_resumen.columns = ['Valor', 'Variable']
        data_resumen = data_resumen[['Variable', 'Valor']]
        resumen = dbc.Table.from_dataframe(data_resumen, striped = True, bordered = True, hover = True)        
        data_plan_sanitario_ = data_plan_sanitario.drop(columns = ['id_criadero', 'id_equino'])
        data_plan_sanitario_.columns = ['Fecha', 'Tipo', 'Aplica', 'Fecha vacunación', 'Fecha próxima', 'Observaciones']
        resumen_plan = dbc.Table.from_dataframe(data_plan_sanitario_, striped = True, bordered = True, hover = True)        
        #insert_dataframe(db, 'seguimiento_alzadas')
        return ['Información validada con éxito', True, 'success', True, [resumen], db.to_json(date_format='iso', orient = 'split'), resumen_plan, data_plan_sanitario.to_json(date_format = 'iso', orient = 'split')]
    except Exception as e: 
        print(e)
        return ['Ha ocurrido un error al validar la información', True, 'warning', False, no_update, no_update, no_update, no_update]

# enviar p1
@app.callback([Output('salida_p1', 'children'),
               Output('salida_p1', 'is_open'),
               Output('salida_p1', 'color'),
               Output('nombre_p1', 'value'),
               Output('ref_p1', 'value'),
               Output('peso_p1', 'value'),
               Output('alzada_p1', 'value'),
               Output('condicion_p1', 'value'),
               Output('calidad_p1', 'value'),
               Output('obs_p1', 'value'),
               Output('influenza_t', 'value'),
               Output('tetano', 'value'),
               Output('encefalitis', 'value'),
               Output('desparasitacion', 'value'),],
              Input('confirm_p1', 'submit_n_clicks'),
              [State(i, 'value') for i in ids_p1_] + [State('val_sa_data', 'data')]+ [State('val_plan_data', 'data')] + [State(i, 'value') for i in ids_plan_s_])
def enviar_p1(n, nombre, ref, peso, alzada, condicion, calidad, obs, data, data_ap, influenza_t, tetano, encefalitis, desparasitacion):
    if n is None:
        return ['Ha ocurrido un error al cargar la información', False, 'warning', nombre, ref, peso, alzada, condicion, calidad, obs, influenza_t, tetano, encefalitis, desparasitacion]
    try:
        db = pd.read_json(data, orient = 'split')
        db['fecha'] = db['fecha'].apply(lambda x: x.split('T')[0])
    except Exception as e:
        print(e)
        return ['Ha ocurrido un error al cargar la información', True, 'warning', nombre, ref, peso, alzada, condicion, calidad, obs, influenza_t, tetano, encefalitis, desparasitacion]

    try:
        db_plan = pd.read_json(data_ap, orient = 'split')
        db_plan['fecha'] = db_plan['fecha'].apply(lambda x: x.split('T')[0])
    except Exception as e:
        print(e)
        return ['Ha ocurrido un error al cargar la información sanitaria', True, 'warning', nombre, ref, peso, alzada, condicion, calidad, obs, influenza_t, tetano, encefalitis, desparasitacion]

    try:
        insert_dataframe(db, 'seguimiento_alzadas')
        print(db_plan)
        insert_dataframe(db_plan, 'plan_sanitario')
        return ['Información enviada con éxito', True, 'success', None, None, None, None, None, None, None, None, None, None, None]
    except Exception as e: 
        print(e)
        return ['Ha ocurrido un error al enviar la información', True, 'warning', nombre, ref, peso, alzada, condicion, calidad, obs, influenza_t, tetano, encefalitis, desparasitacion]




### CALLBACKS ENTRENAMIENTO DEPORTIVO
# piscina p2
@app.callback([Output('freq_ps_sal', 'style'),
               Output('tiempo_ps_sal', 'style')],
               Input('piscina_p2', 'value'))
def pisicina(value):
    if value == 'No':
        style = {'padding-left': '5px', 'visibility': 'hidden'}
        return [style, style]
    elif value == 'Si':
        style = {'padding-left': '5px', 'visibility': 'visible'}
        return [style, style]
    else:
        raise dash.exceptions.PreventUpdate()

# piso duro p2
@app.callback([Output('freq_pd_sal', 'style'),
               Output('tiempo_pd_sal', 'style')],
               Input('pisod_p2', 'value'))
def piso(value):
    if value == 'No':
        style = {'padding-left': '5px', 'visibility': 'hidden'}
        return [style, style]
    elif value == 'Si':
        style = {'padding-left': '5px', 'visibility': 'visible'}
        return [style, style]
    else:
        raise dash.exceptions.PreventUpdate()

# torno p2
@app.callback([Output('freq_tr_sal', 'style'),
               Output('tiempo_tr_sal', 'style')],
               Input('torno_p2', 'value'))
def torno(value):
    if value == 'No':
        style = {'padding-left': '5px', 'visibility': 'hidden'}
        return [style, style]
    elif value == 'Si':
        style = {'padding-left': '5px', 'visibility': 'visible'}
        return [style, style]
    else:
        raise dash.exceptions.PreventUpdate()

# campo p2
@app.callback([Output('freq_cp_sal', 'style'),
               Output('tiempo_cp_sal', 'style')],
               Input('campo_p2', 'value'))
def campo(value):
    if value == 'No':
        style = {'padding-left': '5px', 'visibility': 'hidden'}
        return [style, style]
    elif value == 'Si':
        style = {'padding-left': '5px', 'visibility': 'visible'}
        return [style, style]
    else:
        raise dash.exceptions.PreventUpdate()

# Entrenamiento p2
@app.callback(Output('tiempo_cl_sal', 'style'),
               Input('calen_p2', 'value'))
def calen(value):
    if value == 'No':
        style = {'padding-left': '5px', 'visibility': 'hidden'}
        return style
    elif value == 'Si':
        style = {'padding-left': '5px', 'visibility': 'visible'}
        return style
    else:
        raise dash.exceptions.PreventUpdate()

# Imagen
@app.callback([Output('img_p2', 'color'),
               Output('imagen_rhemo', 'data')],
              [Input('upload_p2', 'filename'),
               Input('upload_p2', 'contents')])
def upload(name, contents):
    if name is not None and contents is not None:
        try:
            save_file(name, contents, name, 'Reportes/')
            image_data = pd.DataFrame({'file': [name]})
            return ['success', image_data.to_json(orient = 'split')]
        except Exception as e:
            print(e)
            return ['warning', no_update]
    else:
        return ['warning', no_update]

# @app.callback(Output("download_p2_", "data"),
#               Input('download_p2', 'n_clicks'))
# def download_p2(n):
#     global report
#     if n is None or n == 0 or report == '':
#         raise dash.exceptions.PreventUpdate()
#     if os.path.exists(report):
#         return send_file(report)
#     raise dash.exceptions.PreventUpdate()


#irc p2
@app.callback(Output('ind_rc_p2', 'value'),
               Input('fc_fn_1_p2', 'value'),
               State('fc_fn_p2', 'value'))
def irc(fc_1, fc):
    if isinstance(fc, str) or isinstance(fc_1, str):
        raise dash.exceptions.PreventUpdate()
    if fc is None or fc_1 is None:
        raise dash.exceptions.PreventUpdate()
    if fc < 0 or fc_1 < 0:
        raise dash.exceptions.PreventUpdate()
    return round(100*(fc - fc_1)/fc, 2)

#round(100*(fc_fin - fc_1min)/fc_fin, 2)
# enviar p2
@app.callback([Output('salida_p2', 'children'),
               Output('salida_p2', 'is_open'),
               Output('salida_p2', 'color'),
               Output('download_p2_', 'data')],
              Input('confirm_p2', 'submit_n_clicks'),
              [State(i, 'value') for i in ids_p2] + [State('imagen_rhemo', 'data'), State('user_info', 'data')])
def enviarP2(n, criadero, nombre, raza, edad, peso, condicion, calidad,
              alzada, etapa, ref, piscina, freq_ps, tiempo_ps, pisod, freq_pd,
              tiempo_pd, torno, freq_tr, tiempo_tr, campo, freq_cp, tiempo_cp,
              calen, tiempo_cl, fc_max, fc_min, fc_prom, h_in, h_fn, grado, agua,
              sal, fc_fin, fc_1min, id_rc, obs, image_data, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]              
    if n is None:
        raise dash.exceptions.PreventUpdate()
    if pais == None or pais == '':
        return [['Pais no valido'], True, 'warning', no_update]
    if criadero == None or criadero == '':
        return [['Criadero en blanco'], True, 'warning', no_update]
    if nombre == None or nombre == '':
        return [['Nombre del equino no valido'], True, 'warning', no_update]
    if raza == None:
        return [['Raza no valida'], True, 'warning', no_update]
    if isinstance(edad, str) or edad == None or edad < 0:
        return [['Edad no validad'], True, 'warning', no_update]
    if isinstance(peso, str) or peso == None or peso < 0:
        return [['Peso no valido'], True, 'warning', no_update]
    if condicion == None:
        return [['Condición corporal no valida'], True, 'warning', no_update]
    if calidad == None:
        return [['Calidad de pelaje no valida'], True, 'warning', no_update]
    if isinstance(alzada, str) or alzada == None or alzada < 0:
        return [['Alzada no valida'], True, 'warning', no_update]
    if etapa == None:
        return [['Etapa fisiológica no valida'], True, 'warning', no_update]
    if ref == None:
        return [['Referencia de alimento no valida'], True, 'warning', no_update]
    if piscina == None:
        return [['Entrenamiento piscina no valido'], True, 'warning', no_update]
    if (piscina == 'Si') and (isinstance(freq_ps, str) or freq_ps == None or freq_ps < 0):
        return [['Frecuencia de piscina no valida'], True, 'warning', no_update]
    if (piscina  == 'Si') and (isinstance(tiempo_ps, str) or tiempo_ps == None or tiempo_ps < 0):
        return [['Tiempo piscina no valido'], True, 'warning', no_update]
    if pisod == None:
        return [['Entrenamiento piso duro no valido'], True, 'warning', no_update]
    if (pisod  == 'Si') and (isinstance(freq_pd, str) or freq_pd == None or freq_pd < 0):
        return [['Frecuencia de piso duro no valido'], True, 'warning', no_update]
    if (pisod  == 'Si') and (isinstance(tiempo_pd, str) or tiempo_pd == None or tiempo_pd < 0):
        return [['Tiempo piso duro no valido'], True, 'warning', no_update]
    if torno == None:
        return [['Entrenamiento torno no valido'], True, 'warning', no_update]
    if (torno  == 'Si') and (isinstance(freq_tr, str) or freq_tr == None or freq_tr < 0):
        return [['Frecuencia de torno no valido'], True, 'warning', no_update]
    if (torno  == 'Si') and (isinstance(tiempo_tr, str) or tiempo_tr == None or tiempo_tr < 0):
        return [['Tiempo torno no valido'], True, 'warning', no_update]
    if campo == None:
        return [['Entrenamiento campo no valido'], True, 'warning', no_update]
    if (campo  == 'Si') and (isinstance(freq_cp, str) or freq_cp == None or freq_cp < 0):
        return [['Frecuencia de campo no valido'], True, 'warning', no_update]
    if (campo  == 'Si') and (isinstance(tiempo_cp, str) or tiempo_cp == None or tiempo_cp < 0):
        return [['Tiempo campo no valido'], True, 'warning', no_update]
    if calen ==  None:
        return [['Calentamiento no valido'], True, 'warning', no_update]
    if (calen  == 'Si') and (isinstance(tiempo_cl, str) or tiempo_cl == None or tiempo_cl < 0):
        return [['Tiempo de calentamiento no valido'], True, 'warning', no_update]
    if isinstance(fc_max, str) or fc_max == None or fc_max < 0:
        return [['FC max no valida'], True, 'warning', no_update]
    if isinstance(fc_min, str) or fc_min == None or fc_min < 0:
        return [['FC min no valida'], True, 'warning', no_update]
    if isinstance(fc_prom, str) or fc_prom == None or fc_prom < 0:
        return [['FC prom no valida'], True, 'warning', no_update]
    if h_in == None or h_in == '':
        return [['Hora inicial no valida'], True, 'warning', no_update]
    if h_fn == None or h_fn == '':
        return [['Hora final no valida'], True, 'warning', no_update]
    if grado == None:
        return [['Grado de sudoración no valido'], True, 'warning', no_update]
    if isinstance(agua, str) or agua == None or agua < 0:
        return [['Consumo de agua no valido'], True, 'warning', no_update]
    if sal == None:
        return [['Consumo de sal no valido'], True, 'warning', no_update]
    if isinstance(fc_fin, str) or fc_fin == None or fc_fin < 0:
        return [['FC final no valida'], True, 'warning', no_update]
    if isinstance(fc_1min, str) or fc_1min == None or fc_1min < 0:
        return [['FC final 1 min despues no valida'], True, 'warning', no_update]
    if isinstance(id_rc, str) or id_rc == None or id_rc < 0:
        return [['Índice de recuperación cardica no valido'], True, 'warning', no_update]

    db = {'Fecha': datetime.today().date().strftime('%Y/%m/%d'),
            'Pais': pais,
            'Criadero': criadero,
            'Nombre Equino': nombre,
            'Raza Equino': raza,
            'Edad (meses)': edad,
            'Peso (kg)': peso,
            'Condición Corporal': condicion,
            'Calidad Pelaje': calidad,
            'Alzada (cm)': alzada,
            'Etapa': etapa,
            'Referencia Alimento': ref,
            'Calentamiento': calen,
            'Tiempo c': tiempo_cl if calen == 'Si' else 0,
            'Piscina': piscina,
            'Frecuencia p': freq_ps if piscina == 'Si' else 0,
            'Tiempo p': tiempo_ps if piscina == 'Si' else 0,
            'Piso Duro': pisod,
            'Frecuencia pd': freq_pd if pisod == 'Si' else 0,
            'Tiempo pd': tiempo_pd if pisod == 'Si' else 0,
            'Torno': torno,
            'Frecuencia t': freq_tr if torno == 'Si' else 0,
            'Tiempo t': tiempo_tr if torno == 'Si' else 0,
            'Campo': campo,
            'Frecuencia cp': freq_cp if campo == 'Si' else 0,
            'Tiempo cp': tiempo_cp if campo == 'Si' else 0,
            'Hora Inicio': h_in,
            'Hora Final': h_fn,
            'FC Prom': fc_prom,
            'FC max': fc_max,
            'FC min': fc_min,
            'Grado sudoracion': grado,
            'Consumo Agua': agua,
            'Consumo Sal': sal,
            'FC Final': fc_fin,
            'FC Final (1 min)': fc_1min,
            'IRC': id_rc,
            'Observaciones': obs}

    try:
        add_row_entrenamiento(db)
        #actualizar_valor(archivo = 'Entrenamiento deportivo', hoja = 0, datos = db)
        env_sal = 'enviada con éxito'
    except Exception as e:
        print(e)
        env_sal = 'no enviada'

    datos_equino = {'Fecha': datetime.today().date().strftime('%Y/%m/%d'),
                    'Criadero': criadero,
                    'Nombre': nombre,
                    'Raza': raza,
                    'Edad (meses)': edad,
                    'Peso (kg)': peso}

    estado_equino = {'Condicion Corporal': condicion,
                        'Calidad de Pelaje': calidad,
                        'Alzada (cm)': alzada,
                        'Estado Fisiológico': etapa,
                        'Referencia Alimento': ref}

    entrenamiento = {'Realiza': [calen, piscina, pisod, torno, campo],
                            'Frecuencia por semana': ['', db['Frecuencia p'], db['Frecuencia pd'], db['Frecuencia t'], db['Frecuencia cp']],
                            'Tiempo (minutos)': [db['Tiempo c'], db['Tiempo p'], db['Tiempo pd'], db['Tiempo t'], db['Tiempo cp']]}

    datos_rhemo = {'Hora inicio': h_in,
                    'Hora final': h_fn,
                    'FC prom': fc_prom,
                    'FC máx': fc_max,
                    'FC mín': fc_min}

    otros = {'Grado Sudoración': grado,
                'Consumo Agua (lts)': agua,
                'Consumo Sal a Voluntad': sal,
                'FC Final': fc_fin,
                'FC Final (1 min)': fc_1min,
                'Índice de Recuperación Cardiaca': round(100*(fc_fin - fc_1min)/fc_fin, 2),
                'Observaciones': obs}
    try:
        imagen_data = pd.read_json(image_data, orient = 'split')                
        x_image = imagen_data['file'][0]
    except Exception as e:
        print(e)
        x_image = ''
    return [f'Información {env_sal}', True, 'success', 
            entrenamiento_pdf(datos_equino = datos_equino, estado_equino = estado_equino,
                              entrenamiento = entrenamiento, data_rhemo = datos_rhemo,
                              otros = otros, image_ = x_image)]


#### CALLBACKS CONSULTAR INFORMACION

## reporte de alzadas

# criadero
@app.callback(Output('criadero_p3_ra', 'options'),
              Input('gerente_p3_ra', 'value'),
              State('user_info', 'data'))
def criaderora(gerente, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [{'label': 'Debe seleccionar un gerente', 'value': None}]
        sql = f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {gerente}'
        try:
            criaderos = get_data(sql)
        except Exception as e:
            print(e)
            return [{'label': 'Error al consultar criaderos', 'value': None}]
        if criaderos.empty:
            return [{'label': 'Sin registros', 'value': None}]
        else:
            criaderos.drop_duplicates(inplace=True)
            criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
            criaderos.reset_index(inplace = True, drop = True)
            return [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])]
    else:
        return no_update

# nombre equino p1
@app.callback(Output('equino_p3_ra', 'options'),
              [Input('criadero_p3_ra', 'value')],
             [State('user_info', 'data'),
              State('gerente_p3_ra', 'value')])
def nom_ra(criadero, data, gerente):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    nuevo = 'No'
    if rol == 'administrador':
        if gerente is None:
            return no_update
        if criadero is None:
            return no_update
        if nuevo == 'No':
            try:
                sql = f'''SELECT id_equino, nombre_equino FROM equinos WHERE id_gerente = {gerente} AND id_criadero = {criadero};'''
                equinos = get_data(sql)
            except Exception as e:
                print(e)
                return no_update
            if equinos.empty:
                equinos = pd.DataFrame({'id_equino': [None],
                                        'nombre_equino': ['Sin registros']})
            equinos.sort_values(by = ['nombre_equino'], inplace = True)
            equinos.drop_duplicates(inplace = True)
            equinos.reset_index(drop = True, inplace = True)
            options = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])]
            return options         

    elif rol == 'gerente':
        if criadero == None:
            return no_update
        if nuevo == 'No':
            try:
                sql = f'''SELECT id_equino, nombre_equino FROM equinos WHERE id_gerente = {doc_id} AND id_criadero = {criadero};'''
                equinos = get_data(sql)
            except Exception as e:
                print(e)
                return no_update
            if equinos.empty:
                equinos = pd.DataFrame({'id_equino': [None],
                                        'nombre_equino': ['Sin registros']})
            equinos.sort_values(by = ['nombre_equino'], inplace = True)
            equinos.drop_duplicates(inplace = True)
            equinos.reset_index(drop = True, inplace = True)
            options = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])]
            return options       

    elif rol == 'cliente':
        return no_update
        # if nuevo == 'No':
        #     try:
        #         sql = f'''SELECT id_equino, nombre_equino FROM equinos WHERE id_criadero = {doc_id};'''
        #         equinos = get_data(sql)
        #     except Exception as e:
        #         print(e)
        #         return no_update
        #     if equinos.empty:
        #         equinos = pd.DataFrame({'id_equino': [None],
        #                                 'nombre_equino': ['Sin registros']})
        #     equinos.sort_values(by = ['nombre_equino'], inplace = True)
        #     equinos.drop_duplicates(inplace = True)
        #     equinos.reset_index(drop = True, inplace = True)
        #     options = [{'label': equinos['nombre_equino'][i], 'value': equinos['id_equino'][i]} for i in range(equinos.shape[0])]
        #     campo = [dbc.FormGroup([
        #             dbc.Label(id = 'nombre_p1' + '_label', children = 'Nombre del equino'),
        #             dbc.Select(id = 'nombre_p1', 
        #                     options = options),
        #             dbc.FormText(id = 'nombre_p1' + '_ayuda', children = '-')
        #             ], style = {'padding-left': '5px'})]
        #     return campo         


# generar reporte alzadas 
@app.callback([Output(i, 'children') for i in ids_sal_p4] + [
               Output('salida_p3_ra', 'children'),
               Output('salida_p3_ra', 'color'),
               Output('salida_p3_ra', 'is_open'),
               Output('modal_ra', 'is_open'),
               Output('info_ra', 'data'),
               Output('info_ps_', 'data')],
              Input('generar_p3_ra', 'n_clicks'),
              [State(i, 'value') for i in ids_ra] + [State('user_info', 'data')])
def enviar_p4(n, gerente, criadero, nombre, espc, cont, obs, data):
    if n is None or n == 0:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]        
    fecha_ = datetime.today().date().strftime('%Y%m%d')
    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [no_update] * 7 + ['Gerente de zona no valido', 'warning', True, no_update, no_update, no_update]
        if criadero is None or criadero == '':
            return [no_update] * 7 + ['Criadero no valido', 'warning', True, no_update, no_update, no_update]
        if nombre is None or nombre == '':
            return [no_update] * 7 + ['Equino no valido', 'warning', True, no_update, no_update, no_update]
        sql = f'''SELECT * FROM seguimiento_alzadas 
            WHERE id_gerente = '{gerente}' 
            AND id_criadero = '{criadero}' 
            AND id_equino = '{nombre}'; '''
        sql_ps = f'''SELECT plan_sanitario.fecha_proxima_vacunacion, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.fecha_proxima_vacunacion >= 20210901 AND plan_sanitario.id_equino = {nombre} AND plan_sanitario.id_criadero = {criadero}; '''
    elif rol == 'gerente':
        if criadero is None or criadero == '':
            return [no_update] * 7 + ['Criadero no valido', 'warning', True, no_update, no_update, no_update]
        if nombre is None or nombre == '':
            return [no_update] * 7 + ['Equino no valido', 'warning', True, no_update, no_update, no_update]
        sql = f'''SELECT * FROM seguimiento_alzadas 
                    WHERE id_gerente = '{doc_id}' 
                    AND id_criadero = '{criadero}' 
                    AND id_equino = '{nombre}'; '''
        sql_ps = f'''SELECT plan_sanitario.fecha_proxima_vacunacion, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.fecha_proxima_vacunacion >= 20210901 AND plan_sanitario.id_equino = {nombre} AND plan_sanitario.id_criadero = {criadero}; '''
    elif rol == 'cliente':
        if criadero is None or criadero == '':
            return [no_update] * 7 + ['Criadero no valido', 'warning', True, no_update, no_update, no_update]
        if nombre is None or nombre == '':
            return [no_update] * 7 + ['Equino no valido', 'warning', True, no_update, no_update, no_update]
        sql = f'''SELECT * FROM seguimiento_alzadas WHERE id_criadero = '{doc_id}' AND id_equino = '{nombre}'; '''
        sql_ps = f'''SELECT plan_sanitario.fecha_proxima_vacunacion, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.fecha_proxima_vacunacion >= 20210901 AND plan_sanitario.id_equino = {nombre} AND plan_sanitario.id_criadero = {doc_id}; '''
    try:
        db_ = get_data(sql)
        plan_sanitario = get_data(sql_ps)
    except Exception as e:
        print(e)
        return [no_update] * 7 + ['Error al consultar la información', 'warning', True, no_update, no_update, no_update]

    db_ = db_.drop(['id', 'id_gerente', 'id_criadero', 'id_equino'], axis = 1)
    db_.columns = ['Fecha','Pais','Gerente de Zona','Departamento/Provincia','Municipio','Nombre Criadero',
                    'Nombre Equino','Raza','Planta de alimento','Referencia Alimento','Etapa Fisiológica',
                    'Edad (Meses)','Sexo','Andar','Peso (Kg)','Pesaje Anterior (Kg)','Días entre visitas',
                    'GPD (g)','Alzada (cm)','Referencia Alzada (cm)','Diferencia (cm)','Condicion Corporal',
                    'Calidad del Pelaje','Observaciones']
    etapa = db_['Etapa Fisiológica'].values[-1]
    if plan_sanitario.empty:
        plan_sanitario = pd.DataFrame({'Próxima vacunación': ['-'],
                                       'Criadero': [db_['Nombre Criadero'].values[0]], 
                                       'Equino': [db_['Nombre Equino'].values[0]], 
                                       'Tipo': ['-']})
    else:
        plan_sanitario.columns = ['Próxima vacunación', 'Criadero', 'Equino', 'Tipo']
    tb1 = salidas(dt = db_, criadero = db_['Nombre Criadero'].values[0], equino = db_['Nombre Equino'].values[0],
                    etapa = etapa, especialista = espc, contacto = cont, obs = obs,
                    pais = pais, tipo = 'tabla_1')

    tb2 = salidas(dt = db_, criadero = criadero, equino = nombre,
                    etapa = etapa, especialista = espc, contacto = cont, obs = obs,
                    pais = pais, tipo = 'tabla_2')
    gp1 = salidas(dt = db_, criadero = criadero, equino = nombre,
                    etapa = etapa, especialista = espc, contacto = cont, obs = obs,
                    pais = pais, tipo = 'fig_1')
    gp2 = salidas(dt = db_, criadero = criadero, equino = nombre,
                    etapa = etapa, especialista = espc, contacto = cont, obs = obs,
                    pais = pais, tipo = 'fig_2')
    tb3 = salidas(dt = db_, criadero = criadero, equino = nombre,
                    etapa = etapa, especialista = espc, contacto = cont, obs = obs,
                    pais = pais, tipo = 'tabla_3')
    tb4 = salidas(dt = db_, criadero = criadero, equino = nombre,
                    etapa = etapa, especialista = espc, contacto = cont, obs = obs,
                    pais = pais, tipo = 'tabla_4')
    return [[dcc.Graph(figure = tb1)], [dcc.Graph(figure = tb2)],
            [dcc.Graph(figure = gp1)], [dcc.Graph(figure = gp2)],
            [dcc.Graph(figure = tb3)], [dcc.Graph(figure = tb4)],
            [dbc.Table.from_dataframe(plan_sanitario, striped = True, bordered = True, hover = True)],
            'Reporte generado con éxito', 'success', True, True, db_.to_json(date_format = 'iso', orient = 'split'), plan_sanitario.to_json(date_format='iso', orient='split')]


# descargar reporte seguimiento alzadas
@app.callback([Output('download_p4_', 'data'),
               Output('download_p3_ra', 'children'),
               Output('download_p3_ra', 'is_open'),
               Output('download_p3_ra', 'color')],
              Input('descargar_p3_ra', 'n_clicks'),
              [State('info_ps_', 'data'), State('info_ra', 'data'), State('user_info', 'data')] + [State(i, 'value') for i in ids_ra])
def down_p4(n, data_ps, data_reporte, data, gerente, criadero, nombre, espc, cont, obs,):
    if n is None:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    pais = usuario['pais'].values[0]

    try:
        db_ = pd.read_json(data_reporte, orient = 'split')
        db_ps = pd.read_json(data_ps, orient = 'split')
        etapa = db_['Etapa Fisiológica'].values[-1]
    except Exception as e:
        print(e)
    
    return [pdf_report(data = db_, pais = pais, criadero = criadero,
                       equino = nombre, etapa = etapa, persona = espc, contacto = cont,
                       obs = obs, data_ps = db_ps),
            'Descargando reporte, por favor espere', True, 'success']
 
# criadero equinos
@app.callback(Output('criadero_p3_eq', 'options'),
              Input('gerente_p3_eq', 'value'),
              State('user_info', 'data'))
def criaderoeq(gerente, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [{'label': 'Debe seleccionar un gerente', 'value': None}]
        sql = f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {gerente}'
        try:
            criaderos = get_data(sql)
        except Exception as e:
            print(e)
            return [{'label': 'Error al consultar criaderos', 'value': None}]
        if criaderos.empty:
            return [{'label': 'Sin registros', 'value': None}]
        else:
            criaderos.drop_duplicates(inplace=True)
            criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
            criaderos.reset_index(inplace = True, drop = True)
            return [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])]
    else:
        return no_update

# ver equinos
@app.callback([Output('salida_p3_eq', 'children'),
               Output('salida_p3_eq', 'color'),
               Output('salida_p3_eq', 'is_open'),
               Output('modal_eq', 'is_open'),
               Output('modal_eq_c', 'children')],
               Input('generar_p3_eq', 'n_clicks'),
               [State('user_info', 'data')] + [State(i, 'value') for i in ids_eq])
def ver_equinos(n, data, gerente, criadero):
    if n is None or n == 0:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]        

    if rol == 'administrador':
        if gerente is None or gerente == '':
            return ['Gerente de zona no valido', 'warning', True, no_update, no_update]
        if criadero is None or criadero == '':
            return ['Criadero no valido', 'warning', True, no_update, no_update]            
        sql = f'''SELECT nombre_equino, raza, sexo, andar, departamento_provincia, municipio FROM equinos 
                  WHERE id_criadero = '{criadero}'; '''
    elif rol == 'gerente':
        if criadero is None or criadero == '':
            return ['Criadero no valido', 'warning', True, no_update, no_update]            
        sql = f'''SELECT nombre_equino, raza, sexo, andar, departamento_provincia, municipio FROM equinos 
                  WHERE id_criadero = '{criadero}'; '''          
    elif rol == 'cliente':
        if criadero is None or criadero == '':
            return ['Criadero no valido', 'warning', True, no_update, no_update]
        sql = f'''SELECT nombre_equino, raza, sexo, andar, departamento_provincia, municipio FROM equinos 
                  WHERE id_criadero = '{doc_id}'; '''
    try:
        db_ = get_data(sql)
        db_.columns = ['EQUINO', 'RAZA', 'SEXO', 'ANDAR', 'DEPARTAMENTO', 'MUNICIPIO']
    except Exception as e:
        print(e)
        return ['Error al consultar la información', 'warning', True, no_update, no_update]
    db_.drop_duplicates(inplace=True)
    db_.sort_values(by = ['EQUINO'], inplace = True)
    db_.reset_index(inplace = True, drop = True)
    if db_.empty:
        return ['Sin registros', 'warning', True, no_update, no_update]

    return ['Información cargada con éxito', 'success', True, True, render_table(db_)]


# criadero historico
@app.callback(Output('criadero_p3_ha', 'options'),
              Input('gerente_p3_ha', 'value'),
              State('user_info', 'data'))
def criaderoeq(gerente, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [{'label': 'Debe seleccionar un gerente', 'value': None}]
        sql = f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {gerente}'
        try:
            criaderos = get_data(sql)
        except Exception as e:
            print(e)
            return [{'label': 'Error al consultar criaderos', 'value': None}]
        if criaderos.empty:
            return [{'label': 'Sin registros', 'value': None}]
        else:
            criaderos.drop_duplicates(inplace=True)
            criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
            criaderos.reset_index(inplace = True, drop = True)
            return [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])]
    else:
        return no_update


# criadero plan sanitario
@app.callback(Output('criadero_p3_ps', 'options'),
              Input('gerente_p3_ps', 'value'),
              State('user_info', 'data'))
def criaderops(gerente, data):
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]
    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [{'label': 'Debe seleccionar un gerente', 'value': None}]
        sql = f'SELECT id_criadero, nombre_criadero FROM criaderos WHERE id_gerente = {gerente}'
        try:
            criaderos = get_data(sql)
        except Exception as e:
            print(e)
            return [{'label': 'Error al consultar criaderos', 'value': None}]
        if criaderos.empty:
            return [{'label': 'Sin registros', 'value': None}]
        else:
            criaderos.drop_duplicates(inplace=True)
            criaderos.sort_values(by = ['nombre_criadero'], inplace = True)
            criaderos.reset_index(inplace = True, drop = True)
            return [{'label': criaderos['nombre_criadero'][i], 'value': criaderos['id_criadero'][i]} for i in range(criaderos.shape[0])]
    else:
        return no_update

# año historico alzadas
@app.callback([Output('año_p3_ha', 'options'),
               Output('año_mes_ha', 'data')],
              Input('criadero_p3_ha', 'value'))
def año_ha(criadero):
    if criadero is None:
        return [[{'value': '-', 'label': 'Seleccione un criadero'}], no_update]

    sql = f'SELECT DISTINCT YEAR(fecha), MONTH(fecha) FROM seguimiento_alzadas WHERE id_criadero = {criadero}'
    try:
        db_fechas = get_data(sql)
    except Exception as e:
        print(e)
        return [[{'value': '-', 'label': 'Error al consultar'}], no_update]
    
    if db_fechas.empty:
        return [[{'value': '-', 'label': 'Sin registros'}], no_update]
    db_fechas.sort_values(by = ['YEAR(fecha)', 'MONTH(fecha)'], ascending = False, inplace = True)
    return [[{'value': i, 'label': i} for i in db_fechas['YEAR(fecha)'].unique()], db_fechas.to_json(date_format = 'iso', orient = 'split')]

# mes historico alzadas
@app.callback(Output('mes_p3_ha', 'options'),
              Input('año_p3_ha', 'value'),
              State('año_mes_ha', 'data'))
def mes_ha(año, data):
    if año is None or isinstance(año, str):
        return no_update
    data_fecha = pd.read_json(data, orient = 'split')
    meses = data_fecha.loc[data_fecha['YEAR(fecha)'].isin(año)].copy()
    meses.sort_values(by = ['MONTH(fecha)'], inplace = True)
    meses = meses['MONTH(fecha)']
    if meses.empty:
        return [{'label': 'Sin registros', 'value': '-'}]
    
    # agregar nombre del mes
    label_meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                   5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                   9: 'Septiembre', 10: 'Ocutubre', 11: 'Noviembre',
                   12: 'Diciembre'}


    return [{'label': label_meses[i], 'value': i} for i in meses.unique()]

    

# generar reporte historico alzadas 
@app.callback([Output('tabla_ha', 'children'),
               Output('salida_p3_ha', 'children'),
               Output('salida_p3_ha', 'color'),
               Output('salida_p3_ha', 'is_open'),
               Output('modal_ha', 'is_open'),
               Output('info_ha', 'data')],
              Input('generar_p3_ha', 'n_clicks'),
              [State(i, 'value') for i in ids_ha] + [State('user_info', 'data')])
def cargar_ha(n, gerente, criadero, año, mes, data):
    if n is None or n == 0:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]        

    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [no_update, 'Gerente de zona no valido', 'warning', True, no_update, no_update]
    if criadero is None or criadero == '':
        return [no_update, 'Criadero no valido', 'warning', True, no_update, no_update]            
    print(año)
    if año is None or isinstance(año, str) or len(año) == 0:
        return [no_update, 'Año de consulta no valido', 'warning', True, no_update, no_update]
    if mes is None or isinstance(mes, str) or len(mes) == 0:
        return [no_update, 'Mes de consulta no valido', 'warning', True, no_update, no_update]
    if rol == 'cliente':
        criadero = doc_id
    año_sql = '('
    for i in año:
        año_sql = año_sql + str(i)
        if int(i) == año[-1]:
            año_sql = año_sql + ')'
        else:
            año_sql = año_sql + ','
    mes_sql = '('
    for i in mes:
        mes_sql = mes_sql + str(i)
        if int(i) == mes[-1]:
            mes_sql = mes_sql + ')'
        else:
            mes_sql = mes_sql + ','

    sql = f'''SELECT * FROM seguimiento_alzadas 
        WHERE id_criadero = '{criadero}'
        AND YEAR(fecha) IN {año_sql}
        AND MONTH(fecha) IN {mes_sql}; '''
    
    try:
        db_ = get_data(sql)
    except Exception as e:
        print(e)
        return [no_update, 'Error al consultar la información', 'warning', True, no_update, no_update]
    if db_.empty:
        return [no_update, 'Sin registros', 'warning', True, no_update, no_update]

    db_ = db_.drop(['id', 'id_gerente', 'id_criadero', 'id_equino'], axis = 1)
    db_.columns = ['Fecha','Pais','Gerente de Zona','Departamento/Provincia','Municipio','Nombre Criadero',
                    'Nombre Equino','Raza','Planta de alimento','Referencia Alimento','Etapa Fisiológica',
                    'Edad (Meses)','Sexo','Andar','Peso (Kg)','Pesaje Anterior (Kg)','Días entre visitas',
                    'GPD (g)','Alzada (cm)','Referencia Alzada (cm)','Diferencia (cm)','Condicion Corporal',
                    'Calidad del Pelaje','Observaciones']
    t = dashtable(archivo = db_, tipo = 'historico')

    return [t, 'Información consultada con éxito', 'warning', True, True, db_.to_json(date_format = 'iso', orient = 'split')]



# generar reporte plan sanitario
@app.callback([Output('tabla_ps', 'children'),
               Output('salida_p3_ps', 'children'),
               Output('salida_p3_ps', 'color'),
               Output('salida_p3_ps', 'is_open'),
               Output('modal_ps', 'is_open'),
               Output('info_ps', 'data')],
              Input('generar_p3_ps', 'n_clicks'),
              [State(i, 'value') for i in ids_ps] + [State('user_info', 'data')])
def cargar_ps(n, gerente, criadero, data):
    if n is None or n == 0:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    rol = usuario['rol_usuario'].values[0]
    user = usuario['nombre'].values[0]
    doc_id = usuario['doc_id'].values[0]
    pais = usuario['pais'].values[0]        

    if rol == 'administrador':
        if gerente is None or gerente == '':
            return [no_update, 'Gerente de zona no valido', 'warning', True, no_update, no_update]
        if criadero is None or criadero == '':
            return [no_update, 'Criadero no valido', 'warning', True, no_update, no_update]            
        sql = f'''SELECT plan_sanitario.fecha, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo, plan_sanitario.aplica, plan_sanitario.fecha_vacunacion, plan_sanitario.fecha_proxima_vacunacion, plan_sanitario.observaciones  FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.id_criadero = '{criadero}'; '''
    elif rol == 'gerente':
        if criadero is None or criadero == '':
            return [no_update, 'Criadero no valido', 'warning', True, no_update, no_update]            
        if nombre is None or nombre == '':
            return [no_update, 'Equino no valido', 'warning', True, no_update, no_update]
        sql = f'''SELECT plan_sanitario.fecha, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo, plan_sanitario.aplica, plan_sanitario.fecha_vacunacion, plan_sanitario.fecha_proxima_vacunacion, plan_sanitario.observaciones  FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.id_criadero = '{criadero}'; '''         
    elif rol == 'cliente':
        if criadero is None or criadero == '':
            return [no_update, 'Criadero no valido', 'warning', True, no_update, no_update]
        if nombre is None or nombre == '':
            return [no_update, 'Equino no valido', 'warning', True, no_update, no_update]
        sql = f'''SELECT plan_sanitario.fecha, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo, plan_sanitario.aplica, plan_sanitario.fecha_vacunacion, plan_sanitario.fecha_proxima_vacunacion, plan_sanitario.observaciones  FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.id_criadero = '{doc_id}'; '''
    try:
        db_ = get_data(sql)
    except Exception as e:
        print(e)
        return [no_update, 'Error al consultar la información', 'warning', True, no_update, no_update]
    
    db_.columns = ['Fecha','Criadero','Equino','Tipo vacuna','Aplicada','Fecha vacunación',
                    'Fecha próxima vacunación','Observaciones']
    t = dbc.Table.from_dataframe(db_, striped = True, bordered = True, hover = True)

    return [t, 'Información consultada con éxito', 'success', True, True, db_.to_json(date_format = 'iso', orient = 'split')]



# descargar reporte plan sanitario
# @app.callback([Output('download_p3_ps', 'children'),
#                Output('download_p3_ps', 'color'),
#                Output('download_p3_ps', 'is_open'),
#                Output('download_ps', 'data')],
#                Input('descargar_p3_ps', 'n_clicks'),
#                [State('info_ps', 'data'),
#                 State('criadero_p3_ps', 'value')])
# def downloadps(n, data, criadero):
#     if n is None:
#         raise dash.exceptions.PreventUpdate()
#     try:
#         db = pd.read_json(data, orient = 'split')
#         db['Fecha'] = db['Fecha'].apply(lambda x: x.split('T')[0])
#         db['Fecha vacunación'] = db['Fecha vacunación'].apply(lambda x: x.split('T')[0])
#         db['Fecha próxima vacunación'] = db['Fecha próxima vacunación'].apply(lambda x: x.split('T')[0])

#     except Exception as e:
#         print(e)
#         return ['Ha ocurrido un error al descargar el archivo', 'warning', True, no_update]
    
#     return ['Descargando archivo', 'success', True, downloadExcel(db, f'Plan sanitario {criadero}.xlsx')]


# descargar reporte historico alzadas
@app.callback([Output('download_p3_ha', 'children'),
               Output('download_p3_ha', 'color'),
               Output('download_p3_ha', 'is_open'),
               Output('download_ha', 'data')],
               Input('descargar_p3_ha', 'n_clicks'),
               [State('info_ha', 'data'),
                State('criadero_p3_ha', 'value')])
def downloadHA(n, data, criadero):
    if n is None:
        raise dash.exceptions.PreventUpdate()
    try:
        db = pd.read_json(data, orient = 'split')
        db['Fecha'] = db['Fecha'].apply(lambda x: x.split('T')[0])
    except Exception as e:
        print(e)
        return ['Ha ocurrido un error al descargar el archivo', 'warning', True, no_update]
    
    return ['Descargando archivo', 'success', True, downloadExcel(db, f'Reporte alzadas {criadero}.xlsx')]


################


# cargar tabla mis granjas no cliente
@app.callback([Output('alert_cargar_mis_granjas_nc', 'children'),
               Output('alert_cargar_mis_granjas_nc', 'color'),
               Output('alert_cargar_mis_granjas_nc', 'is_open'),
               Output('modal_criaderos_c', 'children'),
               Output('modal_criaderos', 'is_open')],
               Input('cargar_mis_granjas_nc', 'n_clicks'),
               [State('user_info', 'data'),
                State('gerente_ver_granjas_nc', 'value')])
def cargarMisgranjas(n, data, gerente):
    if n is None:
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    doc_id = usuario['doc_id'].values[0]

    if gerente is None or len(gerente) < 1:
        return ['Gerente de zona no valido', 'warning', True, None, no_update]
    
    gerente_sql = '('
    for i in gerente:
        gerente_sql = gerente_sql + str(i)
        if int(i) == gerente[-1]:
            gerente_sql = gerente_sql + ')'
        else:
            gerente_sql = gerente_sql + ','
    try:
        data = get_data(f'''SELECT criaderos.nombre_criadero, gerentes.nombre_gerente, criaderos.departamento_provincia, criaderos.municipio FROM criaderos INNER JOIN gerentes ON criaderos.id_gerente = gerentes.doc_id WHERE id_gerente IN {gerente_sql};''')
        data.columns = ['CRIADERO', 'GERENTE', 'DEPARTAMENTO', 'MUNICIPIO']
        data.drop_duplicates(inplace=True)
        data.sort_values(by = ['CRIADERO'], inplace = True)
        data.reset_index(inplace = True, drop = True)
        return ['Información cargada con éxito', 'success', True, render_table(data), True]
    except Exception as e:
        print(e)
        return ['Error al cargar la información', 'success', True, None, no_update]



#crear tabla gerentes
@app.callback([Output('alert_ver_gerentes', 'children'),
               Output('alert_ver_gerentes', 'color'),
               Output('alert_ver_gerentes', 'is_open'),
               Output('modal_gerentes_c', 'children'),
               Output('modal_gerentes', 'is_open')],
               Input('ver_gerentes', 'n_clicks'))
def cargarTablaGerentes(n):
    if n is None:
        raise dash.exceptions.PreventUpdate()
    try:
        gerentes = get_data('SELECT * FROM gerentes').drop('creador', axis = 1)
        gerentes.columns = pd.Index(['DOCUMENTO', 'GERENTE', 'ZONA', 'PAIS'], dtype='object')
        return ['Información cargada con éxito', 'success', True, render_table(gerentes.sort_values(axis = 0, by = 'GERENTE')), True]
    except Exception as e:
        print(e)
        return ['Error al cargar la información', 'warning', True, None, no_update]

# crear granja, seleccion cliente cuando ingresa un gerente
# @app.callback(Output('nit_clientes_nc', 'options'),
#               Input('gerente_nc', 'value'),
#               State('user_info', 'data'))
# def clientesCrearGranja(gerente, data):
#     usuario = pd.read_json(data, orient = 'split')
#     rol_usuario = usuario['rol_usuario'].values[0]
#     if gerente is None:
#         raise dash.exceptions.PreventUpdate()
#     if rol_usuario == 'cliente':
#         raise dash.exceptions.PreventUpdate()
#     elif rol_usuario == 'gerente':
#         gerente = usuario['nombre'].values[0]
#         clientes = get_data(f'''SELECT nit FROM clientes WHERE gerente_zona = '{gerente}';''')
#         return [{'label': i, 'value': i} for i in clientes['nit']]
#     elif rol_usuario == 'administrador':
#         clientes = get_data(f'''SELECT nit FROM clientes WHERE gerente_zona = '{gerente}';''')
#         return [{'label': i, 'value': i} for i in clientes['nit']]


# crea criadero
@app.callback([Output('alert_crear_granja_nc', 'children'),
               Output('alert_crear_granja_nc', 'color'),
               Output('alert_crear_granja_nc', 'is_open'),
               Output('gerente_nc', 'value'),
               Output('nombre_clientes', 'value'),
               Output('depto_granja', 'value'),
               Output('usuario_cliente', 'value'),
               Output('pw_cliente', 'value')],
               Input('confirm_crear_granja_no_cliente', 'submit_n_clicks'),
               [State('user_info', 'data')] + [State(i, 'value') for i in ids_granjas_nc])
def crearGranjaNoCliente(n, data, gerente, cliente, depto, municipio, n_usuario, pw):
    if n is None: 
        raise dash.exceptions.PreventUpdate()
    usuario = pd.read_json(data, orient = 'split')
    rol_usuario = usuario['rol_usuario'].values[0]
    doc_id = usuario['doc_id'].values[0]
    user = usuario['nombre'].values[0]
    nit = randint(9999,99999)
    if rol_usuario == 'gerente':
        pais = usuario['pais'].values[0]
    else:
        try:
            pais = get_data(f'SELECT pais FROM gerentes WHERE doc_id = {gerente}')['pais'].values[0]
        except Exception as e:
            print(e)
            pais = 'NA'

    divipola = pd.read_csv('Datos/Divipola.csv')
    if n is None:
        raise dash.exceptions.PreventUpdate()
    if gerente is None:
        return ['Gerente de zona no valido', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    if cliente is None or cliente == '' or len(cliente) <= 1:
        return ['Nombre de criadero no valido', 'warning', True, gerente, cliente, depto, n_usuario, pw]

    # granjas = get_data(f"SELECT nombre_granja FROM granjas WHERE nit_cliente = '{nit}'")
    # if False if granjas.shape[0] == 0 else granja in granjas['nombre_granja'].values:
    #     return ['Nombre de granja ya registrada', 'warning', True, gerente, nit, ]
    if depto is None or len(depto) < 1:
        return ['Departamento/Provincia no valido', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    if municipio is None or len(municipio) < 1:
        return ['Municipio no valido', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    verificacion = list(range(len(depto)))
    for deptos in range(len(depto)):
        dt_dvp = divipola.loc[divipola['Departamento'] == depto[deptos]]['Municipio']
        verificacion[deptos] = dt_dvp.isin(municipio).sum()
    if not all(verificacion):
        return ['Debe seleccionar por lo menos 1 municipio para cada departamento', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    # if isinstance(altitud, str) or altitud is None or altitud < 0:
    #     return ['Altitud no valida', 'warning', True, gerente, nit]
    if n_usuario is None or n_usuario == '' or len(n_usuario.split()) != 1:
        return ['Nombre de usuario no valido', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    datos_usuario = get_data('SELECT usuario_, doc_id FROM usuarios')
    if n_usuario in datos_usuario['usuario_'].values:
        return ['Nombre de usuario ya registrado', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    if pw is None or pw == '' or len(pw) < 8:
        return ['Contraseña de ingreso no valida, recuerde que debe contar con al menos 8 caracteres', 'warning', True,
                gerente, cliente, depto, n_usuario, pw]
    if  nit in datos_usuario['doc_id'].values:
        return ['Por favor intente nuevamente', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    data = pd.DataFrame()
    fecha = datetime.today().date()
    for i in range(len(municipio)):
        depto = divipola.loc[divipola['Municipio'] == municipio[i], 'Departamento']
        data = data.append({'fecha': datetime.strftime(fecha, '%Y-%m-%d'),
                            'id_criadero': nit,
                            'nombre_criadero': cliente.title(),
                            'departamento_provincia': depto.values[0],
                            'municipio': municipio[i],
                            'id_gerente': gerente,
                            'pais': pais,
                            }, ignore_index=True)
    data = data[['fecha', 'id_criadero', 'nombre_criadero', 'departamento_provincia', 'municipio', 'id_gerente', 'pais']]
    try:
        crear_usuario(usuario = n_usuario, rol = 'cliente', doc_id = nit, pais = pais, nombre = cliente.title(), pw = pw,)
    except Exception as e:
        print(e)
        return ['Error al crear el usuario, por favor intente mas tarde', 'warning', True, gerente, cliente, depto, n_usuario, pw]
    try:
        insert_dataframe(data, 'criaderos')
        return ['Criadero creado con éxito', 'success', True, None, None, None, None, None]
    except Exception as e:
        print(e)
        return ['Error al crear el criadero, por favor intente mas tarde', 'warning', True, gerente, cliente, depto, n_usuario, pw]


# crear gerente
@app.callback([Output('alert_crear_gerente', 'children'),
               Output('alert_crear_gerente', 'color'),
               Output('alert_crear_gerente', 'is_open'),
               Output('documento_gerente', 'value'),
               Output('nombre_gerente', 'value'),
               Output('pais_gerente', 'value'),
               Output('zona_gerente', 'value'),
               Output('usuario_gerente', 'value'),
               Output('pw_gerente', 'value')], 
              Input('confirm_crear_gerente', 'submit_n_clicks'),
              [State('user_info', 'data')] + [State(i, 'value') for i in ids_crear_gerente])
def creargerente(n, data, documento, nombre, pais, zona, usuario, pw):
    if n is None:
        raise dash.exceptions.PreventUpdate()
    user = pd.read_json(data, orient = 'split')
    doc_id = user['doc_id'].values[0]
    if isinstance(documento, str) or documento is None:
        return ['Documento no valido', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    documentos = get_data('SELECT doc_id FROM gerentes')
    if False if documentos.shape[0] == 0 else documento in documentos['doc_id'].values:
        return ['Documento de identidad ya registrado', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    if nombre is None or nombre == '':
        return ['Nombre del Gerente no valido', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    if len(nombre.split()) < 2:
        return ['Por favor ingrese nombre y apellido del gerente', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    if zona is None or zona == '':
        return ['Zona no valida', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    if usuario is None or usuario == '' or len(usuario.split()) != 1:
        return ['Nombre de usuario no valido', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    if usuario in get_data('SELECT usuario_ FROM usuarios')['usuario_'].values:
        return ['Nombre de usuario ya registrado', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    if pw is None or pw == '' or len(pw) < 8:
        return ['Contraseña de usuario no valida, recuerde que debe contar con al menos 8 caracteres', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    
    try:
        crear_usuario(usuario = usuario, rol = 'gerente', doc_id = documento, nombre = nombre, pw = pw, pais = pais)
        crear_gerente(nombre = nombre, documento = documento, zona = zona, pais = pais, creador = user['nombre'].values[0])
        return ['Gerente creado con éxito', 'success', True, None, None, None, None, None, None]
    except Exception as e:
        print(e)
        return ['Gerente no creado, por favor intente mas tarde', 'warning', True, documento, nombre, pais, zona, usuario, pw]
    

## municipios en funcion de depto
@app.callback([Output('municipio_granja', 'options')],
              Input('depto_granja', 'value'))
def mun_depto(depto):
    if depto is None:
        return [[{'label': i, 'value': i} for i in ['-']]]
    divipola = pd.read_csv('Datos/Divipola.csv')
    municipios = divipola[divipola['Departamento'].isin(depto)]['Municipio']

    return [[{'label': i, 'value': i} for i in municipios.sort_values()]]




## collapsible historicos alzadas
@app.callback(Output('collapse_reporte_equinos', 'is_open'),
              Input('collapse_button_equinos', 'n_clicks'),
              State('collapse_reporte_equinos', 'is_open'))
def collapsepw(n, is_open):
    if n:
        return not is_open
    return is_open

## collapsible historicos alzadas
@app.callback(Output('collapse_reporte_historicos', 'is_open'),
              Input('collapse_button_historicos', 'n_clicks'),
              State('collapse_reporte_historicos', 'is_open'))
def collapsepw(n, is_open):
    if n:
        return not is_open
    return is_open


## collapsible plan sanitario
@app.callback([Output('collapse_ps', 'is_open'),
               Output('alerta_ps', 'children'),
               Output('alerta_ps', 'is_open')],
              Input('collapse_button_ps', 'n_clicks'),
              [State('collapse_ps', 'is_open'),
               State('user_info', 'data')])
def collapseps(n, is_open, data):
    fecha = datetime.today().date().strftime('%Y%m%d')
    user = pd.read_json(data, orient = 'split')
    rol = user['rol_usuario'].values[0]
    doc_id = user['doc_id'].values[0]
    if is_open == False or is_open is None:
        if rol == 'administrador':
            sql = f'''SELECT plan_sanitario.fecha_proxima_vacunacion, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.fecha_proxima_vacunacion >= {fecha}; '''
        elif rol == 'gerente':
            sql = f'''SELECT plan_sanitario.fecha_proxima_vacunacion, criaderos.nombre_criadero, criaderos.id_gerente, equinos.nombre_equino, plan_sanitario.tipo FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.fecha_proxima_vacunacion >= {fecha} AND criaderos.id_gerente = {doc_id}; '''
        elif rol == 'cliente':
            sql = f'''SELECT plan_sanitario.fecha_proxima_vacunacion, criaderos.nombre_criadero, equinos.nombre_equino, plan_sanitario.tipo FROM plan_sanitario INNER JOIN criaderos ON plan_sanitario.id_criadero = criaderos.id_criadero INNER JOIN equinos ON plan_sanitario.id_equino = equinos.id_equino WHERE plan_sanitario.fecha_proxima_vacunacion >= {fecha} AND plan_sanitario.id_criadero = {doc_id}; '''
        try:
            plan_s = get_data(sql)
        except Exception as e:
            print(e)
            plan_s = pd.DataFrame({'Próxima vacunación': ['Error'],
                                'Criadero': ['al'], 'Equino': ['Consultar'], 'Tipo': ['']})
        if rol == 'gerente':
            print(plan_s.columns)
            plan_s = plan_s.drop(columns = ['id_gerente'])
        if plan_s.empty:
            plan_s = pd.DataFrame({'Próxima vacunación': ['Sin'],
                                'Criadero': ['Registros'], 'Equino': ['-'], 'Tipo': ['-']})
        else: 
            plan_s.columns = ['Próxima vacunación', 'Criadero', 'Equino', 'Tipo']

    else:
        plan_s = pd.DataFrame({'Próxima vacunación': [''],
                               'Criadero': [''], 'Equino': [''], 'Tipo': ['']})
    if n:
        return [not is_open, dbc.Table.from_dataframe(plan_s, striped = True, bordered = True, hover = True), True]
    return [is_open, dbc.Table.from_dataframe(plan_s, striped = True, bordered = True, hover = True), True]

## collapsible reporte alzadas_
@app.callback(Output('collapse_reporte_sa', 'is_open'),
              Input('collapse_button_reporte_sa', 'n_clicks'),
              State('collapse_reporte_sa', 'is_open'))
def collapsepw(n, is_open):
    if n:
        return not is_open
    return is_open

## collapsible pw
@app.callback(Output('collapse_pw', 'is_open'),
              Input('collapse_button_pw', 'n_clicks'),
              State('collapse_pw', 'is_open'))
def collapsepw(n, is_open):
    if n:
        return not is_open
    return is_open


## collapsible crear cliente
@app.callback(Output('collapse_crear_cliente', 'is_open'),
              Input('callapse_button_crear_cliente', 'n_clicks'),
              State('collapse_crear_cliente', 'is_open'))
def collapseceearcliente(n, is_open):
    if n:
        return not is_open
    return is_open

## collapsible crear gerente
@app.callback(Output('collapse_crear_gerente', 'is_open'),
              Input('callapse_button_crear_gerente', 'n_clicks'),
              State('collapse_crear_gerente', 'is_open'))
def collapsecreargerente(n, is_open):
    if n:
        return not is_open
    return is_open

## collapsible ver gerentes
@app.callback(Output('collapse_ver_gerentes', 'is_open'),
              Input('callapse_button_ver_gerentes', 'n_clicks'),
              State('collapse_ver_gerentes', 'is_open'))
def collapsecreargerente(n, is_open):
    if n:
        return not is_open
    return is_open

## collapsible mis granja
@app.callback(Output('collapse_mis_granjas', 'is_open'),
              Input('callapse_button_mis_granjas', 'n_clicks'),
              State('collapse_mis_granjas', 'is_open'))
def collapsecreargerente(n, is_open):
    if n:
        return not is_open
    return is_open

## collapsible crear granja
@app.callback(Output('collapse_crear_granja', 'is_open'),
              Input('callapse_button_crear_granja', 'n_clicks'),
              State('collapse_crear_granja', 'is_open'))
def collapsecreargerente(n, is_open):
    if n:
        return not is_open
    return is_open


## cambiar constraseña
@app.callback([Output('alert_pw', 'children'),
               Output('alert_pw', 'color'),
               Output('alert_pw', 'is_open')],
              Input('confirm_pw', 'submit_n_clicks'),
              [State('old_pw', 'value'),
               State('new_pw', 'value'),
               State('user_info', 'data')])
def cambio_contraseña(n, old, new, data):
    usuario = pd.read_json(data, orient = 'split')
    if n is None:
        raise dash.exceptions.PreventUpdate()
    if old is None or old == '' :
        return ['Contraseña actual en blanco, por favor verifique', 'danger', True]
    if old is None or old == '' or new is None or new == '':
        return ['Contraseña nueva en blanco, por favor verifique', 'danger', True]
    if len(new) < 8:
        return ['Recuerde que la contraseña debe contar con 8 caracteres como mínimo', 'danger', True]
    if old != get_data(f"SELECT contraseña FROM usuarios WHERE usuario_ = '{usuario['usuario_'].values[0]}'")['contraseña'].values[0]:
        return ['Contraseña actual no coincide, por favor verifique', 'danger', True]
    try:
        change_pw(new_pw = new, user = usuario['usuario_'].values[0])
        return ['Contraseña restablecida con éxito', 'success', True]
    except:
        return ['Error al cambiar la contraseña', 'danger', True]



###############################################################################
# run app
###############################################################################

if __name__ == "__main__":

    app.server.run(
        debug=True,
        host='0.0.0.0',
        port = port
    )
