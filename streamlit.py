import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters


st.title("📊 Tableau de bord gestion des ventes")
st.set_page_config(page_title='Tableau de bord gestion des ventes', page_icon=':bar_chart:')

data = pd.read_csv("donnees_ventes_etudiants.csv")
df = pd.DataFrame(data)

# Dictionnaire de correspondance codes -> noms complets des �tats US
state_mapping = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", 
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", 
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", 
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", 
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", 
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", 
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", 
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", 
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", 
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", 
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", 
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", 
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", 
    "WI": "Wisconsin", "WY": "Wyoming"
}

state_latlon = {
    "Alabama": [32.806671, -86.791130],
    "Alaska": [61.370716, -152.404419],
    "Arizona": [33.729759, -111.431221],
    "Arkansas": [34.969704, -92.373123],
    "California": [36.116203, -119.681564],
    "Colorado": [39.059811, -105.311104],
    "Connecticut": [41.597782, -72.755371],
    "Delaware": [39.318523, -75.507141],
    "District of Columbia": [38.905985, -77.033418],
    "Florida": [27.766279, -81.686783],
    "Georgia": [33.040619, -83.643074],
    "Hawaii": [21.094318, -157.498337],
    "Idaho": [44.240459, -114.478828],
    "Illinois": [40.349457, -88.986137],
    "Indiana": [39.849426, -86.258278],
    "Iowa": [42.011539, -93.210526],
    "Kansas": [38.526600, -96.726486],
    "Kentucky": [37.668140, -84.670067],
    "Louisiana": [31.169546, -91.867805],
    "Maine": [44.693947, -69.381927],
    "Maryland": [39.063946, -76.802101],
    "Massachusetts": [42.230171, -71.530106],
    "Michigan": [43.326618, -84.536095],
    "Minnesota": [45.694454, -93.900192],
    "Mississippi": [32.741646, -89.678696],
    "Missouri": [38.456085, -92.288368],
    "Montana": [46.921925, -110.454353],
    "Nebraska": [41.125370, -98.268082],
    "Nevada": [38.313515, -117.055374],
    "New Hampshire": [43.452492, -71.563896],
    "New Jersey": [40.298904, -74.521011],
    "New Mexico": [34.840515, -106.248482],
    "New York": [42.165726, -74.948051],
    "North Carolina": [35.630066, -79.806419],
    "North Dakota": [47.528912, -99.784012],
    "Ohio": [40.388783, -82.764915],
    "Oklahoma": [35.565342, -96.928917],
    "Oregon": [44.572021, -122.070938],
    "Pennsylvania": [40.590752, -77.209755],
    "Rhode Island": [41.680893, -71.511780],
    "South Carolina": [33.856892, -80.945007],
    "South Dakota": [44.299782, -99.438828],
    "Tennessee": [35.747845, -86.692345],
    "Texas": [31.054487, -97.563461],
    "Utah": [40.150032, -111.862434],
    "Vermont": [44.045876, -72.710686],
    "Virginia": [37.769337, -78.169968],
    "Washington": [47.400902, -121.490494],
    "West Virginia": [38.491226, -80.954453],
    "Wisconsin": [44.268543, -89.616508],
    "Wyoming": [42.755966, -107.302490]
}


# Cr�ation de la nouvelle colonne
df["State Complet"] = df["State"].map(state_mapping)

filter_cols = ["Region", "State Complet", "County", "City", "status"]
for col in filter_cols:
    if df[col].dtype == 'O': 
        df[col] = df[col].astype(str)
    else:
        df[col] = pd.to_numeric(df[col], errors='coerce')

#Question 1 : Sur une ligne mettre, le Calendrier pour donner à l’utilisateur le choix d’indiquer la période de vente choisi
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Date de début", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("Date de fin", max_date, min_value=min_date, max_value=max_date)
mask = (df["order_date"].dt.date >= start_date) & (df["order_date"].dt.date <= end_date)
df_filtered = df.loc[mask]

# Question 2 : 2. Mettez les filtres suivants sous cette ordre (à gauche de l’application) et des multiple choix :- Région- State- Contry- City,

# === FILTRES DYNAMIQUES ===
st.sidebar.header("Choose your filter")
dynamic_filters = DynamicFilters(df_filtered, filters=filter_cols)
dynamic_filters.display_filters(location='sidebar')

# Récupérer le DataFrame filtré
df_filters = dynamic_filters.filter_df()

# Vérifier si le DataFrame filtré n'est pas vide
if df_filters is not None and not df_filters.empty:
    # Question 3 : 3. Sur une ligne mettez les indicateurs ou KPI suivants sous format de valeur numérique:
    # === KPI ===
    st.subheader("KPI")
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Nombre de clients", df_filters['cust_id'].nunique())
    col2.metric("📈 Total vente", f"{df_filters['total'].sum():,.0f}")
    col3.metric("📈 Total commande", df_filters["order_id"].nunique())
     
    #Question 4: Sur une autre ligne ajouter les figures suivantes (ils doivent être sur la même ligne)

    # === Graphiques ===
    st.subheader("Graphiques")

    col3, col4 = st.columns(2)
    # Diagramme circulaire des ventes par Région
    fig_pie = px.pie(df_filters, names="Region", values="total", title="Répartition des ventes par région")
    #Diagramme en barre de la répartition des ventes par catégorie
    fig_bar = px.bar(df_filters.groupby("category")["total"].sum().reset_index(), x="category", y="total", title="Répartition des ventes par catégorie")

    with col3:
        st.plotly_chart(fig_bar, use_container_width=True)

    with col4:
        st.plotly_chart(fig_pie, use_container_width=True)
 
    #Question 5: Sur une autre ligne ajouter la diagramme en barre permettre de savoir le TOP 10 des meilleurs clients en vous servant de la variable Full_name
    fig_bar = px.bar(df_filters.groupby("full_name")["total"].sum().nlargest(10).sort_values().reset_index(), x="full_name", y="total", title="TOP 10 des meilleurs clients")
    st.plotly_chart(fig_bar, use_container_width=True)

    #Question 6: Sur une autre ligne ajouter les figures suivantes :
    #- Un histogramme qui donne la répartition de l’âge des clients : inspirer vous des histogrammes du cours_2
    #- Diagramme en barre qui compte le nombre d’hommes (+pourcentage) et de femmes en vous servant de la variable Gender
    col5, col6 = st.columns(2)
    # 📊 Diagramme en barre de la repartition des clients par Sexe
    gender_count = df_filters["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "cust_id"]
    gender_count["%"] = (gender_count["cust_id"] / gender_count["cust_id"].sum() * 100).round(1)

    fig_gender = px.bar(
        gender_count,
        x="Gender",
        y="cust_id",
        text=gender_count["%"].astype(str) + "%",
        title="Diagramme en barre de la repartition des clients par Sexe(%)"
    )
    # 📊 histogramme répartition de l’âge des clients
    fig_hist = px.histogram(df_filters, x="age", nbins=10, title="histogramme répartition de l’âge des clients")

    with col5:
        st.plotly_chart( fig_gender, use_container_width=True)

    with col6:
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # 7. Sur une autre ligne tracer la courbe qui donne le nombre total de
    # Vente suivant le mois. Pour ce faire, il faudrait faire un group By
    # par mois-année et calculer le nombre total de Vente par mois année
    
    df_filters["order_date"] = pd.to_datetime(df_filters["order_date"], errors="coerce")

    # Créer colonne "YearMonth"
    df_filters["YearMonth"] = df_filters["order_date"].dt.to_period("M").dt.to_timestamp()

    # Grouper par mois-année et calculer le total des ventes
    df_grouped = df_filters.groupby("YearMonth")["total"].sum().reset_index()

    # Tracer la courbe
    fig_line = px.line(df_grouped, x="YearMonth", y="total",
                    markers=True,
                    title="Nombre total de ventes par mois-année")

    st.plotly_chart(fig_line, use_container_width=True)

    # Question 8: Calculer le nombre total de vente par State en mettant en place une carte. Pour ce faire, pour chaque pays vous devez récupérer la latitude et longitude

    df_state = df_filters.groupby("State Complet")["total"].sum().reset_index()

    latitudes = []
    longitudes = []

    for state in df_state["State Complet"]:
        coords = state_latlon.get(state)
        if coords:
            latitudes.append(coords[0])
            longitudes.append(coords[1])
        else:
            latitudes.append(None)
            longitudes.append(None)

    df_state["lat"] = latitudes
    df_state["lon"] = longitudes

    fig_map = px.scatter_mapbox(
    df_state,
    lat="lat",
    lon="lon",
    size="total",
    hover_name="State Complet",
    hover_data={"total": True, "lat": False, "lon": False},
    zoom=3,
    height=500,
    title="Nombre total de vente par State"
    )

    fig_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig_map, use_container_width=True)

    # st.subheader("DataFrame filtré")
    # # Affichage du DataFrame filtré
    # st.dataframe(df_filters)
else:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
