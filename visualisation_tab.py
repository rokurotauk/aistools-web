import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
import os
import tempfile
import zipfile
import itertools
from folium.plugins import HeatMap
from streamlit_folium import st_folium

def render_visualisation_tab():
    st.title("AIS Map Visualisation App")
    COLOR_CYCLE = itertools.cycle(['red', 'blue', 'green', 'orange', 'purple', 'darkred',
                                   'lightblue', 'darkgreen', 'cadetblue', 'pink', 'black', 'gray',
                                   'lightgreen', 'beige', 'lightgray', 'darkblue', 'lightred'])

    mode = st.radio("Select display mode:", ["positions", "heatmap"])
    show_trails = st.checkbox("Show vessel trail lines (positions mode only)", value=True)

    uploaded_csvs = st.file_uploader("Upload AIS CSV files", accept_multiple_files=True, type=["csv"], key="visual_csv")
    uploaded_poi = st.file_uploader("Optional: Upload POI CSV", type="csv", key="visual_poi")
    uploaded_shapefile = st.file_uploader("Optional: Upload Shapefile (.zip)", type="zip", key="visual_shp")

    fmap = folium.Map(location=[0, 0], zoom_start=2)
    mmsi_colors = {}

    def process_csv_as_positions(df, filename):
        layer = folium.FeatureGroup(name=f"Positions: {filename}")
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude'])
        for mmsi in df['mmsi'].unique():
            mmsi_data = df[df['mmsi'] == mmsi].sort_values(by='timestamp')
            if mmsi not in mmsi_colors:
                mmsi_colors[mmsi] = next(COLOR_CYCLE)
            color = mmsi_colors[mmsi]
            trail_coords = []
            for lat, lon, timestamp in zip(mmsi_data['latitude'], mmsi_data['longitude'], mmsi_data['timestamp']):
                label = f"MMSI: {mmsi}<br>Timestamp: {timestamp}<br>Lat: {lat}, Lon: {lon}"
                folium.CircleMarker(location=[lat, lon], radius=6, color=color, fill=True,
                                    fill_opacity=0.7, popup=label).add_to(layer)
                trail_coords.append([lat, lon])
            if show_trails and trail_coords:
                folium.PolyLine(trail_coords, color=color, weight=2.5, opacity=0.6).add_to(layer)
        layer.add_to(fmap)

    def process_csv_as_heatmap(df, filename):
        df = df.dropna(subset=['latitude', 'longitude'])
        heat_data = df[['latitude', 'longitude']].values.tolist()
        layer = folium.FeatureGroup(name=f"Heatmap: {filename}")
        HeatMap(heat_data, radius=8, blur=15, max_zoom=6).add_to(layer)
        layer.add_to(fmap)

    def add_poi_layer(df):
        if not {'name', 'mmsi', 'latitude', 'longitude'}.issubset(df.columns):
            st.warning("POI file missing required columns.")
            return
        layer = folium.FeatureGroup(name="Points of Interest")
        for _, row in df.iterrows():
            popup = f"<b>{row['name']}</b><br>MMSI: {row['mmsi']}<br>Lat: {row['latitude']}, Lon: {row['longitude']}"
            folium.Marker(location=[row['latitude'], row['longitude']], popup=popup,
                          icon=folium.Icon(color='darkblue', icon='info-sign')).add_to(layer)
        layer.add_to(fmap)

    def add_shapefile(zip_file):
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zip_file, "r") as z:
                z.extractall(tmpdir)
            shp_files = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]
            if not shp_files:
                st.warning("No .shp file found in ZIP archive")
                return
            shp_path = os.path.join(tmpdir, shp_files[0])
            gdf = gpd.read_file(shp_path)
            if gdf.crs is None:
                gdf.set_crs(epsg=3857, inplace=True)
            gdf = gdf.to_crs(epsg=4326)
            tooltip_fields = [col for col in gdf.columns if col != 'geometry']
            folium.GeoJson(gdf, name=f"Shapefile: {shp_files[0]}",
                           tooltip=folium.GeoJsonTooltip(fields=tooltip_fields)).add_to(fmap)

    if uploaded_csvs:
        with st.spinner("Processing uploaded AIS data..."):
            progress = st.progress(0)
            total = len(uploaded_csvs)
            for idx, file in enumerate(uploaded_csvs):
                try:
                    df = pd.read_csv(file)
                    if not {'latitude', 'longitude', 'mmsi', 'timestamp'}.issubset(df.columns):
                        st.warning(f"{file.name} missing required columns.")
                        continue
                    if mode == "positions":
                        process_csv_as_positions(df, file.name)
                    else:
                        process_csv_as_heatmap(df, file.name)
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
                progress.progress((idx + 1) / total)

    if uploaded_poi:
        try:
            df_poi = pd.read_csv(uploaded_poi)
            add_poi_layer(df_poi)
        except Exception as e:
            st.error(f"Error reading POI file: {e}")

    if uploaded_shapefile:
        try:
            add_shapefile(uploaded_shapefile)
        except Exception as e:
            st.error(f"Error reading shapefile: {e}")

    folium.LayerControl().add_to(fmap)
    st_folium(fmap, width=1200, height=700)