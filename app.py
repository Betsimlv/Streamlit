#importar librerias
import streamlit as st
import folium
import google.auth
import pandas as pd
#from streamlit_folium import folium_static


 
#Extraer los datos de google cloud

#credenciales = google.auth.default()
#ruta = "gs://archivo_ml/data_sistema_final.parquet"
#df = pd.read_parquet(ruta)
df = pd.read_parquet("data_sistema_final.parquet")

#Encabezado
st.markdown('<h1 style="color: #20639B;text-align: center;">ANALYTICAL INSIGHTS CO.</h1>', unsafe_allow_html=True)

#Subencabezado
st.markdown('<h2 style="color: #173F5F; text-align: center;">Sistema de Recomendación </h2>', unsafe_allow_html=True)


#Texto de explicación
texto = "Un sistema de recomendación funciona tanto para personalizar un producto como para entender las preferencias de los consumidores, su comportamiento y los productos de interés. Este sistema ofrece información sobre los steakhouses que probablemente le gusten a consumidores que nunca han visitado esos lugares, así como también información general sobre el usuario."
st.markdown(texto)




# Función para obtener las recomendaciones    
def obtener_recomendaciones(user_id):
    
    user_id = int(user_id)
    
    # Filtrar el DataFrame por user_id
    df_filtrado = df[df['user_id'] == user_id]

    if df_filtrado.empty:
        return 'No se encontraron recomendaciones para el user_id especificado.'

    # Obtener las recomendaciones y direcciones
    recomendaciones = df_filtrado.iloc[0]['recomendaciones']
    direcciones = df_filtrado.iloc[0]['address_recommend']

    # Crear una lista de recomendaciones con sus direcciones
    recomendaciones_con_direcciones = []
    for recomendacion, direccion in zip(recomendaciones, direcciones):
        recomendacion_con_direccion = f"{recomendacion}, ubicado en; {direccion[0]}, {direccion[1]}"
        recomendaciones_con_direcciones.append(recomendacion_con_direccion)

    return recomendaciones_con_direcciones



#Función para obtener la informacion del usuario
def obtener_informacion(user_id):
    user_id = int(user_id)
    # Filtrar el DataFrame por user_id
    df_filtrado = df[df['user_id'] == user_id]

    if df_filtrado.empty:
        return 'No se encontraron recomendaciones para el user_id especificado.'


    # Obtener el promedio de las estrellas y el número total de reseñas
    promedio_estrellas = df_filtrado.iloc[0]['average_stars']
    total_resenas = df_filtrado.iloc[0]['review_count']

    # Contar el número de reseñas en steakhouses
    numero_resenas_steakhouses = df[df['user_id'] == user_id].shape[0]

    # Crear un diccionario con las recomendaciones, el promedio de estrellas, el número total de reseñas y el número de reseñas en steakhouses
    resultado = {
        'Promedio de Calificación': promedio_estrellas,
        'Reseñas Totales': total_resenas,
        'Reseñas Totales en Steakhouses': numero_resenas_steakhouses
    }

    return resultado



#Funcion para mostrar un mapa de los lugares recomendados
def generar_mapa(user_id):
    user_id = int(user_id)
    mapa = folium.Map()
    nombres = []
    df_usuario = df[df['user_id'] == user_id]
    recomendaciones = df_usuario['recomendaciones'].iloc[0]
    for restaurante in recomendaciones:
        df_restaurante = df[df['name'] == restaurante]
        if not df_restaurante.empty:
            nombre = df_restaurante['name'].iloc[0]
            nombres.append(nombre)
    for index, row in df.iterrows():
        if row['name'] in nombres:
            folium.Marker([row['latitude'], row['longitude']]).add_to(mapa)
    return mapa

#PRUEBA  
 # Obtener el código HTML del mapa de Folium
  #  folium_map_html = mapa._repr_html_()
    
   # return folium_map_html



# Aplicación de Streamlit
def main():
    st.subheader("Obtener Recomendaciones")


    # Entrada del user_id
    user_id = st.text_input('Ingresa el ID del Usuario. Ejemplo: 1')

    
    if st.button('Obtener Recomendaciones'):
        recomendaciones = obtener_recomendaciones(user_id)
        st.write('Recomendaciones:')
        st.write(recomendaciones)
        mapa = generar_mapa(user_id)
       # folium_static(mapa)
# Convertir el mapa de Folium en una imagen
        tmpfile = BytesIO()
        mAPA.save(tmpfile, format='png')
        tmpfile.seek(0)

# Mostrar la imagen en Streamlit
        st.image(tmpfile, width=700)

# Cerrar el archivo temporal
        tmpfile.close()





 
     #PRUEBA
        #folium_map_html = mapa._repr_html_()

# Mostrar el mapa en Streamlit como HTML
      #  st.write(folium_map_html, unsafe_allow_html=True)

#PRUEBA
   # if st.button('Obtener Recomendaciones'):
      #  user_id = obtener_user_id()  # Lógica para obtener el ID del usuario
    #    recomendaciones = obtener_recomendaciones(user_id)
     #   st.write('Recomendaciones:')
      #  st.write(recomendaciones)
       # generar_mapa(user_id)


 
    if st.button('Obtener informacion'):
        informacion = obtener_informacion(user_id)
        st.write('Recomendaciones:')
        st.write(informacion)


if __name__ == '__main__':
    main()
