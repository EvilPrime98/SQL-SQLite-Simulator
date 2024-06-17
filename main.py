import streamlit as st
import sqlite3
import pandas as pd
import os
import re
from converter import convert_sqlite_syntax

def ejecutar_consulta(query, nombre_bd):
    if not os.path.exists(nombre_bd):
        conn = sqlite3.connect(nombre_bd)
        conn.close()
    
    conn = sqlite3.connect(nombre_bd)
    c = conn.cursor()
    try:
        for statement in query.split(';'):
            if statement.strip():
                c.execute(statement)
        if query.strip().lower().startswith('select'):
            datos = c.fetchall()
            columnas = [desc[0] for desc in c.description]
            df = pd.DataFrame(datos, columns=columnas)
            conn.close()
            return df
        elif query.strip().lower().startswith('create table'):
            conn.commit()
            conn.close()
            return None
        else:
            conn.commit()
            conn.close()
            return "Operación realizada exitosamente."
    except sqlite3.Error as e:
        conn.close()
        return f"Error: {e}"

def cargar_sql(nombre_archivo, nombre_bd):
    try:
        with open(nombre_archivo, 'rb') as file:
            contenido = file.read()
        
        try:
            query = contenido.decode('utf-8')
        except UnicodeDecodeError:
            query = contenido.decode('latin-1') 
        
        query_convertida = convert_sqlite_syntax(query)
        
        resultado = ejecutar_consulta(query_convertida, nombre_bd)
        return resultado
    except Exception as e:
        return f"Error al cargar y ejecutar el archivo SQL: {str(e)}"

st.title('Simulador de SQL')

nombre_bd = st.text_input("Ingrese el nombre de la base de datos:", "basededatos.db")

consulta_sql = st.text_area("Escribe tu consulta SQL aquí:", height=200)

archivo_sql = st.file_uploader("O seleccione un archivo .sql para cargar:")

if st.button('Ejecutar consulta SQL'):
    if consulta_sql.strip():
        resultado = ejecutar_consulta(consulta_sql, nombre_bd)
        if isinstance(resultado, pd.DataFrame):
            st.dataframe(resultado)
        elif resultado is None:
            st.success("Operación realizada exitosamente.")
        else:
            st.error(resultado)
    else:
        st.error("Por favor, escribe una consulta SQL.")

if archivo_sql is not None:
    contenido = archivo_sql.read()
    if st.button('Cargar y ejecutar archivo .sql'):
        nombre_temporal = "temp.sql"
        with open(nombre_temporal, 'wb') as f:
            f.write(contenido)
        
        try:
            query = contenido.decode('utf-8')
        except UnicodeDecodeError:
            query = contenido.decode('latin-1')
        
        query_convertida = convert_sqlite_syntax(query)
        
        resultado = cargar_sql(nombre_temporal, nombre_bd)
        os.remove(nombre_temporal)
        if isinstance(resultado, pd.DataFrame):
            st.dataframe(resultado)
        elif resultado is None:
            st.success("Operación realizada exitosamente.")
        else:
            st.error(resultado)
