import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import seaborn as sns 
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime 


st.set_page_config(page_title="Global Economy",layout="wide") #configuración de la página


@st.cache_data # maneja el caché de la app

def load_data(): # cargamos los datos y hacemos una copia en la función
    df = pd.read_csv(r'Data/Clean_GEI.csv') 
    df_clean = df.copy()
    return df_clean

data = load_data() # asignamos una variable a la función de carga de datos

# ponemos un PNG en el menú lateral y desplegamos botones para las diferentes opciones
st.sidebar.image(r"Archivos/Logo_European_Central_Bank.svg")
option = st.sidebar.radio( 
    "Select a section:",
    ["Landing", "Analysis", "Dashboard", "Predictor", "Farewell video", "Full dataset"]
)
st.title("World GDP Indicators")


def show_landing(): # función para gestionar la landing 
    # Aplicamos un HTML para cambiar el tamaño de la letra de nuestro texto
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # Aplicamos la clase CSS 'big-font' que hemos creado al texto
    st.markdown('<p class="big-font">At the European Central Bank we have the best analysts for data operations. Our Upgraders team will present the main results on Global Economy Indicators research.</p>', unsafe_allow_html=True)
    with st.expander('Data origin'):
        st.markdown("""
        ### Basic descriptive variables

        <span style="color:#FCB714">Country</span>: Country<br>
        <span style="color:#FCB714">Year</span>: Year<br>
        <span style="color:#FCB714">Population</span>: Population<br>
        <span style="color:#FCB714">Currency</span>: Currency, local currency<br>
        <span style="color:#FCB714">Exchange_Rate</span>: Currency/USD exchange rate, obtained through the IMF; Currencies obtained with 1 dollar<br>

        ### Economic activities

        <span style="color:#FCB714">Agriculture_Hunting_Forestry_Fishing</span>: Sum of the value of agriculture, hunting, forestry and fishing activities; USD<br>
        <span style="color:#FCB714">Construction</span>: Total value of construction activities; USD<br>
        <span style="color:#FCB714">Manufacturing</span>: Total value of natural product processing activities; USD<br>
        <span style="color:#FCB714">Mining_Manufacturing_Utilities</span> : Total value of mining and raw materials processing activities; USD<br>
        <span style="color:#FCB714">Mining_Utilities</span> : Total value of mining and raw materials activities; USD<br>
        <span style="color:#FCB714">Transport_Storage_Communication</span> : Total value of transportation, storage and communications activities; USD<br>
        <span style="color:#FCB714">Wholesale_RetailTrade_Restaurants_Hotels</span> : Total value of wholesale, retail and restaurant activities; USD<br>
        <span style="color:#FCB714">Other_Activities</span> : Other activities; USD<br>

        ### Main macroeconomic indicators

        <span style="color:#FCB714">GNI</span>: Gross National Income (GNI); USD<br>
        <span style="color:#FCB714">GDP</span> : Gross Domestic Product (GDP); USD<br>
        <span style="color:#FCB714">GNI_pc</span> : RNB per capita; USD<br>
        <span style="color:#FCB714">GDP_pc</span> : PIB per capita; USD<br>
        <span style="color:#FCB714">Consumption</span> : Final Consumption Expenditure; USD<br>
        <span style="color:#FCB714">HH_Consumption</span> : Household Consumption Spending and non-profit companies serving households; USD<br>
        <span style="color:#FCB714">GCF</span> : Gross Capital Formation. Sum of GFCF and Inventory Variation; USD<br>
        <span style="color:#FCB714">GFCF</span> : Gross Fixed Capital Formation; USD<br>
        <span style="color:#FCB714">Gov_Consumption</span> : Final Government Consumption Expenditure (education, health, dependency, security, medicines...); USD<br>
        <span style="color:#FCB714">Exports</span> : Sum of the value of exports of goods and services abroad; USD<br>
        <span style="color:#FCB714">Imports</span> : Sum of the value of exports of goods and services from abroad; USD<br>
        <span style="color:#FCB714">Total_Value_Added</span> : Total Added Value; USD<br>
        <span style="color:#FCB714">Inventory_Changes</span> : Inventory Variation; USD<br>

        ### Other economic indicators

        <span style="color:#FCB714">Continent</span>: Country continent<br>
        <span style="color:#FCB714">GDP_growth</span> : GDP growth compared to the previous year; %<br>
        <span style="color:#FCB714">SNE</span> : Net External Balance; USD<br>
        <span style="color:#FCB714">IAC</span> : Commercial Openness Index; %<br>
        <span style="color:#FCB714">TCC</span> : Commercial Coverage Rate; %<br>
        <span style="color:#FCB714">Exp/GDP</span> : Exports in relation to GDP; %<br>
        <span style="color:#FCB714">IDH</span> : Human development Index; data between 0 and 1<br>
        <span style="color:#FCB714">Unemployment</span> : Total unemployment; % From handwork<br>


        Codes [ISIC](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/)
        """, unsafe_allow_html=True)
        
    # Cargamos el CSV donde hemos puesto los paises y las coordenadas
    csv_mapa = r"Data/df_combinado.csv"

    df = pd.read_csv(csv_mapa)
    
    scaleFactor = 0.0005            # Lo usamos para ajustar el tamaño de los puntos en el mapa
    # Establecemos un punto de visión de inicio, con un zoom amplio para ver la tierra al completo
    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=0.1, min_zoom=0.05)

    # Definimos el tipo de vista, habilitamos la interaccion del usuario y definimos el ancho y altura de la vista
    globe_view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)

    layers = [                          # Creamos una capa de datos desde una Url dada por pydeck
        pdk.Layer(
            "GeoJsonLayer",
            id="base-map",
            data="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson",
            stroked=True,                   # Habilitamos para ver las fronteras
            filled=True,                    # Se rellenan los paises con un color base
            get_fill_color=[200, 200, 200],
            get_line_color=[0, 0, 0],       # Asignamos un color al contorno y el ancho de la línea
            line_width_min_pixels=1,
            
        ),
        pdk.Layer(
            "ScatterplotLayer",  # Ponemos una capa de puntos para cada país en función de sus coordenadas
            id="Country",
            data=df.assign(radius=df["Population"] * scaleFactor),  # Asignamos la variable Population para que muestre cada punto y la multiplicamos por el scalefactor para que no sea enorme y se visualice bien
            get_position=["Longitude", "Latitude"],
            get_color=[60, 204, 31],  # Asignamos el color del puntito
            get_radius="radius",  # Ponemos el radio que nos resulte más cómodo para la visualización
            pickable=True,    # Habilitamos la selección de objetos, en este caso los puntitos
            auto_highlight=True,  # Habilitamos el resaltado de los puntitos
        ),
    ]
    # Creamos el contenedor principal con las capas definidas antes y la vista inicial del mapa
    # Con el tooltip le añadimos la info que nos interese sobre el país en cuestión

    deck = pdk.Deck(
        views=[globe_view],
        initial_view_state=view_state,
        tooltip={"html": "<b>Country:</b> {Country}<br><b>GDP per capita:</b> {GDP_pc}<br><b>Population:</b> {Population}"},
        layers=layers,
        map_provider=None,  # Sirve para que el mapa sea opaco
        parameters={"cull": True}  # Mejora el rendimiento descartando objetos fuera de la vista
    )
    st.pydeck_chart(deck) # Necesario para visualizarlo en streamlit
    
    st.write('Interactive map with the latest data on GDP per capita and population for each country ')

        
def analisis(): #función para mostrar un conjunto de gráficas en formato matriz 
    st.title("Graphics")

    col1, col2 = st.columns(2)

    # Primera fila con dos gráficas
    with col1:
        # Creamos un mapeado de color por continentes
        continent_colors = {
        "Africa": "#FCB714",
        "Asia": "#ee82ee",
        "Europe": "#001489",
        "North America": "#00FFBC",
        "Oceania": "#2ca02c",
        "South America": "#cd853f"
    }
        # Creamos el conjunto de datos con el que vamos a trabajar, en este caso el crecimiento promedio del PIB por continente
        df2 = data.groupby(["Year","Continent"])["GDP_growth"].mean().reset_index()

        # Graficamos con Plotly Express
        fig = px.line(df2, x="Year", y="GDP_growth", color="Continent", 
                    title="GDP growth rate by continent, in % of previous year (1970-2021)",
                    labels={"GDP_growth": "GDP growth rate",},
                    color_discrete_map=continent_colors)

        # Ajustamos un poco los ejes
        fig.update_layout(title_font_color="black", legend_title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black", legend_font_color="black")
        fig.update_xaxes(tickfont=dict(color="black"))
        fig.update_yaxes(tickfont=dict(color="black"))

        st.plotly_chart(fig)

    with col2:
    
        ZonaEuro = data[data["Currency"] == "Euro"].drop(columns=["Currency"])      # Agrupamos la zona euro en función de la moneda €
        USA = data[data["Country"] == "United States"]                              # Escogemos EEUU 
        CHINA = data[data["Country"] == "China"]                                    # Escogemos China

    # Calculamos 'PesoEstado' como el gasto gubernamental entre el PIB para cada región
        ZonaEuro["PesoEstado"] = ZonaEuro["Gov_Consumption"] / ZonaEuro["GDP"]
        USA["PesoEstado"] = USA["Gov_Consumption"] / USA["GDP"]
        CHINA["PesoEstado"] = CHINA["Gov_Consumption"] / CHINA["GDP"]

    # calculamos la media de 'PesoEstado para la zona euro 
        ZonaEuro6 = ZonaEuro.groupby("Year")["PesoEstado"].mean().reset_index()

        USA3 = USA.copy()
        CHINA3 = CHINA.copy()

    # Añadimos la columna región para cada zona
        ZonaEuro6['Region'] = 'Eurozone'
        USA3['Region'] = 'United States'
        CHINA3['Region'] = 'China'

        # Concatenamos los dataframes
        all_data = pd.concat([ZonaEuro6[['Year', 'PesoEstado', 'Region']], 
                            USA3[['Year', 'PesoEstado', 'Region']], 
                            CHINA3[['Year', 'PesoEstado', 'Region']]])

        # Usamos px
        fig = px.line(all_data, x='Year', y='PesoEstado', color='Region', 
                    labels={'PesoEstado': 'Government Consumption as % of GDP'},
                    title='Government Consumption as a Percentage of GDP (1970-2021)')

        fig.update_layout(title_font_color="black", legend_title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black", legend_font_color="black" )
        fig.update_xaxes(tickfont=dict(color="black"))
        fig.update_yaxes(tickfont=dict(color="black")) 
        
        st.plotly_chart(fig)   # Usamos esto en vez de show(fig) para que no nos abra una ventana ajena a streamlit y se muestre en nuestra app
        
    # Segunda fila de gráficas
    
    col1, col2 = st.columns(2)
    
    with col1:
    
        ZonaEuro = data[data["Currency"] == "Euro"].drop(columns=["Currency"])   # Agrupamos la zona euro en función de la moneda €
        USA = data[data["Country"] == "United States"]                           # Escogemos EEUU
        CHINA = data[data["Country"] == "China"]                                 # Escogemos China

        # Calculamos 'PesoInversion' como el Gasto en Consumo Final(GCF) entre el PIB para cada región
        ZonaEuro["PesoInversion"] = ZonaEuro["GCF"] / ZonaEuro["GDP"]
        USA["PesoInversion"] = USA["GCF"] / USA["GDP"]
        CHINA["PesoInversion"] = CHINA["GCF"] / CHINA["GDP"]

        # Calculamos la media de la zona euro
        ZonaEuro7 = ZonaEuro.groupby("Year")["PesoInversion"].mean().reset_index()

        USA3 = USA.copy()
        CHINA3 = CHINA.copy()

        # Añadimos región a cada df
        ZonaEuro7['Region'] = 'Eurozone'
        USA3['Region'] = 'United States'
        CHINA3['Region'] = 'China'

        # Concatenamos todos los df's
        all_data = pd.concat([ZonaEuro7[['Year', 'PesoInversion', 'Region']], 
                            USA3[['Year', 'PesoInversion', 'Region']], 
                            CHINA3[['Year', 'PesoInversion', 'Region']]])

        # usamos px
        fig = px.line(all_data, x='Year', y='PesoInversion', color='Region', 
                    labels={'PesoInversion': 'Investment as % of GDP'},
                    title='Investment as a Percentage of GDP (1970-2021)')
        
        fig.update_layout(title_font_color="black", legend_title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black", legend_font_color="black" )
        fig.update_xaxes(tickfont=dict(color="black"))
        fig.update_yaxes(tickfont=dict(color="black")) 
        
        st.plotly_chart(fig)  # Usamos esto en vez de show(fig) para que no nos abra una ventana ajena a streamlit y se muestre en nuestra app


    with col2:
        # Preparamos la Eurozona con una lista de los países integrantes
        eurozona = ["Germany", "Austria", "Belgium", "Cyprus", "Slovakia", "Spain", "Estonia", "Finland", "France", "Greece", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal"]
        df_eurozona = data[data["Country"].isin(eurozona)] # Preparamos el df de la eurozona
        # Preparamos una lista con los países a comparar con la Eurozona
        otros = ["United States", "Japan", "China", "United Kingdom", "Republic of Korea", "India", "Russian Federation"]
        df_otros = data[data["Country"].isin(otros)]
        
        # Agrupamos otro por país y año y calculamos el total de Consumo gubernamental
        df_otros_total = df_otros.groupby(['Country', 'Year'])['Consumption'].sum().reset_index()
        # Agrupamos la eurozona por año y calculamos su consumo total
        df_eurozona_total = df_eurozona.groupby('Year')['Consumption'].sum().reset_index()
        df_eurozona_total['Country'] = 'Eurozone'

        df_combined_gov = pd.concat([df_otros_total, df_eurozona_total], ignore_index=True)

        fig = px.line(df_combined_gov, x='Year', y='Consumption', color='Country',
                    title='Annual Government Consumption: Eurozone vs Other Countries',
                    labels={'consumption': 'Total Government Consumption', 'Year': 'Year'},
                    color_discrete_map={'Eurozone': '#001489',
                                        'United States': '#6fa8dc',
                                        'China': '#FF0000',
                                        'India': 'brown',
                                        'Republic of Korea': 'pink',
                                        'United Kingdom': 'black',
                                        'Japan': 'purple',
                                        'Russian Federation': 'green'})

        fig.update_layout(legend_title_text='Country', title_font_color="black", legend_title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black", legend_font_color="black" )
        fig.update_xaxes(tickfont=dict(color="black"))
        fig.update_yaxes(tickfont=dict(color="black"))
        st.plotly_chart(fig)  # Usamos esto en vez de show(fig) para que no nos abra una ventana ajena a streamlit y se muestre en nuestra app
    
    # Tercera fila de gráficas    

    col1, col2 = st.columns(2)
    
    with col1:
        # Preparamos la Eurozona con una lista de los países integrantes
        eurozona = ["Germany", "Austria", "Belgium", "Cyprus", "Slovakia", "Spain", "Estonia", "Finland", "France", "Greece", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal"]
        df_eurozona = data[data["Country"].isin(eurozona)] # Preparamos el df de la eurozona
        
        # Preparamos una lista con los países a comparar con la Eurozona
        otros = ["United States", "Japan", "China", "United Kingdom", "Republic of Korea", "India", "Russian Federation"]
        df_otros = data[data["Country"].isin(otros)]
        df_otros_avg = df_otros.copy()
        # Agrupamos otro por país y año y calculamos el promedio de PIB per cápita
        df_eurozona_avg = df_eurozona.groupby('Year')['GDP_pc'].mean().reset_index()
        df_eurozona_avg['Country'] = 'Eurozone'

        # Combinamos los df's
        df_combined = pd.concat([df_otros_avg, df_eurozona_avg], ignore_index=True)

        # Optamos por una grafica scatter para visualizar mejor los años por separado
        fig = px.scatter(df_combined, x='Year', y='GDP_pc', color='Country',
                        title='GDP per Capita Comparison: Eurozone vs Other Countries',
                        labels={'GDP_pc': 'GDP per Capita (mean)', 'Year': 'Year'},
                        color_discrete_map={'Eurozone': '#001489',
                                            'United States': '#6fa8dc',
                                            'China': '#FF0000',
                                            'India': 'brown',
                                            'Republic of Korea': 'pink',
                                            'United Kingdom': 'black',
                                            'Japan': 'purple',
                                            'Russian Federation': 'green'})
        fig.update_traces(marker=dict(size=8),
                        selector=dict(mode='markers'))
        fig.update_layout(legend_title_text='Country', title_font_color="black", legend_title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black", legend_font_color="black" )
        fig.update_xaxes(tickfont=dict(color="black"))
        fig.update_yaxes(tickfont=dict(color="black"))

        st.plotly_chart(fig)  # Usamos esto en vez de show(fig) para que no nos abra una ventana ajena a streamlit y se muestre en nuestra app

    with col2:
        
        # Preparamos la Eurozona con una lista de los países integrantes
        eurozona = ["Germany", "Austria", "Belgium", "Cyprus", "Slovakia", "Spain", "Estonia", "Finland", "France", "Greece", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal"]
        df_eurozona = data[data["Country"].isin(eurozona)]  # Preparamos el df de la eurozona
        # Preparamos una lista con los países a comparar con la Eurozona
        otros = ["United States", "Japan", "China", "United Kingdom", "Republic of Korea", "India", "Russian Federation"]
        df_otros = data[data["Country"].isin(otros)]

        df_otros_GDP = df_otros.copy()
        #Creamos el total GDP de la Eurozona
        gdp_total_eurozona = df_eurozona.groupby('Year')['GDP'].sum().reset_index()
        gdp_total_eurozona['Country'] = 'Eurozone Total'    
        df_comparacion = pd.concat([df_otros_GDP, gdp_total_eurozona], ignore_index=True)

        # Ordenamos el DataFrame por GDP para que la visualización sea más clara
        df_comparacion = df_comparacion.sort_values(by=['Year', 'GDP'])

        # Creamos la gráfica de barras
        fig = px.scatter(df_comparacion, x='Year', y='GDP', orientation='h', color='Country',
                    labels={'GDP': 'GDP Total', 'Year': 'Year'},
                    title='GDP Comparison: Eurozone Total vs Other Countries',
                    hover_data={'GDP': ':,.2f', 'Year': True},              # Formatea el GDP en el tooltip para que tenga dos decimales
                    color_discrete_map={'Eurozone Total': '#001489',
                                        'United States': '#6fa8dc',
                                        'China': '#FF0000',
                                        'India': 'brown',
                                        'Republic of Korea': 'pink',
                                        'United Kingdom': 'black',
                                        'Japan': 'purple',
                                        'Russian Federation': 'green'})  
        fig.update_traces(marker=dict(size=8),
                        selector=dict(mode='markers'))
        fig.update_layout(legend_title_text='Country', title_font_color="black", legend_title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black", legend_font_color="black" )
        fig.update_xaxes(tickfont=dict(color="black"))
        fig.update_yaxes(tickfont=dict(color="black"))

        # Mostrar la gráfica
        st.plotly_chart(fig)  # Usamos esto en vez de show(fig) para que no nos abra una ventana ajena a streamlit y se muestre en nuestra app
    
# Definimos la variable para mostrar el informe en PowerBI
def power_bi():                                  
    st.title("PowerBI Analysis")
    st.header("Pick a dashboard")
    # URL del dashboard de Power BI
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZDZhYzdmMWQtMmNhYS00MTYwLTg2YWItNWQxZTNmMDNlODQyIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9"
    
    # Mostrar el iframe del dashboard de Power BI
    st.components.v1.iframe(powerbi_url, height=600)

# Definimos la función para el predictor y predecir el GDP mediante diferentes modelos
def predictor():

    # URL del endpoint de inferencia
    endpoint_url = "https://machinelearningupgrade-gei.eastus.inference.ml.azure.com/score"
    # Token de autenticación
    auth_token = st.secrets["DB_TOKEN"]

    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    st.header("Eurozone GDP Prediction")
    
    # Cargar datos del CSV al iniciar
    if 'predictions' not in st.session_state:
        try:
            initial_data = pd.read_csv(r"Data/Eurozona.csv")  # Asegúrate de especificar la ruta correcta a tu CSV
            st.session_state.predictions = initial_data.to_dict('records')
        except Exception as e:
            st.error(f"Error loading initial data: {e}")
            st.session_state.predictions = []

    # Crear el formulario
    with st.form(key='gdp_form'):
        year = st.number_input("Year", min_value=2022, max_value=2041, value=2022)
        submit_button = st.form_submit_button(label='Predict')

    # Realizar la inferencia al enviar el formulario
    if submit_button:
        # Convertir el año en la fecha esperada por el modelo
        date_str = datetime(year, 1, 1).strftime("%Y-%m-%dT%H:%M:%S")
        
        # Datos de entrada para la inferencia
        data = {
            "input_data": {
                "columns": ["Year"],
                "index": [0],
                "data": [[date_str]]
            }
        }

        # Hacer la solicitud POST
        response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            st.write("Response JSON:", result)  # Imprimir la estructura de la respuesta para depuración

            # Ajustar esta parte según la estructura real de la respuesta
            # Asumimos que la respuesta tiene una clave 'predictions' que contiene la predicción
            if isinstance(result, list) and len(result) > 0:
                # Si la respuesta es una lista, se asume que la predicción está en el primer elemento
                prediction = result[0]  # Ajusta esto según sea necesario
                # Almacenar el resultado de la predicción
                st.session_state.predictions.append({"Year": year, "GDP": prediction})
                st.success(f"Prediction for {year}: {prediction}")
            elif 'prediction' in result:
                prediction = result['prediction']
                # Almacenar el resultado de la predicción
                st.session_state.predictions.append({"Year": year, "GDP": prediction})
                st.success(f"Prediction for {year}: {prediction}")
            else:
                st.error("Error: 'prediction' key not found in the response.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    # Mostrar la gráfica actualizada
    if st.session_state.predictions:
        df = pd.DataFrame(st.session_state.predictions)
        if 'GDP' in df.columns:
            st.line_chart(df.set_index('Year')['GDP'])
        else:
            st.error("Column 'y' not found in the data.")
        
    with st.expander("Model comparison"):
        # Cargamos ARIMA para comparar      
        st.title('ARIMA Model Predictions')
            
        df = pd.read_csv(r"Data/ARIMAForecast.csv")
            
        plt.figure(figsize=(12, 6))
        
        #  Dibujamos predicciones
        sns.lineplot(data=df, x='Year', y='ARIMAF', label='Predicted GDP', color='red', linestyle='--')
        
        # Dibujamos los datos reales
        sns.lineplot(data=df, x='Year', y='GDP', label='Histórico', color='#001489')
        
        # DIbujamos intervalos de confianza
        plt.fill_between(df['Year'], df['Lower'], df['Upper'], color='red', alpha=0.1)
        
        
        plt.title('ARIMA Model Forecasting for Eurozone GDP')
        plt.xlabel('Year')
        plt.ylabel('GDP')
        plt.legend()
        st.pyplot(plt)
        
        # Cargamos el modelo NeuralProphet para comparar      
        st.title('NeuralProphet Model Predictions')
            
        dfnp = pd.read_csv(r"Data/NeuralProphetForecast_limits.csv")
        
        plt.figure(figsize=(12, 6))
        
        #  Dibujamos predicciones
        sns.lineplot(data=dfnp, x='ds', y='yhat', label='Predicted GDP', color='red', linestyle='--')
        
        # Dibujamos los datos reales
        sns.lineplot(data=dfnp, x='ds', y='y', label='Histórico', color='#001489')
        
        # DIbujamos intervalos de confianza
        plt.fill_between(df['Year'], df['Lower'], df['Upper'], color='red', alpha=0.1)
        
        
        plt.title('NeuralProphet Model Forecasting for Eurozone GDP')
        plt.xlabel('Year')
        plt.ylabel('GDP')
        plt.legend()
        st.pyplot(plt)

#definimos la función para mostrar el video de despedida    
def video():
    st.header("Farewell video")
    st.video(r"Archivos/Top 15 países PIBpc.mp4")

# Definimos la función para mostrar el dataset completo
def show_dataset(): 
    st.header("Full dataset")
    st.dataframe(data)



# Definimos la variable options para desplegar las diferentes funciones que hemos creado
options = {
    "Landing": show_landing,
    "Analysis": analisis,
    "Dashboard": power_bi,
    "Predictor": predictor,
    "Farewell video": video,
    "Full dataset": show_dataset    
}
if option in options:
    options[option]() 
