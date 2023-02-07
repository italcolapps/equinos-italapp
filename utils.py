import dash_bootstrap_components as dbc
import dash_html_components as html
import os
from Datos.db import get_data
import pandas as pd
from numpy import nan
from datetime import datetime
import dash_table
from dash_extensions.snippets import send_file
from dash import no_update
import tempfile
import base64

def downloadExcel(data, archivo):
    if isinstance(data, pd.DataFrame):
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                data.to_excel(os.path.join(tmpdir, archivo), index = False)
                return send_file(os.path.join(tmpdir, archivo))
            except Exception as e:
                print(e)
                return no_update
    else:
        return no_update

def get_granjas(nit):
    data = get_data(f'''SELECT DISTINCT nombre_granja FROM granjas WHERE nit_cliente = '{nit}';''')
    if data.shape[0] == 0:
        return ['-']
    return data['nombre_granja'].values

def titulo(texto, id_, xl = 7, lg = 7, md = 7, sm = 7, xs = 7):
    return dbc.Row(children = [
                dbc.Col([
                    html.H5(texto, id = id_)
                ], xl = xl, lg = lg, md = md, sm = sm, xs = xs)
            ])

def save_file(name, content, nombre, UPLOAD_DIRECTORY):
    """Decode and store a file uploaded with Plotly Dash."""

    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, nombre), "wb") as fp:
        fp.write(base64.decodebytes(data))

def crearTablaIngreso(tabla, filas):
    if tabla is None or filas is None:
        return None
    if isinstance(filas, str) or filas is None or filas < 1:
        return 'Número de granjas no aceptado'
    if tabla == 'granjas':
        head = ['Nº', 'NOMBRE DE LA GRANJA', 'DEPARTAMENTO/PROVINCIA', 'MUNICIPIO', 'ALTITUD msnm']
        return dbc.Table([
            html.Thead(html.Tr([html.Th(label) for label in head]))
        ] + [
            html.Tbody([
                html.Tr([html.Td(str(row+1))] + [
                    html.Td(dbc.Input(type = 'text', id = f"{head[col]}_{row}", debounce = True, value = None))
                 for col in range(1, len(head) - 1)] + [html.Td(dbc.Input(value = None, type = 'number', id = f"{head[3]}_{row}"))]) # Tr
            for row in range(filas)]) # tbody
        ]) # dbc table
    if tabla == 'galpones':
        head = ['Nº', 'NOMBRE DEL GALPÓN', 'TEMPERATURA ºC', 'HUMEDAD RELATIVA %', 'TIPO GALPÓN', 'TIPO COMEDERO', 'TIPO BEBEDERO']
        return dbc.Table([
            html.Thead(html.Tr([html.Th(label) for label in head]))
        ] + [
            html.Tbody([
                html.Tr([html.Td(str(row+1))] + [html.Td(dbc.Input(type = 'text', id = f"{head[1]}_{row}", debounce = True, value = None))] + 
                [html.Td(dbc.Input(value = None, type = 'number', id = f"{head[col]}_{row}")) for col in range(2, 4)] + 
                [html.Td(dbc.Select(id = f"{head[4]}_{row}", options = [{'label': i, 'value': i} for i in ['ABIERTO', 'AMBIENTE CONTROLADO']])), 
                html.Td(dbc.Select(id = f"{head[5]}_{row}", options = [{'label': i, 'value': i} for i in ['AUTOMÁTICO', 'MANUAL']])), 
                html.Td(dbc.Select(id = f"{head[6]}_{row}", options = [{'label': i, 'value': i} for i in ['CAMPANA', 'NIPLE']]))]) # Tr
            for row in range(filas)]) # tbody
        ]) # dbc table
    else:
        return 'Tabla no definida'

def cargarDatosTablaIngreso(tabla, datos, filas):
    if tabla == 'granjas':
        columnas = range(1,5)
        values = {}
        for r in range(filas):
            value = []
            for c in columnas:
                try:
                    if c == 4:
                        value.append(datos['props']['children'][1]['props']['children'][r]['props']['children'][c]['props']['children']['props']['value'])
                    else:
                        value.append(datos['props']['children'][1]['props']['children'][r]['props']['children'][c]['props']['children']['props']['value'].upper())
                except Exception as e:
                    print(e)
                    return 'Tabla sin datos'
            values[r] = value
        return values

    if tabla == 'galpones':
        columnas = range(1,7)
        values = {}
        for r in range(filas):
            value = []
            for c in columnas:
                try:
                    if c == 1:
                        value.append(datos['props']['children'][1]['props']['children'][r]['props']['children'][c]['props']['children']['props']['value'].upper())
                    else:
                        value.append(datos['props']['children'][1]['props']['children'][r]['props']['children'][c]['props']['children']['props']['value'])
                except Exception as e:
                    print(e)
                    return 'Tabla sin datos'
            values[r] = value
        return values

 # validar datos de la tabla de ingreso

def validarTablaIngreso(data, tabla):
    if tabla == 'granjas':
        cols = ['NOMBRE DE LA GRANJA', 'DEPARTAMENTO/PROVINCIA', 'MUNICIPIO', 'ALTITUD msnm']
        for row in data:
            count = -1
            for column in data[row]:
                count += 1
                if count == 3:
                    if isinstance(column, str) or column is None or column <= 0:
                        return f"Granja Nº  {row + 1}: {cols[count]} no valido."
                else:
                    if column is None or column == '':
                        return f"Granja Nº  {row + 1}: {cols[count]} no valido."
                            
        #return type(data[1][1])
        return 'ok'

    if tabla == 'galpones':
        cols = ['NOMBRE DEL GALPÓN', 'TEMPERATURA ºC', 'HUMEDAD RELATIVA %', 'TIPO GALPÓN', 'TIPO COMEDERO', 'TIPO BEBEDERO']
        for row in data:
            count = -1
            for column in data[row]:
                count += 1
                if count == 0:
                    if column == '':
                        return f"Galpón Nº  {row + 1}: {cols[count]} no valido."
                if count in [1, 2]:
                    if isinstance(column, str) or column is None or column <= 0:
                        return f"Galpón Nº  {row + 1}: {cols[count]} no valido."
                else:
                    if column is None:
                        return f"Galpón Nº  {row + 1}: {cols[count]} no valido."
                            
        #return type(data[1][1])
        return 'ok'
    else:
        return 'Tabla no definida'

def seguimientoSemanal(fecha, gerente_zona, cliente, tipo_cliente, depto_prov, municipio,
                       planta_alimento, granja, lote, galpon, linea, sexo, aves_encasetadas,
                       incubadora, marca_alimento, peso_1_dia, edad, peso_7_dia, consumo,
                       peso_cierre, mortalidad, seleccion, observaciones):
    date = datetime.strptime(fecha, '%Y-%m-%d').date()
    data = pd.DataFrame()
    data['fecha'] = [fecha]
    data['año'] = [date.year]
    data['mes'] = [date.month]
    data['semana_año'] = [date.isocalendar()[1]]
    data['gerente_zona'] = [gerente_zona.upper()]
    data['nit_cliente'] = [cliente]
    data['tipo_cliente'] = [tipo_cliente]
    data['departamento_provincia'] = [depto_prov.upper()]
    data['municipio'] = [municipio.upper()]
    data['planta_alimento'] = [planta_alimento]
    data['granja'] = [granja]
    data['lote'] = [lote]
    data['galpon'] = [galpon]
    data['linea'] = [linea]
    data['sexo'] = [sexo]
    data['aves_encasetadas'] = [aves_encasetadas]
    data['incubadora'] = [incubadora]
    data['marca_alimento'] = [marca_alimento]
    data['peso_pollito_1_dia_g'] = [peso_1_dia]
    data['peso_pollito_1_dia_ref_g'] = [referencias(tipo = 'SS', sexo = sexo, edad = 0, linea = linea, var = 'PESO REFERENCIA (g/ave)')]
    data['diferencial_peso_pollito_1_dia_%'] = [100*(peso_1_dia-data['peso_pollito_1_dia_ref_g'].values[0])/data['peso_pollito_1_dia_ref_g'].values[0]]
    data['edad_dias'] = [edad]
    data['peso_dia_7'] = [peso_7_dia]
    data['consumo_acumulado_g_ave'] = [consumo]
    data['consumo_acumulado_ref_g_ave'] = [referencias(tipo = 'SS', sexo = sexo, edad = edad, linea = linea, var = 'CONSUMO ACUMULADO REFERENCIA (g/ave)')]
    data['diferencial_consumo_acumulado_%'] = [100*(consumo-data['consumo_acumulado_ref_g_ave'].values[0])/data['consumo_acumulado_ref_g_ave'].values[0]]
    data['peso_promedio_cierre_semana_g_ave'] = [peso_cierre]
    data['peso_cierre_semana_ref_g_ave'] = [referencias(tipo = 'SS', sexo = sexo, edad = edad, linea = linea, var = 'PESO REFERENCIA (g/ave)')]
    data['diferencia_peso_cierre_semana_%'] = [100*(peso_cierre - data['peso_cierre_semana_ref_g_ave'].values[0])/data['peso_cierre_semana_ref_g_ave'].values[0]]
    data['conversion_alimenticia'] = [consumo/peso_cierre]
    data['conversion_alimenticia_ref'] = [referencias(tipo = 'SS', sexo = sexo, edad = edad, linea = linea, var = 'CONVERSION ALIMENTICIA REFERENCIA')]
    data['diferencia_conversion_alimenticia_%'] = [100*(data['conversion_alimenticia'].values[0] - data['conversion_alimenticia_ref'].values[0])/data['conversion_alimenticia_ref'].values[0]]
    data['vpi_dia_7'] = [peso_7_dia/peso_1_dia]
    data['vpi_dia_7_ref'] = [referencias(tipo = 'SS', sexo = sexo, edad = 0, linea = linea, var = 'VPI SEMANA')]
    data['diferencial_vpi_dia_7_%'] = [100*(data['vpi_dia_7'].values[0] - data['vpi_dia_7_ref'].values[0])/data['vpi_dia_7_ref'].values[0]]
    data['ganacia_diaria_g_dia'] = [peso_cierre/edad]
    data['ganancia_diaria_ref_g_dia'] = [referencias(tipo = 'SS', sexo = sexo, edad = edad, linea = linea, var = 'GANANCIA/ DIARIA DE REFERENCIA (g/día)')]
    data['diferencia_ganancia_diaria_%'] = [100*(data['ganacia_diaria_g_dia'].values[0] - data['ganancia_diaria_ref_g_dia'].values[0])/data['ganancia_diaria_ref_g_dia'].values[0]]
    data['seleccion_acumulada_aves'] = [seleccion]
    data['mortalidad_acumulada_aves'] = [mortalidad]
    data['seleccion_acumulada_%'] = [100*(seleccion/aves_encasetadas)]
    data['mortalidad_acumulada_%'] = [100*(mortalidad/aves_encasetadas)]
    data['mortalidad_seleccion_acumulada_%'] = [data['seleccion_acumulada_%'].values[0] + data['mortalidad_acumulada_%'].values[0]]
    data['observaciones_generales'] = [observaciones]
    data = data.round(decimals = 2, )
    data.fillna(value=nan, inplace = True)
    return data

def liquidaciones(fecha, gerente, cliente, depto, municipio, planta, granja,
                  lote, galpon, linea, sexo, marca, aves_encasetadas, aves_muertas,
                  aves_sacrificadas, aves_decomisadas, peso_total, edad, consumo,
                  precio_promedio, divisa, observaciones):
    date = datetime.strptime(fecha, '%Y-%m-%d').date()                  
    data = pd.DataFrame()
    data['fecha'] = [fecha]
    data['año'] = [date.year]
    data['divisa'] = [divisa]
    data['gerente_zona'] = [gerente.upper()]
    data['nit_cliente'] = [cliente]
    data['departamento_provincia'] = [depto.upper()]
    data['municipio'] = [municipio.upper()]
    data['planta_alimento'] = [planta]
    data['granja'] = [granja]
    data['lote'] = [lote]
    data['galpon'] = [galpon]
    data['linea'] = [linea]
    data['sexo'] = [sexo]
    data['marca_alimento']  = [marca]
    data['aves_encasetadas'] = [aves_encasetadas]
    data['aves_muertas_granja'] = [aves_muertas]
    data['aves_sacrificadas_o_vendidas'] = [aves_sacrificadas]
    data['aves_decomisadas'] = [aves_decomisadas]
    data['decomisos_%'] = [100*(aves_decomisadas/aves_sacrificadas)]
    data['sobrantes_faltantes'] = [aves_encasetadas - aves_muertas - aves_sacrificadas]
    data['precio_promedio_kg_alimento'] = [precio_promedio]
    data['edad_sacrificio_dias'] = [edad]
    data['edad_sacrificio_ref_dias'] = [referencias(tipo = 'LIQ', sexo = sexo, linea = linea, var = 'EDAD', peso_promedio= (peso_total/aves_sacrificadas))]
    data['consumo_total_alimento_kg'] = [consumo]
    data['peso_total_aves_sacrificadas_kg'] = [peso_total]
    data['conversion_alimenticia'] = [consumo/peso_total]
    data['conversion_alimenticia_ref'] = [referencias(tipo = 'LIQ', sexo = sexo, linea = linea, peso_promedio=(peso_total/aves_sacrificadas), var = 'CONVERSION ALIMENTICIA REFERENCIA')]
    data['peso_promedio_ave_kg'] = [peso_total/aves_sacrificadas]
    data['ganancia_diaria_g_ave_dia'] = [100*(peso_total/aves_sacrificadas)/edad]
    data['mortalidad_total_%'] = [100*(1 - (aves_sacrificadas/aves_encasetadas))]
    data['mortalidad_total_ref_%'] = [referencias(tipo = 'MORT_LIQ', edad = edad)]
    data['costo_alimentacion_kg_pollo_producido'] = [(consumo*precio_promedio)/peso_total]
    data['eficiencia_americana'] = [100*(peso_total/aves_sacrificadas)/data['conversion_alimenticia'].values[0]]
    data['eficiencia_americana_ref'] = [referencias(tipo = 'LIQ', sexo = sexo, linea = linea, peso_promedio=(peso_total/aves_sacrificadas), var = 'EA')]
    data['eficiencia_europea'] = [((100-data['mortalidad_total_%'].values[0]/100)/100)*((data['peso_promedio_ave_kg'].values[0]*1000)*10/(edad*data['conversion_alimenticia'].values[0]))]
    data['eficiencia_europea_ref'] = [referencias(tipo = 'LIQ', sexo = sexo, linea = linea, peso_promedio=(peso_total/aves_sacrificadas), var = 'FEE')]
    data['ip'] = [data['eficiencia_americana'].values[0]/data['conversion_alimenticia'].values[0]]
    data['ip_ref'] = [referencias(tipo = 'LIQ', sexo = sexo, linea = linea, peso_promedio=(peso_total/aves_sacrificadas), var = 'IP')]
    data['observaciones'] = [observaciones]
    data = data.round(decimals = 2, )
    data.fillna(value=nan, inplace = True)
    return data

def referencias(sexo = None, linea = None, var = None, edad = None, peso_promedio = None, tipo = None):
    if tipo is None:
        return None
        # SS > segumiento semanal
    if tipo == 'SS':
        df = pd.read_csv('Datos/df_ref_prod.csv')
        #referencia = df_ref.query(f'''SEXO == "{sexo}" & LINEA == "{linea}" & EDAD = {edad}''')[var]
        try:
            referencia = df[(df['SEXO'] == sexo) &
                            (df['LINEA'] == linea) &
                            (df['EDAD'] == edad)][var]                    
            valor = referencia.values[0]
            return valor

        except Exception as e:
            print(e)
            return None

    if tipo == 'LIQ':
        df = pd.read_csv('Datos/df_ref_liq.csv')
        #referencia = df_ref.query(f'''SEXO == "{sexo}" & LINEA == "{linea}" & EDAD = {edad}''')[var]
        try:
            referencia = df[(df['SEXO'] == sexo) &
                            (df['LINEA'] == linea) &
                            (df['PESO REFERENCIA (g/ave)'] < (1000*peso_promedio))][var]                    
            valor = referencia.values[0]
            return valor

        except Exception as e:
            print(e)
            return None

    if tipo == 'MORT_LIQ':
        df = pd.read_csv('Datos/df_mort_ref_liq.csv')
        #referencia = df_ref.query(f'''SEXO == "{sexo}" & LINEA == "{linea}" & EDAD = {edad}''')[var]
        try:
            referencia = df[df['Dia'] == edad][var]                    
            valor = referencia.values[0]
            return valor

        except Exception as e:
            print(e)
            return None


def dashtable(archivo, tipo = ''):
    if tipo == 'ss':
        types = ['datetime'] + ['numeric']*3 + ['text', 'numeric'] + ['text']*9 + ['numeric', 'text', 'text'] + ['numeric']*25 + ['text']
    if tipo == 'lq':
        types = ['datetime', 'numeric', 'text', 'text', 'text', 'numeric', 'text'] +  ['numeric']*6 + ['text']
    if tipo == 'historico':
        types = ['datetime'] + ['text']*10 + ['numeric'] + ['text']*2 + ['numeric']* 9 + ['text']

    table = dash_table.DataTable(
        data = archivo.to_dict('records'),
        columns = [{'name': i, 'id': i, 'type': j} for i, j in zip(archivo.columns, types)],
        #fixed_columns = {'headers': True},
        #fixed_rows = {'headers': True},
        #fixed_columns = {'headers': True, 'data': 3},
        filter_action = 'native',
        editable = False,
        #dropdown = {'Gerente de Zona': },
        style_table =  {
            'overflowY': 'scroll',
            'overflowY': 'scroll',
            'height': 550,
            'minWidth': '100%'
            },
        style_cell = {
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'textAlign': 'center',
            #'width': '135px',
            'fontSize': 16,
            'font-family': 'sans-serif'
            },
        style_header={
            'backgroundColor': '#FFA651',
            'fontWeight': 'bold',
            'fontSize': 15,
            },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
            ],
        style_cell_conditional = [
            ],
        tooltip_data = [
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
                } for row in archivo.to_dict('rows')
            ],
        tooltip_duration = None
        )

    return table
