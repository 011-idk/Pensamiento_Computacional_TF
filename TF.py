# Primer instalamos streamlit e importamos lo necesario para iniciar el programa
import streamlit as st # Permite construir la página web
import pandas as pd # Permitira leer las bases de datos
import folium # Permite crear mapas
from streamlit_option_menu import option_menu # Permite generar menus visuales
from streamlit_folium import st_folium # Permite generarlos mapas dentro de la página web de Streamlit.

# Creamos el menú como barra lateral (sidebar) en la aplicación.
with st.sidebar:
    with st.expander("Selecciona una sección", expanded=True): #Utilizamos st.expander para que el menu pueda ocultarse o mostrarse
        opciones = option_menu (
            menu_title=None, # Utilizamos None para que no aparesca el titulo/encabezado del menú
            options=['Presentación', 'Discografía', 'Filmografía', 'Game', 'Espresso'], 
            icons=['suit-heart-fill', 'suit-heart-fill', 'suit-heart-fill', 'suit-heart-fill', 'suit-heart-fill'], #Repetimos los iconos
            default_index=0)

if opciones == 'Presentación': # Con bucle if creamos la primera seccione del menú lateral
    st.markdown("<h1 style='text-align: center;'>One More Espresso</h1>", unsafe_allow_html=True) # Muestra un título principal utilizando HTML 
    st.image ("Sabrina_Carpenter_Grammys.webp", caption="Sabrina Carpenter - Grammys 2026", use_container_width=True)
    # Ponemos la imagen primero escribiendo el nombre del la misma ubicada en el repositorio, utilizando use_container_width=True para que abarque el ancho disponible.
    
   # Definimos una cadena de texto multilínea con guía para redactar una presentación sobre el la página
    texto = """
    ¡Bienvenidos! Este blog está dedicado a conocer y explorar la trayectoria de Sabrina Carpenter, tanto en su faceta como actriz como en su carrera musical. Aquí encontrarás información sobre
    su discografía desde sus inicos hasta los últimos lanzamientos, así como de sus películas y series más recordadas o que quiza no conocias.
    Este blog está organizado en diferentes secciones. En la sección de Discografía encontraras una compilación de las canciones de Sabrina Carpenter, etres albums, sensillos y demás. En la 
    sección de Filmografía encontrarás información sobre los productos audiovisuales en los que ha participado tanto peliculas, series, incluso especiales de TV. También esta la sección Games en 
    donde podrás jugar el famoso juego del ahorcado basado en las producciones en las que ha participado la artista. Finalmente tenemos la sección Espresso, en la cual podrás encontrar un grafico comparativo, 
    un mapa interactivo, y podrás ver elegir entre videoclips de las canciones de Sabrina Carpenter e ir directo a verlos.
    Espero que disfrutes recorriendo este espacio y que encuentres información interesante sobre una de las artistas más destacadas de su generación. ¡Gracias!
    """
    # Mostramos el texto de presentación debajo de la imagen utilizando HTML
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{texto}</div>", unsafe_allow_html=True)

    st.write("---") 
    
    texto_bio = """
    Biografía:
    Sabrina Carpenter (nacida el 11 de mayo de 1999 en Pensilvania) es una cantante, compositora y actriz estadounidense que se ha consolidado como 
    una de las mayores estrellas del pop actual. Comenzó su carrera como actriz infantil, logrando su salto a la fama al interpretar a Maya Hart en la 
    serie de Disney Channel Girl Meets World (2014-2017), para luego expandir su faceta actoral en películas. Aunque hacía música desde la adolescencia, 
    su verdadera revolución musical llegó en 2022 con el álbum Emails I Can't Send, aclamado por su composición íntima y vulnerable. Ese mismo año, su 
    popularidad se disparó a nivel mundial tras ser la telonera oficial de Taylor Swift en el fenómeno global The Eras Tour. Posteriormente, alcanzó el 
    estatus de superestrella global con su álbum Short n' Sweet, un disco que rompió récords en las listas de éxitos gracias a sencillos virales y masivos 
    como Espresso, Please Please Please y Taste, los cuales definen su estilo actual caracterizado por un pop pegadizo, letras atrevidas y una estética 
    retro muy marcada.
    """
    # Mostramos el texto de presentación debajo de la imagen utilizando HTML
    st.markdown(f"<div style='text-align: justify; font-size: 18px;'>{texto_bio}</div>", unsafe_allow_html=True)


elif opciones == 'Discografía': # Creamos la sección de Discografía 
    st.markdown("<h1 style='text-align: center;'>Álbums, Sensillos y más</h1>", unsafe_allow_html=True)

    df_discografia = pd.read_excel("Musica_BD.xlsx") # Importamos y leemos la primera base de datos de excel nombrada Musica_DB.xlsx
    lista_lanzamientos = list(df_discografia["Music_releases"].unique())[0:149] #Creamos una lista unicamente con los datos de la columna seleccionada
    
    # Creamos una lista unicamente con los datos de la columna seleccionada
    # Hacemos una agrupación general de los datos de la columna previamente seleccionada Music_releases
    Fecha = df_discografia.groupby("Music_releases")["Año"].first()
    # .first es utilizado para que de todas las filas que compartan el mismo nombre se tomen unicamente el primer valor que encuentre en la columna "Año"
    grupo_canciones = df_discografia.groupby("Music_releases")["canciones"].count()
    # count para determinar la cantidad de canciones pertenecientes a cada titulo de la columna Music_releases, los mismo en los demás casos
    portadas_lanzamientos = df_discografia.groupby("Music_releases")["portada_link"].first()
    disqueras_lanzamientos = df_discografia.groupby("Music_releases")["Disquera"].first()
    
    disco_seleccionado = st.selectbox("Selecciona un lanzamiento musical:", lista_lanzamientos)  # Creamos una especie de subsección
    
    st.write("---")  # Utilizada como linea divisora en pantalla
    canciones_filtradas = df_discografia[df_discografia["Music_releases"] == disco_seleccionado]  # Filtramos las canciones de la columna conciones
    
    # Variables de los lanzamientos
    nombre_disco = disco_seleccionado
    año_disco = Fecha.loc[nombre_disco]  # . loc nos permitira buscar información basándose en el nombre de la etiqueta o fila.
    canciones_total = grupo_canciones.loc[nombre_disco]
    portada_disco = portadas_lanzamientos.loc[nombre_disco]
    disquera_disco = disqueras_lanzamientos.loc[nombre_disco]
    
    with st.container():
        col1, col2 = st.columns(2)  # Hacemos dos columnas
        with col1:  # La primera columna contiene los datos generales antes extraidos
            st.markdown(
                f"""
            <h2 style='margin-top: 0;'>{nombre_disco}</h2>
            <p style='font-size: 18px;'>
                <b>Lanzamiento:</b> {nombre_disco}<br>
                <b>Año:</b> {año_disco}<br>
                <b>Disquera:</b> {disquera_disco}<br>
                <b>Total de canciones:</b> {canciones_total}
            </p>
            """,
                unsafe_allow_html=True)
            
        with col2:  # La segunda columna contiene la imagen del lanzamiento
            st.image(portada_disco, use_container_width=True)
    
    st.write("---")
    st.markdown("Lista de Canciones")
    
    # Ahora procedemos con la lista de canciones de cada lanzamiento
    # Recorremos cada canción del disco seleccionado (usando .itertuples() de Pandas)
    for cancion in canciones_filtradas.itertuples():
        nombre_cancion = cancion.canciones
        genero_cancion = cancion.genero
        duracion_cancion = cancion.duracion
        enlace_spotify = cancion.Link_spotify
    
        # NUEVO CAMBIO: Extraemos el enlace de la columna Link_letras
        enlace_letras = cancion.Link_letras
    
        # Convertimos a texto los datos de la columa duracion y extraemos solo los primeros 5 caracteres (los minutos y segundos)
        duracion_cancion = str(cancion.duracion)[:5]
    
        with st.container():  # Creamos un contenedor que agrupe los elementos
            st.markdown(
                f"""
            <h4><b>{nombre_cancion}</b></h4>
            <ul style='list-style-type: none; padding-left: 10px;'>
                <li><b>Género:</b> {genero_cancion}</li>
                <li><b>Duración:</b> {duracion_cancion}</li>
            </ul>
            """,
                unsafe_allow_html=True)
    
            # Creamos un diseño para dos botones alineados
            # Creamos dos columnas iguales para botones y un espacio vacío grande a la derecha
            btn_spotify, btn_letras, _ = st.columns([1, 1, 3])
    
            with btn_spotify:
                st.link_button("Spotify 🎧", url=enlace_spotify, use_container_width=True)
    
            with btn_letras:
                # Validamos que el enlace exista en Excel antes de mostrar el botón
                if pd.notna(enlace_letras):
                    st.link_button("Ver Letra 🎤", url=enlace_letras, use_container_width=True)
                else:
                    # Si la celda está vacía, muestra un botón deshabilitado o un mensaje sutil
                    st.button("No disponible", disabled=True, use_container_width=True)
    
            st.write("")  # Generamos un salto de linea
            st.divider()  # Generamos una línea horizontal que cruza la pantalla



elif opciones == 'Filmografía': # Creamos la sección de Filmografía
    st.markdown("<h2 style='text-align: center;'>Carrea Actoral</h2>", unsafe_allow_html=True)
#Creamos un texto introductorio a esta sección
    texto_actriz = """
    Sabrina Carpenter inicio en el mundo de la actuación a la edad de 11 años y desde entonces ha  participado en diversas producciones audiovisuales, 
    contruyendo un carrera actoral polifacética y en constante evolución. Sus primeras participaciones se dieron en series de televisión, más no fue hasta entrar a
    Disney que alcanzó gran popularidad internacional. Esto la a consolidado como una artista integral en la industria del entretenimiento.
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_actriz}</div>", unsafe_allow_html=True)

    st.write("---")

    # Leemos y extraemos los datos de la segunda base de datos nombrada Filmografía_BD.xlsx
    df_filmografia = pd.read_excel("Filmografía_BD.xlsx")
    #Creamos una especie de sub sección que se divida en tres tipos de productos
    seccion_seleccionada = st.selectbox("Selecciona una sección para ver sus producciones:", ["Películas", "Series", "Otros"])

    st.write("---") # Genemos una linea divisoria

    #Utilizamos el bucle if para la sub sección
    if seccion_seleccionada == "Películas":  # Filtra filas que contengan 'peli' en Producciones_tipo
        #Filtramos los datos de las columnas Producciones_tipo cuyos datos de sividen en la categoria de Peliculas, Series y Otros
        producciones_filtradas = df_filmografia[df_filmografia["Producciones_tipo"].str.lower().str.contains("peli", na=False)]
    elif seccion_seleccionada == "Series":  # Filtra filas exactas que digan 'serie'
        producciones_filtradas = df_filmografia[df_filmografia["Producciones_tipo"].str.lower() == "serie"]
    else:  # Sección 'Otros', Ahora busca la palabra exacta "otros", igual que con las Series
        producciones_filtradas = df_filmografia[df_filmografia["Producciones_tipo"].str.lower() == "otros"]

    # Recorremos las filas de los datos filtrados de las producciones
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
            col1, col2 = st.columns(2)  # Greamos dos columnas por proyecto
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
                # Hacemos que la imagen se muestre del lado derecho, así como con la sección en discografía
                st.image(portada_proyecto, use_container_width=True)

            st.divider()  # Creamos una línea de separación sutil entre cada producción


elif opciones == 'Game': # Creamos la sección Games
    st.markdown("<h2 style='text-align: center;'>¡Ahora de jugar!</h2>", unsafe_allow_html=True)   
    # Creamos un texto introductorio a la sección
    texto_recomendacion = """
    Recomendación: Si es tu primer acercamiento a la carrera artistica de Sabrina Carpenter revisa la sección de filmografía
    antes de empezar a jugar. Ten en cuenta que los títulos estan en el idioma original, en este caso la mayoria estan en inglés. Mucha suerte!!!!
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_recomendacion}</div>", unsafe_allow_html=True)
    st.write("---") 
    # Iniciamos la crreación del juego El Ahorcado con la Filmografía de Sabrina Carpenter
    # Primero importamos la líbrería random
    import random
    
    # Creamos una lista con los nombres de las producciones
    lista_producciones = ["Law & Order: Special Victims Unit", "Just Dance Kids 2", "Phineas and Ferb", "The Unprofessional", "The Goodwin Games", 
                       "Orange Is the New Black", "Horns", "Austin & Ally", "Wander Over Yonder", "Walk the Prank", "Adventure in Babysitting", "Girls Meets World", 
                      "Soy Luna", "Mickey and the Roadster Racers", "Sofia the First", "The Short History of the Long Road", "Milo Murphy's Law", "Tall Girl", "Royalties", 
                      "Work It", "Clouds", "Emergency", "Tall Girl 2", "That's Not How This Works (short film)", "A Nonsense Christmas with Sabrina Carpenter", 
                      "Saturday Night Live", "Taylor Swift: The End of an Era", "The Muppet Show", "Confessions II - The Film"]
    
    
    # Utilizamos bucle if y st.session_state para comprovar si es la primera vez que se inicia una partida
    if "produccion_secreta" not in st.session_state:
        st.session_state.produccion_secreta = random.choice(lista_producciones) #Generamos algun dato al azar de lista_producciones
    if "producciones_adivinadas" not in st.session_state:
        st.session_state.producciones_adivinadas = [] #Se guardan las veces que se a adivinado alguna letra
    if "intentos" not in st.session_state:
        st.session_state.intentos = 0 #Inicia con una cantidad de intentos de 0
    if "intentos_maximos" not in st.session_state:
        st.session_state.intentos_maximos = 3 # Marcamos un limite de intentos, en este caso 3
    
    # Le asignamos variables para facilitar la lectura
    intentos_maximos = st.session_state.intentos_maximos
    produccion_secreta = st.session_state.produccion_secreta
    
    # Mostramos la cantidad de intentos fallidos y las letras que fueron utilizadad
    st.sidebar.markdown(f"**Intentos fallidos:** {st.session_state.intentos} / {intentos_maximos}")
    st.sidebar.markdown(f"**Letras probadas:** {', '.join(st.session_state.producciones_adivinadas)}")
    
    # Construcción de la palabra oculta
    palabra_mostrada = ""
    for letra in produccion_secreta:
        if not letra.isalpha(): 
            palabra_mostrada += letra + " "  # Muestra espacios, números y símbolos directamente
        elif letra.lower() in st.session_state.producciones_adivinadas:
            palabra_mostrada += letra + " "
        else:
            palabra_mostrada += "_ "
    
    st.subheader("Adivina la producción cinematográfica o televisiva:") # El emnsaje inicial que indica la dinamica del juego
    st.markdown(f"### {palabra_mostrada}")
    
    # Control del fin del juego o entrada de datos
    if st.session_state.intentos >= intentos_maximos:
        st.error(f"💥 ¡Game Over! Agotaste tus {intentos_maximos} intentos. La producción era: **{produccion_secreta}**") # Creamos aquello que aparecera en caso falle
    #Creamos tres columnas para queel gif quede centrado
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("SC_gif_2.gif", caption="¡Inténtalo de nuevo!", width=400) #Creamos un mensaje que aparece debajo del gif
    # Lo mismo aplica en el caso que gane, con su respectivo mensaje y gif
    elif "_" not in palabra_mostrada:
        st.success("🎉 ¡Felicidades! ¡Has adivinado la producción con éxito!")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("SC_gif.gif", caption="¡Eres excelente!", width=400)
    
    else:
        # Utilizamos un input  para eliminar los problemas de sobrecarga
        intento = st.text_input("Adivina una letra (escribe y presiona Enter):", max_chars=1, key="input_letra")
    
        if intento:
            letra_ingresada = intento.lower() #Nos aseguramos que las letras ingresadas sena en minusculas
            
            # Validamos los caracteres válidos
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
                
                # Limpiamos el input
                st.rerun()
    
    # Creamos un boton de reinicio de la partida
    st.markdown("---")
    if st.button("🔄 Reiniciar Juego / Siguiente Palabra"): #Estas son las palabras que apareceran en el boton
        st.session_state.produccion_secreta = random.choice(lista_producciones) # Se vuelve a eledir un dato al azar de la lista
        st.session_state.producciones_adivinadas = []
        st.session_state.intentos = 0
        st.rerun()
        #En sintesis, se reinicia la partida


elif opciones == 'Espresso': #Creamos la última sección llamada Espresso
    st.markdown("<h2 style='text-align: center;'>Gráficos y demás</h2>", unsafe_allow_html=True)   
   # Creamos un mensaje introductorio a la sección
    texto_detalles = """
    Comparativa del éxito de las canciones de Sabrina Carpenter, tanto suyas como en las que participo, fromando parte de la disqueda Hollywood Records e 
    Islando Records segun las vistas de cada canción. 
    """
    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_detalles}</div>", unsafe_allow_html=True)
    st.write("---") 
    # Importamos la libreria matplotlib para poder crear un grafico de barras
    import matplotlib.pyplot as plt
    # 1. Carga de datos
    df_comparativa = pd.read_excel("Musica_BD.xlsx")
    
    # Convertimos a texto y eliminamos posibles comas de miles
    df_comparativa['vistas_yt'] = df_comparativa['vistas_yt'].astype(str).str.replace(',', '', regex=False)
    
    # REalizamos una conversión numerica
    df_comparativa['vistas_yt'] = pd.to_numeric(df_comparativa['vistas_yt'], errors='coerce')
    df_comparativa = df_comparativa.dropna(subset=['vistas_yt', 'Disquera'])
    
    # Realizamos una correción extra de seguridad
    if df_comparativa['vistas_yt'].mean() < 100:
        df_comparativa['vistas_yt'] = df_comparativa['vistas_yt'] * 1000
    
    # Agrupamos la columna de Disquera y para sacar el promedio de la columna vistas_yt
    promedio_vistas_disquera = df_comparativa.groupby('Disquera')['vistas_yt'].mean()
    
    # Filtramos los datos exlusivamente de dos disqueras: Hollywood Records e Island Records
    # Convertimos el resultado a DataFrame para poder filtrar por el nombre de la disquera
    df_filtrado = promedio_vistas_disquera.reset_index()
    
    # Filtramos para quedarnos unicamente con Hollywood Records e Island Records
    disqueras_a_comparar = ["Hollywood Records", "Island Records"]
    df_filtrado = df_filtrado[df_filtrado['Disquera'].isin(disqueras_a_comparar)]
    
    # Volvemos a poner 'Disquera' como índice y ordenamos de mayor a menor
    promedio_dos_disqueras = df_filtrado.set_index('Disquera')['vistas_yt'].sort_values(ascending=False)
    
    # Lo ponemos en escala de miles
    promedio_dos_disqueras = promedio_dos_disqueras / 1000
    
    # Creamos la figura 
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Dibujamos las barras verticales
    promedio_dos_disqueras.plot(kind='bar', ax=ax, color='#F5F5BC', width=0.4) # Reducimos width a 0.4 para que las 2 barras no se vean tan anchas
    
    # Eliminamos los bordes superior, derecho e izquierdo de las barras
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Suavizamos el borde inferior (eje X) pasándolo a un gris muy sutil
    ax.spines['bottom'].set_color('#DCDDE1')
    
    # Suavizamos la cuadrícula horizontal 
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#636E72')
    
    # Enviamos la cuadrícula al fondo
    ax.set_axisbelow(True)
    
    # Agregamos título al gráfico
    plt.title('Comparativa: Hollywood Records vs Island Records', fontsize=13, fontweight='bold', color='#2D3436', pad=15)
    # Etiqueta del eje X
    plt.xlabel('Disquera', fontsize=10, color='#636E72', labelpad=10)
    # Etiqueta del eje Y
    plt.ylabel('Promedio de vistas obtenidas (en miles)', fontsize=10, color='#636E72', labelpad=10)
    
    # Estilizamos los nombres de los ejes
    plt.xticks(rotation=0, fontsize=10, color='#2D3436')
    plt.yticks(fontsize=9, color='#636E72')
    ax.tick_params(axis='y', left=False) 
    ax.tick_params(axis='x', colors='#DCDDE1')
    
    # Quitamos el fondo blanco para acoplarse al tema de Streamlit
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    # Ajustamos automáticamente los espacios
    plt.tight_layout()
    
    st.pyplot(fig)

    st.markdown("---")

    #Creamos un texto introductorio a la parte del mapa interactivo
    texto_locacion = """
    Lugares en donde se grabaron los videos musicales de Sabrina Carpenter.
    Dato curioso: La mayoria de sus videos se grabaron en Los Ángeles, Californa. Al ser grabaciones cerradas, se desconocer el lugar específico en el cual se
    realizaron, mayoritariamente.
    """

    st.markdown(f"<div style='text-align: justify; font-size: 18px; margin-bottom: 25px;'>{texto_locacion}</div>", unsafe_allow_html=True)
   
    # Extraemos los datos de la base de datos Musica_BD.xlsx
    df_musica = pd.read_excel("Musica_BD.xlsx")

    # 2. Extracción y limpieza para el mapa (coordenadas únicas)
    # Quitamos las filas vacías y eliminamos duplicados en las coordenadas
    df_mapa = df_musica[['Grabación_lugar', 'Coordenadas']].dropna().drop_duplicates(subset=['Coordenadas'])

    st.subheader("Ubicaciones de Grabación") # Texto a modo de subtitulo

    # Creamos el mapa base de Folium
    mapa = folium.Map(location=[15.0, -30.0], zoom_start=2)

    #Recorremos las filas limpiando los paréntesis antes de separar
    for _, fila in df_mapa.iterrows():
    
        # Convertimos a texto y eliminamos los paréntesis '(' y ')
        coor_limpia = str(fila['Coordenadas']).replace('(', '').replace(')', '')
            
        # Separamos por coma y convertimos a número las coordenadas
        lat, lon = map(float, coor_limpia.split(','))
            
        contenido = f"<b>Lugar:</b> {fila['Grabación_lugar']}"
        folium.Marker(location=[lat, lon], popup=folium.Popup(contenido, max_width=300), icon=folium.Icon(color='cadetblue', icon='music')).add_to(mapa)
       
    # Mostramos el mapa interactivo en Streamlit
    st_folium(mapa, width=1000, height=500, returned_objects=[])

    st.markdown("---")
#Finalmente creamos la sección de canciones con videoclip (MV) debajo del mapa
    st.subheader("Buscador de Videoclips")

    # Filtramos las canciones que tienen un link de video válido
    df_videos = df_musica[['canciones', 'mv', 'Link_mv']].dropna(subset=['Link_mv'])

    if not df_videos.empty:
        # Creamos un menú desplegable con las canciones únicas que tienen video
        cancion_seleccionada = st.selectbox("Selecciona una canción para ver su videoclip:", options=df_videos['canciones'].unique())

        # Extraemos la información de la canción seleccionada
        info_cancion = df_videos[df_videos['canciones'] == cancion_seleccionada].iloc[0]

        # Mostramos los datos en pantalla
        st.write(f"**Canción:** {info_cancion['canciones']}")
        st.write(f"**Detalle del MV:** {info_cancion['mv']}")
        
        # Permitimos un enlace directo para abrir el video
        st.markdown(f"[➡️ Ver Videoclip en este enlace]({info_cancion['Link_mv']})")
