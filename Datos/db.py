import pymysql
import pymysql.cursors
import pandas as pd
import time


def usuario():
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            sql = 'SELECT nombre, usuario_, rol_usuario, doc_id, contraseña, pais FROM usuarios'
            cursor.execute(sql)
            result = cursor.fetchall()

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    return pd.DataFrame(result)


def get_data(sql):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    return pd.DataFrame(result)

def change_pw(new_pw, user):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:

            sql = f'''
                UPDATE `usuarios` SET `contraseña` = '{new_pw}' WHERE (`usuario_` = '{user}');
            '''
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


def crear_usuario(usuario, rol, doc_id, pais, nombre, pw):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            sql = f'''
           INSERT INTO `usuarios` (usuario_, doc_id, rol_usuario, nombre, contraseña, pais)
           VALUES ('{usuario}', {doc_id}, '{rol}', '{nombre}', '{pw}', '{pais.upper()}');
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

def crear_gerente(documento, nombre, zona, pais, creador):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            sql = f'''
           INSERT INTO `gerentes` (doc_id, nombre_gerente, zona, pais, creador)
           VALUES ('{documento}', '{nombre.upper()}', '{zona.upper()}', '{pais.upper()}', '{creador.upper()}');
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


def add_row_alzadas(db):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            sql = f'''
                INSERT INTO `seguimiento_alzadas`(fecha, pais, id_gerente, gerente_zona, departamento_provincia, municipio, id_criadero, nombre_criadero, id_equino, nombre_equino, raza, planta_alimento, referencia_alimento, etapa_fisiologica, edad_meses, sexo, andar, peso_kg, peso_anterior_kg, dias_entre_visita, gpd_g, alzada_cm, referencia_alzada_cm, diferencia_cm, condicion_corporal, calidad_pelaje, observaciones)
                VALUES ('{db["Fecha"]}', '{db["Pais"]}', '{db["id_gerente"]}', '{db["Gerente de Zona"]}', '{db["Departamento/Provincia"]}', '{db["Municipio"]}', '{db["id_criadero"]}', '{db["Nombre Criadero"]}', '{db["id_equino"]}', '{db["Nombre Equino"]}', '{db["Raza"]}', '{db["Planta de alimento"]}', '{db["Referencia Alimento"]}', '{db["Etapa Fisiológica"]}', {db["Edad (Meses)"]}, '{db["Sexo"]}', '{db["Andar"]}', {db["Peso (Kg)"]}, {db["Pesaje Anterior (Kg)"]}, {db["Días entre visitas"]}, {db["GPD (g)"]}, {db["Alzada (cm)"]}, {db["Referencia Alzada (cm)"]},  {db["Diferencia (cm)"]}, {db["Condicion Corporal"]}, {db["Calidad del Pelaje"]}, '{db["Observaciones"]}');
            '''
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


def add_row_entrenamiento(db):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppEquinos',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            sql = f'''
                INSERT INTO `entrenamiento_deportivo` (fecha, pais, criadero, nombre_equino, raza_equino, edad_meses, peso_kg, condicion_corporal, 
                                                       calidad_pelaje, alzada_cm, etapa, referencia_alimento, calentamiento, tiempo_calentamiento, 
                                                       piscina, frecuencia_piscina, tiempo_piscina, piso_duro, frecuencia_piso_duro, tiempo_piso_duro, 
                                                       torno, frecuencia_torno, tiempo_torno, campo, frecuencia_campo, tiempo_campo, hora_inicio, 
                                                       hora_final, fc_promedio, fc_maxima, fc_minima, grado_sudoracion, consumo_agua_lts, consumo_sal, 
                                                       fc_final, fc_final_1min, irc, observaciones)
                VALUES ('{db["Fecha"]}','{db["Pais"]}','{db["Criadero"]}','{db["Nombre Equino"]}','{db["Raza Equino"]}',{db["Edad (meses)"]},
                        {db["Peso (kg)"]},'{db["Condición Corporal"]}','{db["Calidad Pelaje"]}',{db["Alzada (cm)"]},'{db["Etapa"]}',
                        '{db["Referencia Alimento"]}','{db["Calentamiento"]}',{db["Tiempo c"]},'{db["Piscina"]}',{db["Frecuencia p"]},
                        {db["Tiempo p"]},'{db["Piso Duro"]}',{db["Frecuencia pd"]},{db["Tiempo pd"]},'{db["Torno"]}',{db["Frecuencia t"]},
                        {db["Tiempo t"]},'{db["Campo"]}',{db["Frecuencia cp"]},{db["Tiempo cp"]},'{db["Hora Inicio"]}','{db["Hora Final"]}',
                        {db["FC Prom"]},{db["FC max"]},{db["FC min"]},'{db["Grado sudoracion"]}',{db["Consumo Agua"]},'{db["Consumo Sal"]}',
                        {db["FC Final"]},{db["FC Final (1 min)"]},{db["IRC"]},'{db["Observaciones"]}');
            '''
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

