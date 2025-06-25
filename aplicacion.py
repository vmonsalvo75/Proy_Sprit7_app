#Cargar librerias
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

#Carga de datos     
car_data = pd.read_csv('vehicles_us.csv') # leer los datos

#Titulo subrayado
st.header("Vehiculos", divider = "gray")

#Botón para desargar datos
st.download_button(
    label = "Descargar datos",  #Texto de botón
    data = car_data.to_csv(index = False), #Base a descargar
    file_name = "Vehiculos.csv" #Nombre con el que se descarga la base
)

#dividir pantalla
#st.divider()

hist_button = st.button('Construir histograma') # crear un botón
     
if hist_button: # al hacer clic en el botón
# escribir un mensaje
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
         
    # crear un histograma
    fig = px.histogram(car_data, x="odometer")
     
    # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)

# crear una casilla de verificación
build_histogram = st.checkbox('Construir un histograma')

if build_histogram: # si la casilla de verificación está seleccionada
    st.write('Construir un histograma para la columna odómetro')

#Dividir pag
st.divider()

#Seleccionador de variables
numericas = car_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
categoricas = car_data.select_dtypes(include='object').columns.tolist()

st.subheader("Análisis personalizado")

var_num = st.multiselect(
    label="Seleccione variables numéricas (máx 2):",
    options=numericas,
    max_selections=2
)

var_cat = st.selectbox(
    label="Seleccione una variable categórica para colorear (opcional):",
    options=['(ninguna)'] + categoricas
)

#Boton para ejecutar graficos
analisis_b = st.button(
    label = "Analizar"
)

st.divider()

#Analisis de datos
if analisis_b:
    if len(var_num) != 2:
        st.warning("Selecciona exactamente 2 variables numéricas.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            hist_1 = px.histogram(car_data, x=var_num[0], color=var_cat if var_cat != '(ninguna)' else None,
                                  title=f"Distribución de {var_num[0]}")
            st.plotly_chart(hist_1, use_container_width=True)

            prom1 = car_data[var_num[0]].mean()
            st.metric("Media", f"{round(prom1, 1)}")

        with col2:
            hist_2 = px.histogram(car_data, x=var_num[1], color=var_cat if var_cat != '(ninguna)' else None,
                                  title=f"Distribución de {var_num[1]}")
            st.plotly_chart(hist_2, use_container_width=True)

        # Gráfico de dispersión
        scatter = px.scatter(car_data, x=var_num[0], y=var_num[1],
                             color=var_cat if var_cat != '(ninguna)' else None,
                             title=f"Dispersión {var_num[1]} vs {var_num[0]}")
        st.plotly_chart(scatter, use_container_width=True)
        
        if var_cat != '(ninguna)':
            st.subheader(f"Métricas de la variable categórica: {var_cat}")
        
            # Elimina nulos para trabajar con la columna categórica
            cat_series = car_data[var_cat].dropna()

            n_categorias = cat_series.nunique()
            moda = cat_series.mode()[0]
            frecuencia = cat_series.value_counts(normalize=True).iloc[0] * 100

            col3, col4, col5 = st.columns(3)

            with col3:
                st.metric("Categorías únicas", n_categorias)
            with col4:
                st.metric("Moda", moda)
            with col5:
                st.metric("Frecuencia de la moda", f"{frecuencia:.1f}%")

            # (Opcional) Tabla de frecuencia completa
            st.write("Frecuencia por categoría:")
            st.dataframe(cat_series.value_counts())
            
            # Gráfico de barras con frecuencias
            freq_df = cat_series.value_counts().reset_index()
            freq_df.columns = [var_cat, 'Frecuencia']

            bar_plot = px.bar(freq_df, x=var_cat, y='Frecuencia', 
                            title=f"Frecuencia por categoría de '{var_cat}'",
                            text='Frecuencia')
            st.plotly_chart(bar_plot, use_container_width=True)
