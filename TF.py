# Primer instalamos streamlit
import streamlit as st # Permite construir la página web
import pandas as pd # Permitira leer las bases de datos
import folium # Permite crear mapas
from streamlit_option_menu import option_menu # Permite generar menus visuales
from streamlit_folium import st_folium # Permite generarlos mapas dentro de la página web de Streamlit.

# Menú vertical en una barra lateral
# Crea una barra lateral (sidebar) en la aplicación.
with st.sidebar:
    with st.expander("Selecciona una sección", expanded=True):
        opciones = option_menu (
            menu_title=None, 
            options=['Presentación', 'Discografía', 'Filmografía', 'Game', 'Estadísticas'], 
            icons=['suit-heart-fill', 'suit-heart-fill', 'suit-heart-fill', 'suit-heart-fill', 'suit-heart-fill'], 
            default_index=0)

if opciones == 'Presentación':
    st.markdown("<h1 style='text-align: center;'>One More Espresso</h1>", unsafe_allow_html=True)
    # Muestra un título principal utilizando HTML -> st.markdown("...", unsafe_allow_html=True)
    # La etiqueta <h1> define un encabezado de nivel 1 -> "<h1 ...>...</h1>"
    # El estilo CSS 'text-align: center' centra el texto -> style='text-align: center;'
    # unsafe_allow_html=True permite que Streamlit interprete y renderice el código HTML incluido en la cadena

    st.image ("Sabrina_Carpenter_Grammys.webp", caption="Sabrina Carpenter - Grammys 2026", use_container_width=True)
    
   # Define una cadena de texto multilínea que contiene una guía para redactar una presentación personal.
    texto = """
    Aquí escribe una presentación sobre el blog
    """
    # Mostramos el texto de presentación debajo de la imagen utilizando HTML
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{texto}</div>", unsafe_allow_html=True)


elif opciones == 'Discografía':
    st.markdown("<h1 style='text-align: center;'>Álbums, Sensillos y más</h1>", unsafe_allow_html=True)

    df_discografia = pd.read_excel("Musica_BD.xlsx")
    lista_lanzamientos = list(df_discografia["Music_releases"].unique())[0:149]
    
    # Agrupaciones generales del álbum
    Fecha = df_discografia.groupby("Music_releases")["Año"].first()
    grupo_canciones = df_discografia.groupby('Music_releases')['canciones'].count()
    portadas_lanzamientos = df_discografia.groupby('Music_releases')['portada_link'].first()
    disqueras_lanzamientos = df_discografia.groupby('Music_releases')['Disquera'].first()

    disco_seleccionado = st.selectbox("Selecciona un lanzamiento musical:", lista_lanzamientos)

    st.write("---")
    canciones_filtradas = df_discografia[df_discografia["Music_releases"] == disco_seleccionado]
    
    # Variables de la cabecera superior del álbum
    nombre_disco = disco_seleccionado
    año_disco = Fecha.loc[nombre_disco]
    canciones_total = grupo_canciones.loc[nombre_disco]
    portada_disco = portadas_lanzamientos.loc[nombre_disco]
    disquera_disco = disqueras_lanzamientos.loc[nombre_disco]
        
    with st.container():
        col1, col2 = st.columns(2) 
        with col1:
            st.markdown(f"""
            <h2 style='margin-top: 0;'>{nombre_disco}</h2>
            <p style='font-size: 18px;'>
                <b>Lanzamiento:</b> {nombre_disco}<br>
                <b>Año:</b> {año_disco}<br>
                <b>Disquera:</b> {disquera_disco}<br>
                <b>Total de canciones:</b> {canciones_total}
            </p>
            """, unsafe_allow_html=True)
        with col2:
            st.image(portada_disco, use_container_width=True)
    
    st.write("---")
    st.markdown("Lista de Canciones")
    
    # Ciclo para iterar y mostrar los datos de cada canción
    for cancion in canciones_filtradas.itertuples():
        nombre_cancion = cancion.canciones 
        genero_cancion = cancion.genero
        duracion_cancion = cancion.duracion
        enlace_spotify = cancion.Link_spotify

# Convierte a texto y extrae solo los primeros 5 caracteres (los minutos y segundos)
        duracion_cancion = str(cancion.duracion)[:5]
        
        with st.container():
            st.markdown(f"""
            <h4><b>{nombre_cancion}</b></h4>
            <ul style='list-style-type: none; padding-left: 10px;'>
                <li><b>Género:</b> {genero_cancion}</li>
                <li><b>Duración:</b> {duracion_cancion}</li>
            </ul>
            """, unsafe_allow_html=True)
            
            # Ajuste de columnas: Ahora solo reservamos un espacio pequeño para el botón de Spotify
            # El segundo espacio vacío ([1, 4]) evita que el botón se estire feo por toda la pantalla
            btn_col, _ = st.columns([1, 4]) 
            with btn_col:
                st.link_button("Spotify", url=enlace_spotify, use_container_width=True)
            
            st.write("") 
            st.divider()



elif opciones == 'Filmografía':
    st.markdown("<h2 style='text-align: center;'>Carrea Actoral</h2>", unsafe_allow_html=True)

    texto_actriz = """
    Sabrina Carpenter ha construido una carrera actoral polifacética y en constante evolución desde muy joven. 
    Comenzó con participaciones memorables en series de televisión y alcanzó gran popularidad internacional gracias a su papel protagónico en Disney Channel. 
    Posteriormente, demostró su madurez interpretativa liderando largometrajes cinematográficos, producciones musicales en formato corto y prestando su voz para universos animados, consolidándose como una artista integral en la industria del entretenimiento.
    """

    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_actriz}</div>", unsafe_allow_html=True)

    st.write("---")

    # Carga de datos de películas
    df_filmografia = pd.read_excel("Filmografía_BD.xlsx")

    seccion_seleccionada = st.selectbox("Selecciona una sección para ver sus producciones:", ["Películas", "Series", "Otros"])

    st.write("---")


    if seccion_seleccionada == "Películas":  # Filtra filas que contengan 'peli' en Producciones_tipo
        producciones_filtradas = df_filmografia[df_filmografia["Producciones_tipo"].str.lower().str.contains("peli", na=False)]
    elif seccion_seleccionada == "Series":  # Filtra filas exactas que digan 'serie'
        producciones_filtradas = df_filmografia[df_filmografia["Producciones_tipo"].str.lower() == "serie"]
    else:  # Sección 'Otros', Ahora busca la palabra exacta "otros", igual que con las Series
        producciones_filtradas = df_filmografia[df_filmografia["Producciones_tipo"].str.lower() == "otros"]


    for proyecto in producciones_filtradas.itertuples():
        # Mapeo exacto de las columnas que solicitaste
        nombre_proyecto = proyecto.Producciones
        año_proyecto = proyecto.Año
        genero_proyecto = proyecto.Género
        duracion_proyecto = proyecto.Duración_minutos
        participacion_proyecto = proyecto.Participación
        personaje_proyecto = proyecto.Personaje
        portada_proyecto = proyecto.Link_portada

        with st.container():
            col1, col2 = st.columns(2)  # Dos columnas por proyecto
            with col1:
                st.markdown(
                    f"""
                <h4><b>{nombre_proyecto}</b></h4>
                <ul style='list-style-type: none; padding-left: 10px;'>
                    <li><b>Año:</b> {año_proyecto}</li>
                    <li><b>Género:</b> {genero_proyecto}</li>
                    <li><b>Duración:</b> {duracion_proyecto} min</li>
                    <li><b>Participación:</b> {participacion_proyecto}</li>
                    <li><b>Personaje:</b> {personaje_proyecto}</li>
                </ul>
                """,
                    unsafe_allow_html=True)
            with col2:
                # La imagen se muestra al lado derecho, justo como en tu discografía
                st.image(portada_proyecto, use_container_width=True)

            st.divider()  # Línea de separación sutil entre cada producción


elif opciones == 'Game':
    st.markdown("<h2 style='text-align: center;'>¡Ahora de jugar!</h2>", unsafe_allow_html=True)   

    texto_recomendacion = """
    Recomendación: Si es tu primer acercamiento a la carrera artistica de Sabrina Carpenter revisa la sección de filmografía
    antes de empezar a jugar. Ten en cuenta que los títulos estan en el idioma original, en este caso la mayoria estan en inglés. Mucha suerte!!!!
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_recomendacion}</div>", unsafe_allow_html=True)
    st.write("---") 
        
    # Importamos la líbrería random
    import random
    
    # Creamos una lista
    lista_producciones = ["Law & Order: Special Victims Unit", "Just Dance Kids 2", "Phineas and Ferb", "The Unprofessional", "The Goodwin Games", 
                       "Orange Is the New Black", "Horns", "Austin & Ally", "Wander Over Yonder", "Walk the Prank", "Adventure in Babysitting", "Girls Meets World", 
                      "Soy Luna", "Mickey and the Roadster Racers", "Sofia the First", "The Short History of the Long Road", "Milo Murphy's Law", "Tall Girl", "Royalties", 
                      "Work It", "Clouds", "Emergency", "Tall Girl 2", "That's Not How This Works (short film)", "A Nonsense Christmas with Sabrina Carpenter", 
                      "Saturday Night Live", "Taylor Swift: The End of an Era", "The Muppet Show", "Confessions II - The Film"]
    
    
    # 2. INICIALIZACIÓN SEGURA DEL ESTADO DE LA SESIÓN
    if "produccion_secreta" not in st.session_state:
        st.session_state.produccion_secreta = random.choice(lista_producciones)
    if "producciones_adivinadas" not in st.session_state:
        st.session_state.producciones_adivinadas = []
    if "intentos" not in st.session_state:
        st.session_state.intentos = 0
    if "intentos_maximos" not in st.session_state:
        st.session_state.intentos_maximos = 3
    
    # Asignación a variables locales para facilitar la lectura
    intentos_maximos = st.session_state.intentos_maximos
    produccion_secreta = st.session_state.produccion_secreta
    
    # 3. INTERFAZ LATERAL (Muestra estadísticas de forma estática)
    st.sidebar.markdown(f"**Intentos fallidos:** {st.session_state.intentos} / {intentos_maximos}")
    st.sidebar.markdown(f"**Letras probadas:** {', '.join(st.session_state.producciones_adivinadas)}")
    
    # 4. CONSTRUCCIÓN DE LA PALABRA OCULTA
    palabra_mostrada = ""
    for letra in produccion_secreta:
        if not letra.isalpha(): 
            palabra_mostrada += letra + " "  # Muestra espacios, números y símbolos directamente
        elif letra.lower() in st.session_state.producciones_adivinadas:
            palabra_mostrada += letra + " "
        else:
            palabra_mostrada += "_ "
    
    st.subheader("Adivina la producción cinematográfica o televisiva:")
    st.markdown(f"### {palabra_mostrada}")
    
    # 5. CONTROL DE FIN DE JUEGO O ENTRADA DE DATOS
    if st.session_state.intentos >= intentos_maximos:
        st.error(f"💥 ¡Game Over! Agotaste tus {intentos_maximos} intentos. La producción era: **{produccion_secreta}**")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("SC_gif_2.gif", caption="¡Inténtalo de nuevo!", width=400)
    
    elif "_" not in palabra_mostrada:
        st.success("🎉 ¡Felicidades! ¡Has adivinado la producción con éxito!")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("SC_gif.gif", caption="¡Eres excelente!", width=400)
    
    else:
        # INPUT TRADICIONAL SIN FORMULARIO (Elimina problemas de recarga en cascada)
        intento = st.text_input("Adivina una letra (escribe y presiona Enter):", max_chars=1, key="input_letra")
    
        if intento:
            letra_ingresada = intento.lower()
            
            # Validación de caracteres válidos
            if not letra_ingresada.isalpha():
                st.warning("Por favor, ingresa una sola letra válida.")
            elif letra_ingresada in st.session_state.producciones_adivinadas:
                st.info("Ya probaste esa letra.")
            else:
                # Guardamos la letra en la lista global
                st.session_state.producciones_adivinadas.append(letra_ingresada)
                
                # Evaluamos si falló o acertó
                if letra_ingresada in produccion_secreta.lower():
                    st.toast("¡Bien hecho! Letra correcta.", icon="✅")
                else:
                    st.session_state.intentos += 1
                    st.toast("Letra incorrecta.", icon="❌")
                
                # Limpiamos el input forzando una recarga limpia para refrescar la interfaz
                st.rerun()
    
    # 6. BOTÓN DE REINICIO
    st.markdown("---")
    if st.button("🔄 Reiniciar Juego / Siguiente Palabra"):
        st.session_state.produccion_secreta = random.choice(lista_producciones)
        st.session_state.producciones_adivinadas = []
        st.session_state.intentos = 0
        st.rerun()


elif opciones == 'Estadísticas':
    st.markdown("<h2 style='text-align: center;'>Gráficos y demás</h2>", unsafe_allow_html=True)   
   
    texto_detalles = """
    Comparativa del éxito de las canciones de Sabrina Carpenter, tanto suyas como en las que participo, fromando parte de la disqueda Hollywood Records e 
    Islando Records segun las vistas de cada canción. 
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_detalles}</div>", unsafe_allow_html=True)
    st.write("---") 
    
    import matplotlib.pyplot as plt
    # 1. Carga de datos
    df_comparativa = pd.read_excel("Musica_BD.xlsx")
    
    # Convertimos a texto y eliminamos posibles comas de miles que confundan a Python
    df_comparativa['vistas_yt'] = df_comparativa['vistas_yt'].astype(str).str.replace(',', '', regex=False)
    
    # Conversión numérica limpia
    df_comparativa['vistas_yt'] = pd.to_numeric(df_comparativa['vistas_yt'], errors='coerce')
    df_comparativa = df_comparativa.dropna(subset=['vistas_yt', 'Disquera'])
    
    # --- CORRECCIÓN EXTRA DE SEGURIDAD ---
    if df_comparativa['vistas_yt'].mean() < 100:
        df_comparativa['vistas_yt'] = df_comparativa['vistas_yt'] * 1000
    
    # 2. LÓGICA: Agrupar por Disquera y sacar el promedio de vistas_yt
    promedio_vistas_disquera = df_comparativa.groupby('Disquera')['vistas_yt'].mean()
    
    # --- FILTRO EXCLUSIVO PARA DOS DISQUERAS ---
    # Convertimos el resultado a DataFrame para poder filtrar por el nombre de la disquera
    df_filtrado = promedio_vistas_disquera.reset_index()
    
    # Filtramos para quedarnos UNICAMENTE con Hollywood Records e Island Records
    disqueras_a_comparar = ["Hollywood Records", "Island Records"]
    df_filtrado = df_filtrado[df_filtrado['Disquera'].isin(disqueras_a_comparar)]
    
    # Volvemos a poner 'Disquera' como índice y ordenamos de mayor a menor
    promedio_dos_disqueras = df_filtrado.set_index('Disquera')['vistas_yt'].sort_values(ascending=False)
    # --------------------------------------------
    
    # --- ESCALA A MILES ---
    promedio_dos_disqueras = promedio_dos_disqueras / 1000
    
    # Creamos la figura explícitamente para Streamlit (Tamaño 8, 5 para que no sea tan gigante al ser solo 2 barras)
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Dibujamos las barras verticales (puedes usar un color llamativo)
    promedio_dos_disqueras.plot(kind='bar', ax=ax, color='#6C5CE7', width=0.4) # Reducimos width a 0.4 para que las 2 barras no se vean tan anchas
    
    # [CORRECCIÓN 1] Eliminamos los bordes superior, derecho e izquierdo de la caja
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Suavizamos el borde inferior (eje X) pasándolo a un gris muy sutil
    ax.spines['bottom'].set_color('#DCDDE1')
    
    # [CORRECCIÓN 2] Suavizamos la cuadrícula horizontal reduciendo alpha a 0.2 y aclarando el color
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#636E72')
    
    # [CORRECCIÓN 3] Enviamos la cuadrícula al fondo
    ax.set_axisbelow(True)
    
    # Agregamos título al gráfico
    plt.title('Comparativa: Hollywood Records vs Island Records', fontsize=13, fontweight='bold', color='#2D3436', pad=15)
    # Etiqueta del eje X
    plt.xlabel('Disquera', fontsize=10, color='#636E72', labelpad=10)
    # Etiqueta del eje Y
    plt.ylabel('Promedio de vistas obtenidas (en miles)', fontsize=10, color='#636E72', labelpad=10)
    
    # Estilizamos los nombres de los ejes (Al ser solo 2 nombres, rotación 0 es más estético)
    plt.xticks(rotation=0, fontsize=10, color='#2D3436')
    plt.yticks(fontsize=9, color='#636E72')
    ax.tick_params(axis='y', left=False) 
    ax.tick_params(axis='x', colors='#DCDDE1')
    
    # Quitamos el fondo blanco rígido para acoplarse al tema de Streamlit
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    # Ajustamos automáticamente los espacios
    plt.tight_layout()
    
    # 3. RENDERIZADO EN STREAMLIT:
    st.pyplot(fig)

    st.markdown("---")

    texto_locacion = """
    Lugares en donde se grabaron los videos musicales de Sabrina Carpenter.
    Dato curioso: La mayoria de sus videos se grabaron en Los Ángeles, Californa. Al ser grabaciones cerradas, se desconocer el lugar específico en el cual se
    realizaron, mayoritariamente.
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_locacion}</div>", unsafe_allow_html=True)
    st.write("---") 
   
    # 1. Carga directa de los datos (sin st.cache_data)
    df_musica = pd.read_excel("Musica_BD.xlsx")

    # 2. Extracción y limpieza para el mapa (coordenadas únicas)
    # Quitamos filas vacías y eliminamos duplicados en las coordenadas
    df_mapa = df_musica[['Grabación_lugar', 'Coordenadas']].dropna().drop_duplicates(subset=['Coordenadas'])

    st.subheader("Ubicaciones de Grabación")

    # Crear el mapa base de Folium
    mapa = folium.Map(location=[15.0, -30.0], zoom_start=2)

     Recorrer las filas limpiando los paréntesis antes de separar
    for _, fila in df_mapa.iterrows():
        try:
            # Convertimos a texto y eliminamos los paréntesis '(' y ')' si existen
            coor_limpia = str(fila['Coordenas']).replace('(', '').replace(')', '')
            
            # Ahora sí separamos por coma y convertimos a número
            lat, lon = map(float, coor_limpia.split(','))
            
            contenido = f"<b>Lugar:</b> {fila['Grabación_lugar']}"
            folium.Marker(location=[lat, lon], popup=folium.Popup(contenido, max_width=300), icon=folium.Icon(color='cadetblue', icon='music')).add_to(mapa)
       
    # Mostrar el mapa interactivo en Streamlit
    st_folium(mapa, width=1000, height=500, returned_objects=[])

    st.markdown("---")

    # 3. Sección de canciones con videoclip (MV) debajo del mapa
    st.subheader("Buscador de Videoclips")

    # Filtramos las canciones que tienen un link de video válido
    df_videos = df_musica[['canciones', 'MV', 'Link_mv']].dropna(subset=['Link_mv'])

    if not df_videos.empty:
        # Menú desplegable con las canciones únicas que tienen video
        cancion_seleccionada = st.selectbox("Selecciona una canción para ver su videoclip:", options=df_videos['canciones'].unique())

        # Extraemos la información de la canción seleccionada
        info_cancion = df_videos[df_videos['canciones'] == cancion_seleccionada].iloc[0]

        # Mostramos los datos en pantalla
        st.write(f"**Canción:** {info_cancion['canciones']}")
        st.write(f"**Detalle del MV:** {info_cancion['MV']}")
        
        # Enlace directo para abrir el video
        st.markdown(f"[➡️ Ver Videoclip en este enlace]({info_cancion['Link_mv']})")
    else:
        st.warning("No se encontraron canciones con enlaces de videoclips en el archivo.")


   




    







