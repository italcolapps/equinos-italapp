import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html 
from datetime import datetime, date
import pandas as pd

def campos(id_ = '', label = '', ayuda = '', tipo = '', plh = '', valor = '',
           xl = 2, lg = 2, md = 4, sm = 5, xs = 6, vl = '', style_ = {'padding-left': '1px'}, style_col = {},
           pais = ''):
    if tipo == 'text' or tipo == 'number':
        text_input = dbc.Col(id = id_ + '_col', children = [
            dbc.FormGroup(id = id_ + '_sal', children = [
                dbc.Label(id = id_ + '_label', children = label),
                dbc.Input(id = id_, placeholder = plh, type = tipo,
                          debounce = True, value = valor),
                dbc.FormText(id = id_ + '_ayuda', children = ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs, style = style_col)
        return text_input

    if tipo == 'pw':
        text_input = dbc.Col(id = id_ + '_col', children = [
            dbc.FormGroup(id = id_ + '_sal', children = [
                dbc.Label(id = id_ + '_label', children = label),
                dbc.Input(id = id_, placeholder = plh, type = 'password',
                          debounce = True, value = valor),
                dbc.FormText(id = id_ + '_ayuda', children = ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'date':
        text_input = dbc.Col([
            dbc.FormGroup(
                [
                dbc.Label(label),
                dcc.DatePickerSingle(id = id_, date = valor, style = style_,
                                     display_format='YYYY/MM/DD'),
                dbc.FormText(ayuda, style = {'padding-left': '3px'})
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'slider':
        text_input = dbc.Col(id = id_ + '_col', children = [
            dbc.FormGroup(
                [
                dbc.Label(label),
                dcc.Slider(id = id_, min = 1, max = 49, value = 10,
                           #marks = {i: str(i) for i in range(1, 10)},
                           tooltip = {'always_visible': True}),
                dbc.FormText(ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'seleccion':
        text_input = dbc.Col(id = id_ + '_col', children = [
            dbc.FormGroup(
                [
                dbc.Label(label),
                dbc.Select(id = id_,
                           options = valor,
                           value = vl),
                dbc.FormText(ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'seleccion_m':
        text_input = dbc.Col([
            dbc.FormGroup(
                [
                dbc.Label(label),
                dcc.Dropdown(id = id_,
                           options = valor,
                           multi = True,
                           value = vl),
                dbc.FormText(ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'seleccion_3':
        text_input = dbc.Col(id = id_ + '_col', children = [
            dbc.InputGroup(
                [
                dbc.InputGroupAddon(label, addon_type='prepend'),
                dbc.Select(id = id_,
                           options = valor,
                           value = vl),
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'date_2':
        text_input = dbc.Col(id = id_ + '_col', children = [
            dbc.InputGroup(
                [
                dbc.InputGroupAddon(label),
                dcc.DatePickerSingle(id = id_, date = valor, style = style_,
                                     display_format='YYYY/MM/DD'),
                #dbc.FormText(ayuda, style = {'padding-left': '3px'})
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'depto':
        deptos = pd.read_csv('Datos/Divipola.csv')
        deptos = deptos.loc[deptos['Pais'] == pais]
        text_input = dbc.Col([
            dbc.FormGroup(
                [
                dbc.Label(label),
                dcc.Dropdown(id = id_,
                           options = [{'label': i, 'value': i} for i in deptos['Departamento'].unique()],
                           multi = True
                           ),
                dbc.FormText(ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'seleccion_2':
        text_input = dbc.Col([
            dbc.FormGroup(
                [
                dbc.Label(label),
                dbc.Checklist(id = id_,
                           options = valor,
                           value = vl,
                           inline = True,
                           switch = True),
                dbc.FormText(ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'text_area':
        text_input = dbc.Col([
            dbc.FormGroup(
                [
                dbc.Label(label),
                dbc.Textarea(id = id_, bs_size = 'sm',
                             placeholder = 'Por favor ingrese sus observaciones'),
                dbc.FormText(ayuda)
                ], style = style_)
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
            style = style_col)
        return text_input

    if tipo == 'boton':
        input = dbc.Col([
                    dbc.Button(valor, id = id_)
                ], xl = xl, lg = lg, md = md, sm = sm, xs = xs,
                style = style_col)
        return input

    if tipo == 'seleccion_2_':
        text_input = dbc.Col([
            dbc.FormGroup(
                [
                dbc.Label(label),
                dbc.RadioItems(id = id_,
                           options = [{'label': i, 'value': i} for i in ['Si', 'No']],
                           value = 'No', inline = True),
                dbc.FormText(ayuda)
                ], style = {'padding-left': '15px'})
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs)
        return text_input

    if tipo == 'text_sal' or tipo == 'number_sal':
        text_input = dbc.Col([
            dbc.FormGroup(id = id_ + '_sal',
                children = [
                dbc.Label(label),
                dbc.Input(id = id_, placeholder = plh, type = tipo.split('_')[0],
                          debounce = True, value = valor),
                dbc.FormText(ayuda)
                ], style = {'padding-left': '5px', 'visibility': 'hidden'})
            ], xl = xl, lg = lg, md = md, sm = sm, xs = xs)
        return text_input

# campos consulta de informacion

## campos ingreso de datos
razas = ['Criollo Colombiano', 'Cuarto de Milla', 'Árabe', 'Pura Raza Español', 'Lusitano',
'Belga', 'Percherón', 'Frisón', 'PSI', 'Silla Francesa', 'Silla Argentino',
'Apaloosa', 'Andaluz', 'Paso Peruano', 'Falabella', 'Mini Horse', 'Hannoveriano',
'Lipizzano', 'Pinto Americano', 'Poni', 'Asnal', 'Mular', 'Pura Sangre de Carrera',
'Criollo Ecuatoriano', 'Polo', 'Otra'] #
razas.sort()
ref_alimento = ['Brio Adultos', 'Brio Yeguas', 'Brio Potros', 'Brio Fx', 'Pódium',
                'Equinos', 'Caballos de Fuerza', 'Furia Total', 'Multiforraje']
fecha_actual_p1 = campos(id_ = 'fecha_ac_p1', label = 'Fecha actual', tipo = 'date',
                         ayuda = 'Año/Mes/Día', valor = datetime.today().date())
fecha_u_v_p1 = campos(id_ = 'fecha_u_v_p1', label = 'Fecha útima visita', tipo = 'date',
                      ayuda = 'Año/Mes/Día', valor = date(2020, 11, 21))
fecha_nac_p1 = campos(id_ = 'fecha_nac_p1', label = 'Fecha de nacimiento', tipo = 'date',
                      ayuda = 'Año/Mes/Día', valor = date(2020, 1, 1))

pais_p1 = campos(id_ = 'pais_p1', label = 'Pais', ayuda = '-',tipo = 'seleccion',
                 valor = [{'label': 'Colombia', 'value': 'Colombia'},
                          {'label': 'Panamá', 'value': 'Panamá'},
                          {'label': 'Ecuador', 'value': 'Ecuador'}])
# gerente_p1 = campos(id_ = 'gerente_p1', label = 'Gerente de zona', ayuda = '-',tipo = 'seleccion',
#                  valor = [{'label': '-', 'value': '-'}], xl = 3, lg = 3, md = 5, sm = 6, xs = 6)
# criadero_p1 = campos(id_ = 'criadero_p1', label = 'Criadero', ayuda = '-',tipo = 'seleccion',
#                  valor = [{'label': '-', 'value': '-'}], xl = 2, lg = 2, md = 5, sm = 6, xs = 6)
nuevo_e_p1 = campos(id_ = 'nuevo_e_p1', label = 'Registrar equino?', ayuda = 'Registrar equino',
                    tipo = 'seleccion_2_', xl = 2, lg = 2, md = 4, sm = 4, xs = 4)
depto_p1 = campos(id_ = 'depto_p1', label = 'Departamento', ayuda = '-',tipo = 'seleccion',
                 valor = [{'label': '-', 'value': '-'}], xl = 2, lg = 2, md = 5, sm = 6, xs = 6)
mun_p1 = campos(id_ = 'mun_p1', label = 'Municipio', ayuda = '-',tipo = 'seleccion',
                 valor = [{'label': '-', 'value': '-'}], xl = 2, lg = 2, md = 5, sm = 6, xs = 6)   
nombre_p1 = campos(id_ = 'nombre_p1', label = 'Nombre del equino', ayuda = '-',tipo = 'seleccion',
                 valor = [{'label': '-', 'value': '-'}], xl = 3, lg = 3, md = 5, sm = 6, xs = 6)
planta_p1 = campos(id_ = 'planta_p1', label = 'Planta', ayuda = 'Planta de alimento',tipo = 'seleccion',
                 valor = [{'label': '-', 'value': '-'}], xl = 2, lg = 2, md = 4, sm = 5, xs = 5)                 
raza_p1 = campos(id_ = 'raza_p1', label = 'Raza', ayuda = 'Raza equino', tipo = 'seleccion',
                 valor = [{'label': i, 'value': i} for i in razas], xl = 3, lg = 3, md = 4, sm = 6, xs = 6)
ref_p1 = campos(id_ = 'ref_p1', label = 'Referencia', ayuda = 'Referencia de alimento',
                tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in ref_alimento],
                xl = 3, lg = 3, md = 4, sm = 6, xs = 6)
etapa_p1 = campos(id_ = 'etapa_p1', label = 'Etapa fisiológica', ayuda = 'Etapa del equino',
                  tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in ['Adulto', 'Potro', 'Yegua en Lactancia', 'Yegua Preñada']])
sexo_p1 = campos(id_ = 'sexo_p1', label = 'Sexo', ayuda = 'Sexo del equino',
                 tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in ['Macho', 'Hembra']])
peso_p1 = campos(id_ = 'peso_p1', label = 'Peso', ayuda = 'Kg', tipo = 'number', valor = None)
peso_a_p1 = campos(id_ = 'peso_a_p1', label = 'Peso anterior', ayuda = 'Kg', tipo = 'number')
alzada_p1 = campos(id_ = 'alzada_p1', label = 'Alzada', ayuda = 'cm', tipo = 'number', valor = None)
condicion_p1 = campos(id_ = 'condicion_p1', label = 'Condición corporal', ayuda = '-',
                   tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in range(1, 10, 1)])
calidad_p1 = campos(id_ = 'calidad_p1', label = 'Calidad pelaje', ayuda = '-',
                    tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in range(1, 6, 1)])
obs_p1 = campos(id_ = 'obs_p1', label = 'Observaciones', ayuda = '', tipo = 'text',
                xl = 4, lg = 4, md = 4, sm = 8, xs = 8)

# campos seccion plan sanitario
influenza_t = campos(id_ = 'influenza_t', label = 'Vacuna Influenza + tétano', tipo = 'seleccion_3',
                     valor = [{'label': i, 'value': i} for i in ['Si', 'No']], vl = None,
                     xl = 4, lg = 5, md = 7, sm = 12, xs = 12)
fecha_influenza_t = campos(id_ = 'fecha_influenza_t', label = 'Fecha vacunación', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = datetime.today().date(),
                         xl = 4, lg = 5, md = 7, sm = 12, xs = 12)
prx_influenza_t = campos(id_ = 'prx_influenza_t', label = 'Próxima', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = None, #datetime.today().date(),
                         xl = 3, lg = 4, md = 6, sm = 10, xs = 10)
obs_influenza_t = campos(id_ = 'obs_influenza_t', label = 'Observaciones', ayuda = '', tipo = 'text',
                         xl = 6, lg = 7, md = 8, sm = 10, xs = 10)


tetano = campos(id_ = 'tetano', label = 'Vacuna Tétano', tipo = 'seleccion_3',
                     valor = [{'label': i, 'value': i} for i in ['Si', 'No']], vl = None,
                     xl = 3, lg = 4, md = 6, sm = 12, xs = 12)
fecha_tetano = campos(id_ = 'fecha_tetano', label = 'Fecha vacunación', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = datetime.today().date(),
                         xl = 4, lg = 5, md = 7, sm = 12, xs = 12)
prx_tetano = campos(id_ = 'prx_tetano', label = 'Próxima', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = None, #datetime.today().date(),
                         xl = 3, lg = 4, md = 6, sm = 10, xs = 10)        
obs_tetano = campos(id_ = 'obs_tetano', label = 'Observaciones', ayuda = '', tipo = 'text',
                    xl = 6, lg = 7, md = 8, sm = 10, xs = 10)


encefalitis = campos(id_ = 'encefalitis', label = 'Vacuna encefalitis equina venezolana', tipo = 'seleccion_3',
                     valor = [{'label': i, 'value': i} for i in ['Si', 'No']], vl = None,
                     xl = 5, lg = 6, md = 8, sm = 12, xs = 12)
fecha_encefalitis = campos(id_ = 'fecha_encefalitis', label = 'Fecha vacunación', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = datetime.today().date(),
                         xl = 4, lg = 5, md = 7, sm = 12, xs = 12)
prx_encefalitis = campos(id_ = 'prx_encefalitis', label = 'Próxima', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = None, #datetime.today().date(),
                         xl = 3, lg = 4, md = 6, sm = 10, xs = 10)   
obs_encefalitis = campos(id_ = 'obs_encefalitis', label = 'Observaciones', ayuda = '', tipo = 'text',
                         xl = 6, lg = 7, md = 8, sm = 10, xs = 10)


desparasitacion = campos(id_ = 'desparasitacion', label = 'Desparasitación', tipo = 'seleccion_3',
                     valor = [{'label': i, 'value': i} for i in ['Si', 'No']], vl = None,
                     xl = 3, lg = 4, md = 6, sm = 12, xs = 12)
fecha_desparasitacion = campos(id_ = 'fecha_desparasitacion', label = 'Fecha desparasitación', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = datetime.today().date(),
                         xl = 4, lg = 5, md = 7, sm = 12, xs = 12)   
prx_desparasitacion = campos(id_ = 'prx_desparasitacion', label = 'Próxima', tipo = 'date_2',
                         ayuda = 'Año/Mes/Día', valor = None, #datetime.today().date(),
                         xl = 3, lg = 4, md = 6, sm = 10, xs = 10) 
obs_desparasitacion= campos(id_ = 'obs_desparasitacion', label = 'Observaciones', ayuda = '', tipo = 'text',
                            xl = 6, lg = 7, md = 8, sm = 10, xs = 10)


ids_plan_s = ['fecha_influenza_t', 'prx_influenza_t', 'fecha_tetano', 'prx_tetano', 'fecha_encefalitis', 
              'prx_encefalitis', 'fecha_desparasitacion', 'prx_desparasitacion', 'influenza_t', 
              'obs_influenza_t', 'tetano', 'obs_tetano', 'encefalitis', 'obs_encefalitis', 
              'desparasitacion',  'obs_desparasitacion']

ids_plan_s_ = ['influenza_t', 'tetano', 'encefalitis', 'desparasitacion']

ids_p1 = ['edad_p1_1', 'dias_p1_1', 'gerente_p1', 'criadero_p1', 'nuevo_e_p1', 'nombre_p1',
          'raza_p1', 'planta_p1', 'ref_p1', 'etapa_p1', 'sexo_p1', 'peso_p1',
          'peso_a_p1', 'alzada_p1', 'condicion_p1', 'calidad_p1', 'andar_p1',
          'obs_p1', 'mun_p1']

ids_p1_ = ['nombre_p1', 'ref_p1', 'peso_p1', 'alzada_p1', 'condicion_p1', 'calidad_p1', 
           'obs_p1']

# campos entrenamiento deportivo
# pais_p2 = campos(id_ = 'pais_p2', label = 'Pais', ayuda = '-', tipo = 'seleccion',
#                  valor = [{'label': i, 'value': i} for i in ['Colombia', 'Ecuador', 'Panamá']],
#                  xl = 2, lg = 2, md = 4, sm = 3, xs = 3)
criadero_p2 = campos(id_ = 'criadero_p2', label = 'Criadero', ayuda = '-', tipo = 'text')
nombre_p2 = campos(id_ = 'nombre_p2', label = 'Nombre del equino', ayuda = '-',
                   tipo = 'text')
raza_p2 = campos(id_ = 'raza_p2', label = 'Raza', ayuda = 'Raza equino', tipo = 'seleccion',
                 valor = [{'label': i, 'value': i} for i in razas], xl = 3, lg = 3, md = 4, sm = 6, xs = 6)
edad_p2 = campos(id_ = 'edad_p2', label = 'Edad', ayuda = 'Meses', tipo = 'number')
peso_p2 = campos(id_ = 'peso_p2', label = 'Peso', ayuda = 'Kg', tipo = 'number')
condicion_p2 = campos(id_ = 'condicion_p2', label = 'Condición corporal', ayuda = '-',
                   tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in range(1, 10, 1)])
calidad_p2 = campos(id_ = 'calidad_p2', label = 'Calidad pelaje', ayuda = '-',
                    tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in range(1, 6, 1)])
alzada_p2 = campos(id_ = 'alzada_p2', label = 'Alzada', ayuda = 'cm', tipo = 'number')
etapa_p2 = campos(id_ = 'etapa_p2', label = 'Etapa fisiológica', ayuda = 'Etapa del equino',
                  tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in ['Adulto',
                                                                                  'Potro',
                                                                                  'Yegua en Lactancia',
                                                                                  'Yegua Preñada']])
ref_p2 = campos(id_ = 'ref_p2', label = 'Referencia', ayuda = 'Referencia de alimento',
                tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in ref_alimento],
                xl = 3, lg = 3, md = 4, sm = 6, xs = 6)
piscina_p2 = campos(id_ = 'piscina_p2', label = 'Piscina', ayuda = '-', tipo = 'seleccion',
                    valor = [{'label': i, 'value': i} for i in ['Si', 'No']],
                    xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
freq_ps = campos(id_ = 'freq_ps', label = 'Frecuencia', ayuda = 'Por semana',
                 tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
tiempo_ps = campos(id_ = 'tiempo_ps', label = 'Tiempo', ayuda = 'Minutos',
                   tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)


pisod_p2 = campos(id_ = 'pisod_p2', label = 'Piso duro', ayuda = '-', tipo = 'seleccion',
                  valor = [{'label': i, 'value': i} for i in ['Si', 'No']],
                  xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
freq_pd = campos(id_ = 'freq_pd', label = 'Frecuencia', ayuda = 'Por semana',
                 tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
tiempo_pd = campos(id_ = 'tiempo_pd', label = 'Tiempo', ayuda = 'Minutos',
                   tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)

torno_p2 = campos(id_ = 'torno_p2', label = 'Torno', ayuda = '-', tipo = 'seleccion',
                  valor = [{'label': i, 'value': i} for i in ['Si', 'No']],
                  xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
freq_tr = campos(id_ = 'freq_tr', label = 'Frecuencia', ayuda = 'Por semana',
                 tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
tiempo_tr = campos(id_ = 'tiempo_tr', label = 'Tiempo', ayuda = 'Minutos',
                   tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)

campo_p2 = campos(id_ = 'campo_p2', label = 'Campo', ayuda = '-', tipo = 'seleccion',
                  valor = [{'label': i, 'value': i} for i in ['Si', 'No']],
                  xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
freq_cp = campos(id_ = 'freq_cp', label = 'Frecuencia', ayuda = 'Por semana',
                 tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)
tiempo_cp = campos(id_ = 'tiempo_cp', label = 'Tiempo', ayuda = 'Minutos',
                   tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)

calen_p2 = campos(id_ = 'calen_p2', label = 'Calentamiento', ayuda = '¿Realiza?', tipo = 'seleccion',
                  valor = [{'label': i, 'value': i} for i in ['Si', 'No']],
                  xl = 2, lg = 2, md = 3, sm = 4, xs = 4)
tiempo_cl = campos(id_ = 'tiempo_cl', label = 'Tiempo', ayuda = 'Minutos',
                   tipo = 'number_sal', xl = 2, lg = 2, md = 3, sm = 3, xs = 3)


fc_max_p2 = campos(id_ = 'fc_max_p2', label = 'FC máxima', ayuda = '-', tipo = 'number',
                   xl = 2, lg = 2, md = 3, sm = 4, xs = 4)
fc_min_p2 = campos(id_ = 'fc_min_p2', label = 'FC mínima', ayuda = '-', tipo = 'number',
                   xl = 2, lg = 2, md = 3, sm = 4, xs = 4)
fc_prom_p2 = campos(id_ = 'fc_prom_p2', label = 'FC promedio', ayuda = '-', tipo = 'number',
                    xl = 2, lg = 2, md = 3, sm = 4, xs = 4)
horain_p2 = campos(id_ = 'horain_p2', label = 'Hora inicio', ayuda = 'Inicio entrenamiento hr:min',
                   tipo = 'text', xl = 2, lg = 2, md = 3, sm = 5, xs = 5, plh = 'Hora:Minuto')
horafn_p2 = campos(id_ = 'horafn_p2', label = 'Hora final', ayuda = 'Final entrenamiento hr:min',
                   tipo = 'text', xl = 2, lg = 2, md = 3, sm = 5, xs = 5, plh = 'Hora:Minuto')
sud = ['1: Impreceptible', '2: Bajo', '3: Moderado', '4: Alto', '5: Muy alto']
grado_p2 = campos(id_ = 'grado_p2', label = 'Grado de sudoración', ayuda = '-',
                  tipo = 'seleccion', valor = [{'label': i, 'value': i} for i in sud])
agua_p2 = campos(id_ = 'agua_p2', label = 'Consumo de agua', ayuda = 'Litros',
                 tipo = 'number')
consumo_p2 = campos(id_ = 'consumo_p2', label = 'Consumo de sal', ayuda = 'A volunatad', tipo = 'seleccion',
                  valor = [{'label': i, 'value': i} for i in ['Si', 'No']],
                  xl = 2, lg = 2, md = 3, sm = 4, xs = 4)
fc_fn_p2 = campos(id_ = 'fc_fn_p2', label = 'FC final', ayuda = '-', tipo = 'number')
fc_fn_1_p2 = campos(id_ = 'fc_fn_1_p2', label = 'FC final 1 min', ayuda = '1 minuto después',
                    tipo = 'number')
ind_rc_p2 = campos(id_ = 'ind_rc_p2', tipo = 'number', ayuda = 'Recuperación cardiaca',
                   label = 'Índice RC')
obs_p2 = campos(id_ = 'obs_p2', label = 'Observaciones', ayuda = '', tipo = 'text',
                xl = 4, lg = 4, md = 4, sm = 6, xs = 6)

ids_p2 = ['criadero_p2', 'nombre_p2', 'raza_p2', 'edad_p2', 'peso_p2',
          'condicion_p2', 'calidad_p2', 'alzada_p2', 'etapa_p2', 'ref_p2', 'piscina_p2',
          'freq_ps', 'tiempo_ps', 'pisod_p2', 'freq_pd', 'tiempo_pd', 'torno_p2',
          'freq_tr', 'tiempo_tr', 'campo_p2', 'freq_cp', 'tiempo_cp', 'calen_p2',
          'tiempo_cl', 'fc_max_p2', 'fc_min_p2', 'fc_prom_p2', 'horain_p2', 'horafn_p2',
          'grado_p2', 'agua_p2', 'consumo_p2', 'fc_fn_p2', 'fc_fn_1_p2', 'ind_rc_p2', 'obs_p2']

# campos reporte alzadas
# ra > reporte de alzadas_
especialista_ra = campos(id_ = 'espc_p4', label = 'Nombre especialista', ayuda = '-',
                         tipo = 'text', xl = 3, lg = 3, md = 6, sm = 8, xs = 8)
contacto_ra = campos(id_ = 'cont_p4', label = 'Contacto especialista', ayuda = '-',
                         tipo = 'text', xl = 3, lg = 3, md = 6, sm = 8, xs = 8)
observaciones_ra = campos(id_ = 'obs_p4', label = 'Observaciones', ayuda = '-',
                         tipo = 'text_area', xl = 3, lg = 3, md = 6, sm = 8, xs = 8)                      
ids_ra = ['gerente_p3_ra', 'criadero_p3_ra', 'equino_p3_ra', 'espc_p4', 'cont_p4', 'obs_p4']
ids_eq= ['gerente_p3_eq', 'criadero_p3_eq']
ids_ha= ['gerente_p3_ha', 'criadero_p3_ha', 'año_p3_ha', 'mes_p3_ha']
ids_ps= ['gerente_p3_ps', 'criadero_p3_ps']

form_sal = dbc.Form([
            html.Hr(),
            dbc.Spinner(dbc.Alert(id = 'aux_p4', is_open = False, duration = 4000)),
            dbc.FormGroup([
                html.H5('INFORMACIÓN GENERAL del equino'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'tab_1'),
            ], style = {'padding-button': '10px'}),
            dbc.FormGroup([
                html.H5('GANANCIA PESO DIARIA'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'tab_2')
            ], style = {'padding-button': '10px'}),
            dbc.FormGroup([
                html.H5('PESO Y CONDICIÓN CORPORAL'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'graph_1')
            ], style = {'padding-button': '10px'}),
            dbc.FormGroup([
                html.H5('ALZADA'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'graph_2'),
            ], style = {'padding-button': '10px'}),
            dbc.FormGroup([
                html.H5('OBSERVACIONES'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'tab_3'),
            ], style = {'padding-button': '10px'}),
            dbc.FormGroup([
                html.H5('PLAN SANITARIO'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'tab_ps'),
            ], style = {'padding-button': '10px'}),
            dbc.FormGroup([
                html.H5('CONTACTO ESPECIALISTA LINEA EQUINOS'.title(),
                        style = {'font-size': '18px'}),
                html.Div(id = 'tab_4'),
            ], style = {'padding-button': '10px'}),
], style = {'padding-left': '25px'})
ids_sal_p4 = ['tab_1', 'tab_2', 'graph_1', 'graph_2', 'tab_3', 'tab_4', 'tab_ps']

# campos creacion usuario

usuario_cliente = campos(id_ = 'usuario_cliente', label = 'NOMBRE DE USUARIO', 
                         ayuda = 'Use minúsculas, no use espacios.', tipo = 'text',
                         xl = 3, lg = 4, md = 6, sm = 6, xs = 6)
pw_cliente = campos(id_ = 'pw_cliente', label = 'CONTRASEÑA DE INGRESO', plh = '******',
                    ayuda = 'Recuerde que debe contar con al menos 8 caracteres', tipo = 'pw',
                    xl = 3, lg = 2, md = 6, sm = 6, xs = 6)
# campos creacion gerente
documento_gerente = campos(id_ = 'documento_gerente', label = 'DOCUMENTO DE IDENTIDAD', ayuda = '-', tipo = 'number',
                           xl = 3, lg = 4, md = 6, sm = 6, xs = 6)
nombre_gerente = campos(id_ = 'nombre_gerente', label = 'NOMBRE DEL GERENTE', ayuda = 'Nombre y apellido', tipo = 'text',
                        xl = 4, lg = 5, md = 8, sm = 10, xs = 10)
pais_gerente = campos(id_ = 'pais_gerente', label = 'PAIS', ayuda = '-', tipo = 'seleccion',
                        valor = [{'label': i, 'value': i} for i in ['COLOMBIA', 'ECUADOR', 'PANAMÁ']],
                        xl = 3, lg = 4, md = 6, sm = 6, xs = 6)
zona_gerente = campos(id_ = 'zona_gerente', label = 'ZONA', ayuda = '-', tipo = 'text',
                        xl = 3, lg = 4, md = 4, sm = 10, xs = 10)
usuario_gerente = campos(id_ = 'usuario_gerente', label = 'NOMBRE DE USUARIO', 
                         ayuda = 'Use minúsculas, no use espacios.', tipo = 'text',
                         xl = 3, lg = 4, md = 6, sm = 6, xs = 6)
pw_gerente = campos(id_ = 'pw_gerente', label = 'CONTRASEÑA DE INGRESO', plh = '******',
                    ayuda = 'Recuerde que debe contar con al menos 8 caracteres', tipo = 'pw',
                    xl = 3, lg = 2, md = 6, sm = 6, xs = 6)
ids_crear_gerente = ['documento_gerente', 'nombre_gerente', 'pais_gerente', 'zona_gerente', 'usuario_gerente', 'pw_gerente']

## campos crear granja/criadero
nit_clientes = campos(id_ = 'nit_clientes', label = 'NIT DEL CLIENTE', ayuda = '-', tipo = 'seleccion',
                     xl = 3, lg = 4, md = 6, sm = 6, xs = 6, valor = [{'label': '-', 'value': '-'}])
nit_clientes_nc = campos(id_ = 'nit_clientes_nc', label = 'NIT DEL CLIENTE', ayuda = '-', tipo = 'seleccion',
                     xl = 3, lg = 4, md = 6, sm = 6, xs = 6, valor = [{'label': '-', 'value': '-'}])                     
nombre_clientes = campos(id_ = 'nombre_clientes', label = 'NOMBRE DEL CRIADERO', ayuda = '-', tipo = 'text',
                        xl = 3, lg = 4, md = 6, sm = 6, xs = 6)                     
nombre_granja = campos(id_ = 'nombre_granja', label = 'NOMBRE DE LA GRANJA', ayuda = '-', tipo = 'text',
                       xl = 4, lg = 5, md = 8, sm = 10, xs = 10)
# depto_granja = campos(id_ = 'depto_granja', label = 'DEPARTAMENTO/PROVINCIA', ayuda = '-', tipo = 'depto',
#                        xl = 3, lg = 4, md = 6, sm = 12, xs = 12)
municipio_granja = campos(id_ = 'municipio_granja', label = 'MUNICIPIO', ayuda = '-', tipo = 'seleccion_m',
                           valor = [{'label': '-', 'value': '-'}],
                           xl = 3, lg = 4, md = 6, sm = 12, xs = 12)


ids_granjas_nc = ['gerente_nc', 'nombre_clientes', 'depto_granja', 'municipio_granja', 'usuario_cliente', 'pw_cliente']

